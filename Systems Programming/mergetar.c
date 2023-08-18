// 
// Name(s): TUGULDUR GANTUMUR, LOH XUAN RU
// Student number(s): 22677666, 22880502

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include "mergetars.h" 

#define MAXPATHLEN 4096 // A reasonable value for maximum path length

int main(int argc, char *argv[]) {
    if (argc < 3) {
        printf("At least 3 arguments required, given: %i\n", argc);
        exit(EXIT_FAILURE);
    } else {
        for (int i = 1; i < argc; ++i) {
            if (strlen(argv[i]) > MAXPATHLEN) {
                printf("File path exceeds limit\n");
                exit(EXIT_FAILURE);
            }
        }
    }

    int SIZE = argc - 2;
    char *all_input[SIZE];
    char *all_directories[SIZE];

    // Store all input tars into an array
    for (int i = 1; i < argc - 1; ++i) {
        all_input[i - 1] = argv[i]; // Adjust index to start from 0
        printf("Storing %s into all_input[%i]\n", argv[i], i - 1);
    }

    // Create directories according to the number of input tars and expand the tar files into a directory
    for (int i = 0; i < SIZE; ++i) { // Loop through SIZE instead of argc - 1
        all_directories[i] = temp_directory();
        printf("Created %s\n", all_directories[i]);
        untar(all_input[i], all_directories[i]);
        list_directory(all_directories[i]);
    }

    // Create a new directory to merge input tar files in
    all_directories[SIZE] = temp_directory(); // Use SIZE index
    printf("Temporary directory %s is created to merge files in\n", all_directories[SIZE]);

    // Browse directories for files and move them depending on criteria
    for (int i = 0; i < SIZE; ++i) { // Loop through SIZE
        printf("Browsing into: %s\nMerging into: %s\n", all_directories[i], all_directories[SIZE]);
        browse_direct(all_directories[i], all_directories[SIZE], ""); 
    }

    // Remove input directories
    for (int i = 0; i < SIZE; ++i) {
        remove_dir(all_directories[i]);
    }

    // Transfer final directory into result.tar
    createTars(all_directories[SIZE], argv[argc - 1]);

    // Remove the final merged directory
    remove_dir(all_directories[SIZE]);

    return 0; // Return a value to indicate successful execution
}
