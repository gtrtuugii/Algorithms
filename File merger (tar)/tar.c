//
//  Mod includes functions which manipulate or use the tar files.
//
//  NOTES:
//  * Cannot use cp, no marks awarded for using cp
//  * seek alternatives, maybe -mv (move) ?
//  * fork() and exec()
//  c – create a archive file.
//  x – extract a archive file.
//  v – show the progress of archive file.
//  f – filename of archive file.
//  t – viewing content of archive file.
//  j – filter archive through bzip2.
//  z – filter archive through gzip.
//  r – append or update files or directories to existing archive file.
//  W – Verify a archive file.
//  https://www.tecmint.com/18-tar-command-examples-in-linux/
//  http://www.ee.surrey.ac.uk/Teaching/Unix/unix2.html
//  https://linuxhint.com/exec_linux_system_call_c/#:~:text=In%20execl()%20system%20function,command%20and%20prints%20the%20output.
//  https://codeforwin.org/2018/03/c-program-to-list-all-files-in-a-directory-recursively.html
//
/*
    It is anticipated (though not required) that a successful project will use (some of) the following system-calls, and standard C99 & POSIX functions:

    perror(),  exit(),
    mkdtemp(),  mkdir(),  opendir(),  readdir(),  stat(),  closedir(),
    fork(),  execl(),  wait(),
    open(),  read(),  write(),  close(), utimes(),
    strcpy(),  strcmp(),  strdup(),
    malloc(),  calloc(),  realloc(), and  free().
 */

/*
    FROM LECTURE 17
 
void list_directory(char *dirname)
{
    DIR             *dirp;
    struct dirent   *dp;
    char  fullpath[MAXPATHLEN];

    dirp       = opendir(dirname);
    if(dirp == NULL) {
        perror( progname );
        exit(EXIT_FAILURE);
    }

    while((dp = readdir(dirp)) != NULL) {
        printf( "%s\n", dp->d_name );
        struct stat  stat_buffer;
        struct stat  *pointer = &stat_buffer;

        sprintf(fullpath, "%s/%s", dirname, dp->d_name );

        if(stat(fullpath, pointer) != 0) {
            perror( progname );
        }
        else if( S_ISDIR( pointer->st_mode )) {
            printf( "%s is a directory\n", fullpath );
        }
        else if( S_ISREG( pointer->st_mode )) {
            printf( "%s is a regular file\n", fullpath ); 
        }
        else
        {
            printf( "%s is unknown!\n", fullpath );
        }
    }
    closedir(dirp);
}

*/

#include "mergetars.h"


char* temp_directory()
{
    /*  CREATE A TEMPORARY DIRECTORY TO STORE FILES IN  */
    
    char newdirname[] = TEMPLATE;
    char *tempodir = malloc(MAXPATHLEN);
    mkdtemp(newdirname);  //    RANDOM DIRECTORY CREATED
    strcpy(tempodir, newdirname);
    if(tempodir == NULL)
    {
        printf("could not create a directory %s\n", tempodir);
    }
    return tempodir;
}

void list_directory(char *directname)
{
    /* THIS FUNCTION WILL SHOW THE CONTENTS OF A DIRECTORY
     AND WILL RECURSIVELY CALL ITSELF AGAIN IF THERE IS A
     DIRECTORY WITHIN THE DIRECTORY
     
     NOTE: STARTS WITH: "." , "..", ".DS_Store or "."
     
     */
    
    printf("LIST THE CONTENTS OF %s\n", directname);
    char  fpath[MAXPATHLEN];
    char dir_tempo[MAXPATHLEN];
    DIR             *dirx;
    struct dirent   *fd;

    dirx       = opendir(directname);
    if(dirx == NULL)
    {
        
        exit(EXIT_FAILURE);
    }

    while((fd = readdir(dirx)) != NULL) {
        printf( "%s\n", fd->d_name );
        struct stat  stat_buffer;
        struct stat  st = {0};
        struct stat  *pointer = &stat_buffer;

        sprintf(fpath, "%s/%s", directname, fd->d_name );
        
        if (!strcmp(fd->d_name, ".") || !strcmp(fd->d_name, ".."))
            //To list all files and sub-directories of a directory recursively
            {
                continue; //skip . and ..
            }

        if(stat(fpath, pointer) != 0) {
            printf("ERROR");
            exit(EXIT_FAILURE);
        }
        else if( S_ISDIR( pointer->st_mode )) {
            printf( "%s is a directory\n", fpath );
            
            //CREATE PATH
            sprintf(dir_tempo, "%s/%s", directname,fd->d_name);
            //CURRENT DIR TO OPEN
            DIR *currentdir = opendir(dir_tempo);
            
            if (stat(dir_tempo, &st) == -1)
            {
                //  CREATE DIR IF NON-EXISTENT
                //  PERMISSION DENIED ON 0600 ?
                //  CHANGED IT TO 0700 according to specs
                mkdir(dir_tempo, 0700);
            }
            else
            {
                closedir(currentdir);

            }
            
            //  IF IT IS A DIRECTORY WE WANT TO ACCESS IT AGAIN (RECURSION)
            //  TO ACCESS FILES
            //  CHANGE PARAMETER(s) AND CALL AGAIN.
            
            list_directory(dir_tempo);
        }
        else if( S_ISREG( pointer->st_mode )) {
            printf( "%s is a regular file\n", fpath );
        }
        else
        {
            printf( "%s is unknown!\n", fpath );
        }
    }
    closedir(dirx);
}




void untar(char* input, char* destination)
{
    /*  Transfers input tar file into output directory, i.e expands the tar.    */
    int  pid;
    pid = fork();
    if(pid == -1)
    {
        printf("fork() failed\n");
        exit(EXIT_FAILURE);
    }
    else if(pid == 0)
    {
        printf(" %s ---> %s\n", input, destination);
        
        char * binPath = "/usr/bin/tar";
        execl(binPath, "tar",  "-C", destination,"-xvf", input, NULL);
        exit(EXIT_SUCCESS);
    }
    else
    {
            int status;
            waitpid(pid, &status, 0);
    }
}


struct stat content_attrib(char *filename)
{
    /*  GETS THE FILE ATTRIBUTES    */
    
    struct stat attrib;
    if (stat(filename, &attrib) != 0)
    {
        printf("Error: file not found or availiable");
        exit(EXIT_FAILURE);
    }
    return attrib;
}

char *compare_attrib(char *input1, char *input2)
{
    /*
     This function wants to return the latest modified or
     largest file if the file names are the same.
     
     This function will compare file last modification time (st_mtime)
     and size (st_size)
    */
    
        struct stat file1 = content_attrib(input1);
        struct stat file2 = content_attrib(input2);
        

        if ((int)file1.st_mtime > (int)file2.st_mtime)
        {
            return input1;
        }
        else if ((int)file1.st_mtime < (int)file2.st_mtime)
        {
            return input2;
        }

        if((int)file1.st_mtime == (int)file2.st_mtime)
        {
            if ((int)file1.st_size > (int)file2.st_size)
            {
                return input1;
            }
            else if ((int)file1.st_size < (int)file2.st_size)
            {
                return input2;
            }
            else if((int)file1.st_size == (int)file2.st_size)
            {
                return input1;
            }
        }
    
        return input2;
}

void transfer(char *source, char *target)
{
    /*
     This function will move directories or files inbetween directories
     */

    pid_t pid = fork();
    if (pid == -1)
    {
        printf("FORK ERROR\n");
        exit(EXIT_FAILURE);
    }
    else if (pid == 0)
    {
        execl("/bin/mv", "mv", source, target, NULL);
        exit(EXIT_SUCCESS);
    }
    else
    {
        int status;
        waitpid(pid, &status, 0);
    }
}


void browse_direct(char *directory_name, char *target_file, char *source)
{

    /*
    BASED FROM LECTURE 17 (last 2 pages)
     
     
    This function will browse the directory (recursively if there's another directory
     within the directory) until it finds the regular files, then if the regular file   already exists ( access() ) it will compare the files based on size and time (using the compare_attrib() )
     */
    
    
    char path[MAXPATHLEN];
    char tempdir[MAXPATHLEN];
    char source_file[MAXPATHLEN];
    char file1[MAXPATHLEN];
    char file2[MAXPATHLEN];

    DIR           *d;
    struct dirent *dirx;

    d = opendir(directory_name);
    
    if (d == NULL)
     {
         exit(EXIT_FAILURE);
     }
    while((dirx = readdir(d)) != NULL)
    {
            struct stat  stat_buffer;
            struct stat  st = {0};
            struct stat  *pointer = &stat_buffer;

            sprintf(path, "%s/%s", directory_name, dirx->d_name ); //return path to direct
        
        
            if (!strcmp(dirx->d_name, ".") || !strcmp(dirx->d_name, ".."))
            {
                continue; //skip . and ..
            }

            if(stat(path, pointer) != 0) {
                printf("ERROR 404:");
            }
            else if( S_ISDIR( pointer->st_mode )) //FILE IS A DIRECTORY
            {
                printf( "%s is a directory\n", path );
                //CREATE PATH
                sprintf(tempdir, "%s/%s/%s", target_file, source, dirx->d_name);
                //CURRENT DIR TO OPEN
                DIR *currentdir = opendir(tempdir);
                
                if (stat(tempdir, &st) == -1)
                {
                    //  CREATE DIR IF NON-EXISTENT
                    //  PERMISSION DENIED ON 0600 ?
                    //  CHANGED IT TO 0700 according to specs
                    mkdir(tempdir, 0700);
                }
                else
                {
                    closedir(currentdir);

                }
                
                //  CREATE A PATH TO DIR
                sprintf(source_file, "%s%s/", source, dirx->d_name);
                
                //  IF IT IS A DIRECTORY WE WANT TO ACCESS IT AGAIN (RECURSION)
                //  TO ACCESS FILES
                //  CHANGE PARAMETERS AND CALL BROWSE_DIRECT() AGAIN.
                
                browse_direct(path, target_file, source_file);
            }
            else if( S_ISREG( pointer->st_mode ))
            {
                //  THE FILE IS A REGULAR FILE

                
                sprintf(file1, "%s/%s/%s", target_file, source, dirx->d_name);
                sprintf(file2, "%s/%s", target_file, source);
                //file1 = ("%s/%s/%s", target_file,source,dirx->d_name); WHAT IT MEANS
                
                if( access( file1, F_OK ) != -1 ) //CHECKS IF FILE EXISTS
                {
                    //  FILE EXISTS IN THE DIRECTORY
                    printf("FILE: %s EXISTS",file1);
                    //  RETURN FILE WITH LATEST MOD TIME OR BIGGEST SIZE
                    //  latest mfile = later m_time or bigger size
                    char *latest_mfile = compare_attrib(file1, path);
                    transfer(latest_mfile, file2);
                } else {
                    //  FILE DOESNT EXIST SO WE WANT TO MOVE
                    //  THE FILE INTO THE DIR/PATH
                    printf("%s ---> %s\n",path, file2);
                    transfer(path, file2);
                }
            }
            else {
                //  UNKNOWN FILE
                printf( "%s UNKNOWN FILE!\n", path );
            }
        }
        closedir(d);
    
     
}

void createTars(char *srcpath, char *finfilepath)
{
    /* This function uses the -cvf command and
     c - will create a archive file.
     v - show the progress of archive file.
     f - filename of archive file.
     */
    
    pid_t pid = fork();
    if (pid == -1)
    {
        printf("didn't fork, error occured\n");
        exit(EXIT_FAILURE);
    }
    else if (pid == 0)
    {
        printf("%s ---> %s\n", srcpath, finfilepath);
        char * binPath = "/usr/bin/tar";
        execl(binPath, "...", "-cvf", finfilepath, "-C", srcpath, ".", NULL);
        exit(EXIT_SUCCESS);
    }
    else
    {
        int status;
        waitpid(pid, &status, 0);
    }

}


void remove_dir(char* directory)
{
    /* This function uses the rm -rf command which is one of the fastest way to delete a folder and its contents. ... The some of options used with rm command are. rm command in Linux is used to delete files. rm -r command deletes the folder recursively, even the empty folder. rm -f command removes 'Read only File' without asking.
     */
    
    pid_t pid = fork();
    if (pid == -1)
    {
        printf("FORK ERROR\n");
        exit(EXIT_FAILURE);
    }
    else if (pid == 0)
    {
        printf("... CLEANING %s ...\n", directory);
        execl("/bin/rm", "rm", "-r", directory, NULL);
        exit(EXIT_SUCCESS);
    }
    else
    {
        int status;
        waitpid(pid, &status, 0);
    }
    
    
}

