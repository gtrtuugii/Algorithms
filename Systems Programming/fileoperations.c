// FILE AND DIRECTORY RELATED FUNCTIONS

/*
*   Creates a temporary folder in directory 'TEMPLATE'.
*   Folder name is randomised. Returns pointer to directory of folder
*/
#define TEMPLATE "/tmp/mt-XXXXXX"
char *create_temp_directory()
{
    char newdirname[] = TEMPLATE;
    char *tempdir = malloc(MAXPATHLEN);
    mkdtemp(newdirname); //Creates randomised directory
    strcpy(tempdir, newdirname);
    printf("Created temp directory: %s\n", tempdir);
    return tempdir;
}

/*
*   Moves file 'in_file' to directory 'out_dir'
*/
void move_file(char *in_file, char *out_dir)
{
    char *infile = malloc(MAXPATHLEN);
    strcpy(infile, in_file);
    char *outfile = malloc(MAXPATHLEN);
    strcpy(outfile, out_dir);

    pid_t pid = fork(); //fork process so child can complete task
    if (pid == -1)
    {
        printf("didn't fork, error occured\n");
        exit(EXIT_FAILURE);
    }
    else if (pid == 0) //child process
    {
        char *args[] = {"mv", infile, outfile, NULL};
        execvp(args[0], args);
        exit(EXIT_SUCCESS);
    }
    else //parent waits for child to complete
    {
        int status;
        waitpid(pid, &status, 0);
    }
}

/*
*   Removes file or directory 'dir_' and everything inside it
*/
void remove_directory(char *dir_)
{
    char dir[MAXPATHLEN];
    strcpy(dir, dir_);
    pid_t pid = fork(); //fork process so child can complete task
    if (pid == -1)
    {
        printf("didn't fork, error occured\n");
        exit(EXIT_FAILURE);
    }
    else if (pid == 0) //child process
    {
        char *args[] = {"rm", "-rf", dir, NULL};
        execvp(args[0], args);
        exit(EXIT_SUCCESS);
    }
    else //parent waits for child
    {
        int status;
        waitpid(pid, &status, 0);
    }
}

/*
*   Returns a struct containing metadata about specified file 'filename'
*/
struct stat file_attributes(char *filename)
{
    struct stat stat_buffer;
    if (stat(filename, &stat_buffer) != 0)
    {
        printf("Error: file not found or availiable");
        exit(EXIT_FAILURE);
    }
    return stat_buffer;
}

/*
*   Compares metadata about 2 files and returns the one which takes priority.
*/
char *compare_files(char *file1_, char *file2_)
{
    struct stat file1 = file_attributes(file1_);
    struct stat file2 = file_attributes(file2_);

    //return latest modified file
    if ((int)file1.st_mtime > (int)file2.st_mtime)
    {
        return file1_;
    }
    else if ((int)file1.st_mtime < (int)file2.st_mtime)
    {
        return file2_;
    }

    //return largest file
    if ((int)file1.st_size > (int)file2.st_size)
    {
        return file1_;
    }
    else if ((int)file1.st_size < (int)file2.st_size)
    {
        return file2_;
    }

    return file2_;
}

/*
*   Recursively propagates through all files and directories inside 'dir_name'
*   adds all files and directories to 'out_file'. If file already exists inside 
*   'out_file' then compare_files() is called to decide which one is used.
*/
void merge_directories(char *dir_name, char *out_file, char *parent_file)
{
    char *dirname = malloc(MAXPATHLEN);
    strcpy(dirname, dir_name);
    char *outfile = malloc(MAXPATHLEN);
    strcpy(outfile, out_file);

    char fullpath[MAXPATHLEN];
    DIR *dirp;
    struct dirent *dp;

    //open directory and access contents
    dirp = opendir(dirname);
    if (dirp == NULL)
    {
        exit(EXIT_FAILURE);
    }

    //Loop through all files and directories in current open directory
    while ((dp = readdir(dirp)) != NULL)
    {
        struct stat stat_buffer;
        sprintf(fullpath, "%s/%s", dirname, dp->d_name); //create path to current element
        if (!strcmp(dp->d_name, ".") || !strcmp(dp->d_name, ".."))
        {
            continue;
        }
        if (stat(fullpath, &stat_buffer) != 0)
        {
            printf("Error: file not found or availiable");
            exit(EXIT_FAILURE);
        }
        else if (S_ISDIR(stat_buffer.st_mode)) //If element is a directory
        {
            char newdir[MAXPATHLEN];
            //check directory doesn't exist in output file
            sprintf(newdir, "%s/%s%s", outfile, parent_file, dp->d_name);
            DIR *dir = opendir(newdir);
            if (dir)
            {
                closedir(dir);
            }
            else
            {
                //directory doesnt exist create it
                mkdir(newdir, 0700);
            }
            char parent[MAXPATHLEN];
            //create path file to directory and then call 'merge_directories' on it
            sprintf(parent, "%s%s/", parent_file, dp->d_name);
            merge_directories(fullpath, outfile, parent);
        }
        else if (S_ISREG(stat_buffer.st_mode)) //If element is a file
        {
            //check if file exists in output file
            char checkfile[MAXPATHLEN];
            sprintf(checkfile, "%s/%s%s", outfile, parent_file, dp->d_name);
            char newfile[MAXPATHLEN];
            sprintf(newfile, "%s/%s", outfile, parent_file);
            if (access(checkfile, F_OK) != 0)
            {
                //if not move the file there
                move_file(fullpath, newfile);
            }
            else
            {
                //if it does exist then preform checks to see which one wins
                char *pref_file = malloc(MAXPATHLEN);
                pref_file = compare_files(checkfile, fullpath);
                move_file(pref_file, newfile);
            }
        }
        else
        {
            printf("%s is unknown!\n", fullpath);
        }
    }
    closedir(dirp); //close directory and exit function
}
