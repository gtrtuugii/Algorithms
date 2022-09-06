//  CITS2002 Project 2 2020
//  Name(s):             TUGULDUR GANTUMUR (, LOH XUAN RU)
//  Student number(s):   22677666 (, 22880502)
//
//  EXTENDED DEADLINE: 25/10/2020
//

/* WORKS PERFECTLY WHEN PASSING ARGUMENTS AS PATH I HAVENT TRIED PASSING THEM AS "testTar.tar" due to issues with Xcode, (for some reason it couldn't find them even though they were located in the same folder. I tried adding them to the local folder and Library/Developer/ as well). I assummed this issue will onnly occur with my IDE.
 */


#include "mergetars.h"

int main(int argc, char *argv[]) {
   
    int SIZE = argc - 2; //     TAKES INPUTS ARGV[1] -- ARGV[ARGC-1]
    char* all_input[SIZE]; //   STORE INPUTS ARGV[1] -- ARGV[ARGC-1]
    char* all_directories[SIZE]; //     CREATED DIRECTORIES

    if(argc < 3)
    {
        printf("at least 3 arguments required, given: %i\n",argc);
        exit(EXIT_FAILURE);
    }
    else
    {
        for(int i = 0; i < argc; ++i)
        {
            if(strlen(argv[i]) > MAXPATHLEN)
            {
                printf("file path exceeds limit"); //   IF THE PATH IS TOO LONG, EXIT
                exit(EXIT_FAILURE);
            }
        }

    }
    
    //  STORE ALL INPUT TARS INTO AN ARRAY
    //  argv[0] is mergetars and last argv is result.tar
    
    for(int i = 1; i < argc - 1; ++i)
    {
        all_input[i] = argv[i];
        printf("storing %s into all_input[%i]\n", argv[i], i);
    }
    
    //  CREATE DIRECTORIES ACCORDING TO NUMBER OF INPUT TARS
    //  AND EXPAND THE TAR FILES INTO A DIRECTORY
    
    for(int i = 1; i < argc - 1; ++i)
    {
        all_directories[i] = temp_directory();
        printf("CREATED %s\n", all_directories[i]);
        untar(all_input[i], all_directories[i]);
        list_directory(all_directories[i]); //LOOKS AT THE FILES WITHIN THE DIRECTORY
    }
    
    //  CREATE NEW DIRECTORY TO MERGE INPUT TAR FILES IN.
    all_directories[argc-1] = temp_directory();
    printf("Temporary directory %s is created to merge files in\n", all_directories[argc-1]);
    
    //  BROWSE DIRECTORIES FOR THE FILES AND MOVE DEPENDING ON
    //  IF IT MEETS THE CRITERIA
    
    for(int i = 1; i < argc-1; ++i)
    {
        printf("BROWSING INTO: %s\n MERGING INTO: %s\n",all_directories[i], all_directories[argc-1]);
        browse_direct(all_directories[i], all_directories[argc-1], "");
    }
    
    /*  CLEAN_UP/REMOVE_DIRECTORIES
     
     We can remove all input directories i.e argv[1] - argv[argc-1]

     */
    
    for(int i = 1; i < argc-1; ++i)
    {
        remove_dir(all_directories[i]);
    }
   
    //  TRANSFER FINAL DIRECTORY INTO RESULT.TAR
    
    createTars(all_directories[argc-1], argv[argc-1]);
    
    /* FINAL CLEAN UP
     Now that we have transferred the final directory into the
     result.tar (argv[argc-1]), we can now remove the final
     directory (merged directory)
     
     Similar to what Chris did in Workshop 8.
     
     Also could've removed all directories at the end.
     
     for(int i = 0; i < argc; ++i)
       {
           remove_dir(all_directories[i]);
       }
.
     */
    
    remove_dir(all_directories[argc-1]);
    


}
