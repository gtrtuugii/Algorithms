
#ifndef _MERGETARSH_
#define _MERGETARSH_

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdbool.h>
#include <stdarg.h>
#include <time.h>
#include <sys/wait.h>
#include <sys/param.h>
#include <sys/stat.h>
#include <dirent.h>
#include <fcntl.h>

#define TEMPLATE    "/tmp/gtrtuugii-XXXXXX"
#define _POSIX_C_SOURCE 200809L
#define MYSIZE 10000

extern char* temp_directory(void);
extern void remove_dir(char* directory);
extern void untar(char* input, char* destination);
extern void transfer(char *in_dir, char *out_dir);
extern void browse_direct(char *directory_name, char *target_file, char *source);
extern void createTars(char *srcpath, char *finfilepath);

extern void list_directory(char *dirname);


#endif /* mergetars_h */
