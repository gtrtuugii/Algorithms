#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>


/*  
    Name:                Tuguldur Gantumur
    Student number(s):   22677666
 */


//  MAXIMUM NUMBER OF PROCESSES OUR SYSTEM SUPPORTS (PID=1..20)
#define MAX_PROCESSES                       20

//  MAXIMUM NUMBER OF SYSTEM-CALLS EVER MADE BY ANY PROCESS
#define MAX_SYSCALLS_PER_PROCESS            50

//  MAXIMUM NUMBER OF PIPES THAT ANY SINGLE PROCESS CAN HAVE OPEN (0..9)
#define MAX_PIPE_DESCRIPTORS_PER_PROCESS    10

//  TIME TAKEN TO SWITCH ANY PROCESS FROM ONE STATE TO ANOTHER
#define USECS_TO_CHANGE_PROCESS_STATE       5

//  TIME TAKEN TO TRANSFER ONE BYTE TO/FROM A PIPE
#define USECS_PER_BYTE_TRANSFERED           1


//  ---------------------------------------------------------------------

//  YOUR DATA STRUCTURES, VARIABLES, AND FUNCTIONS SHOULD BE ADDED HERE:

//System calls
enum {NEW = 0, READY, RUNNING, WAITING, SLEEPING, READING, WRITING, EXITING};
enum {SYS_COMPUTE = 0, SYS_SLEEP, SYS_EXIT, SYS_FORK};



int timetaken       = 0;

struct
{
    int state;      //NEW = 0, RUNNING, ...
    int nextsyscall;    //SYS_COMPUTE = 0, SYS_SLEEP,...

    struct
    {
        int syscall;
        int usecs;
        int otherPID;
        int nbytes;
        int pipedesc;
        

    } syscalls[MAX_SYSCALLS_PER_PROCESS];
    
} processes[MAX_PROCESSES];

void init_processes(void) //initialize, not complete ,example
{
    for(int p=0; p < MAX_PROCESSES; ++p){
        processes[p].state = NEW;
        processes[p].nextsyscall = 0;
        
        for(int s=0; s<MAX_SYSCALLS_PER_PROCESS; ++s){
            processes[p].syscalls[s].syscall = SYS_EXIT;
        }
    }
    
}


void sim_fork(int pid)
{
    switch(pid = fork())
        {
            case -1:
                printf("fork() failed\n");     // process creation failed
                exit(EXIT_FAILURE);
                break;
            case 0:
                printf("c:  value of pid=%i\n", pid); //new child
                printf("c:  child's pid=%i\n", getpid());
                printf("c:  child's parent pid=%i\n", getppid());
                break;
            default:                  // original parent process
                sleep(1);
                printf("p:  value of pid=%i\n", pid);
                printf("p:  parent's pid=%i\n", getpid());
                printf("p:  parent's parent pid=%i\n", getppid());
                break;
        }
         fflush(stdout);
}

//  ---------------------------------------------------------------------

void run_simulation(int timequantum, int pipesize)
{
    //parse_eventfile(<#char *program#>, <#char *eventfile#>);
    init_processes();
    
    //int max_time = 1000;
    
    
    
    for(int pid = 0; pid < MAX_PROCESSES; ++pid){
    if(processes[pid].syscalls[processes[pid].nextsyscall].syscall == SYS_COMPUTE)
        {
        //COMPUTE
            //if(max_time >= 1000,  = 0);
            //compute(pid);
            ++processes[pid].nextsyscall;
        }
    else if (processes[pid].syscalls[processes[pid].nextsyscall].syscall == SYS_SLEEP)
        {
            processes[pid].state = READY;
            processes[pid].state = RUNNING;
            sleep(pid);
            ++processes[pid].nextsyscall;
        }
    else if (processes[pid].syscalls[processes[pid].nextsyscall].syscall == SYS_EXIT)
        {
            processes[pid].state = READY;
            processes[pid].state = RUNNING;
            exit(pid);
            
        }
    else if (processes[pid].syscalls[processes[pid].nextsyscall].syscall == SYS_FORK)
        {
            processes[pid].state = READY;
            processes[pid].state = RUNNING;
            sim_fork(pid);
            processes[pid].state = READY;
            ++processes[pid].nextsyscall;
            
        }
   
    
    
    
    
    
    
    
    }
  
}
                    
                    
                    
//  FUNCTIONS TO VALIDATE FIELDS IN EACH eventfile - NO NEED TO MODIFY
int check_PID(char word[], int lc)
{
    int PID = atoi(word);

    if(PID <= 0 || PID > MAX_PROCESSES) {
        printf("invalid PID '%s', line %i\n", word, lc);
        exit(EXIT_FAILURE);
    }
    return PID;
}

int check_microseconds(char word[], int lc)
{
    int usecs = atoi(word);

    if(usecs <= 0) {
        printf("invalid microseconds '%s', line %i\n", word, lc);
        exit(EXIT_FAILURE);
    }
    return usecs;
}

int check_descriptor(char word[], int lc)
{
    int pd = atoi(word);

    if(pd < 0 || pd >= MAX_PIPE_DESCRIPTORS_PER_PROCESS) {
        printf("invalid pipe descriptor '%s', line %i\n", word, lc);
        exit(EXIT_FAILURE);
    }
    return pd;
}

int check_bytes(char word[], int lc)
{
    int nbytes = atoi(word);

    if(nbytes <= 0) {
        printf("invalid number of bytes '%s', line %i\n", word, lc);
        exit(EXIT_FAILURE);
    }
    return nbytes;
}

//  parse_eventfile() READS AND VALIDATES THE FILE'S CONTENTS
//  YOU NEED TO STORE ITS VALUES INTO YOUR OWN DATA-STRUCTURES AND VARIABLES
void parse_eventfile(char program[], char eventfile[])
{
#define LINELEN                 100
#define WORDLEN                 20
#define CHAR_COMMENT            '#'

//  ATTEMPT TO OPEN OUR EVENTFILE, REPORTING AN ERROR IF WE CAN'T
    FILE *fp    = fopen(eventfile, "r");

    if(fp == NULL) {
        printf("%s: unable to open '%s'\n", program, eventfile);
        exit(EXIT_FAILURE);
    }

    char    line[LINELEN], words[4][WORDLEN];
    int     lc = 0;
    //int     process_sys_calls[MAX_PROCESSES] = { 0 };
//  READ EACH LINE FROM THE EVENTFILE, UNTIL WE REACH THE END-OF-FILE
    while(fgets(line, sizeof line, fp) != NULL) {
        ++lc;

//  COMMENT LINES ARE SIMPLY SKIPPED
        if(line[0] == CHAR_COMMENT) {
            continue;
        }

//  ATTEMPT TO BREAK EACH LINE INTO A NUMBER OF WORDS, USING sscanf()
        int nwords = sscanf(line, "%19s %19s %19s %19s",
                                    words[0], words[1], words[2], words[3]);

//  WE WILL SIMPLY IGNORE ANY LINE WITHOUT ANY WORDS
        if(nwords <= 0) {
            continue;
        }
        
//  ENSURE THAT THIS LINE'S PID IS VALID
        int thisPID = check_PID(words[0], lc);
        
//  OTHER VALUES ON (SOME) LINES
        int otherPID, nbytes, usecs, pipedesc;
        
        int next = processes[thisPID-1].nextsyscall;

//  IDENTIFY LINES RECORDING SYSTEM-CALLS AND THEIR OTHER VALUES
//  THIS FUNCTION ONLY CHECKS INPUT;  YOU WILL NEED TO STORE THE VALUES
        if(nwords == 3 && strcmp(words[1], "compute") == 0) {
            usecs   = check_microseconds(words[2], lc);
            
            processes[thisPID-1].syscalls[next].syscall = SYS_COMPUTE;
            processes[thisPID-1].syscalls[next].usecs = usecs;
            
            ++processes[thisPID-1].nextsyscall;
            //processes[thisPID].syscalls[process_sys_calls[thisPID]].syscall = SYS_COMPUTE;
            //processes[thisPID].syscalls[process_sys_calls[thisPID]].usecs = usecs;
        }
        else if(nwords == 3 && strcmp(words[1], "sleep") == 0) {
            usecs   = check_microseconds(words[2], lc);
           
            processes[thisPID-1].syscalls[next].syscall = SYS_SLEEP;
            processes[thisPID-1].syscalls[next].usecs = usecs;
            
            ++processes[thisPID-1].nextsyscall;
            //processes[thisPID].syscalls[process_sys_calls[thisPID]].syscall = SYS_SLEEP;
            //processes[thisPID].syscalls[process_sys_calls[thisPID]].usecs = usecs;
        }
        else if(nwords == 2 && strcmp(words[1], "exit") == 0) {
            processes[thisPID-1].syscalls[next].syscall = SYS_EXIT;
            
            ++processes[thisPID-1].nextsyscall;
            //processes[thisPID].syscalls[process_sys_calls[thisPID]].syscall = SYS_EXIT;
        }
        else if(nwords == 3 && strcmp(words[1], "fork") == 0) {
            otherPID = check_PID(words[2], lc);
            processes[thisPID-1].syscalls[next].syscall = SYS_FORK;
            processes[thisPID-1].syscalls[next].otherPID = otherPID;
            
            ++processes[thisPID-1].nextsyscall;
            //processes[thisPID].syscalls[process_sys_calls[thisPID]].syscall = SYS_FORK;
        }
        else if(nwords == 3 && strcmp(words[1], "wait") == 0) {
            otherPID = check_PID(words[2], lc);
            
            processes[thisPID-1].syscalls[next].syscall = WAITING;
            processes[thisPID-1].syscalls[next].otherPID = otherPID;
            

            
            ++processes[thisPID-1].nextsyscall;
            //processes[thisPID].syscalls[process_sys_calls[thisPID]].syscall = SYS_WAIT;
        }
        else if(nwords == 3 && strcmp(words[1], "pipe") == 0) {
            pipedesc = check_descriptor(words[2], lc);
            processes[thisPID-1].syscalls[next].syscall = READING;
           //processes[thisPID].syscalls[process_sys_calls[thisPID]].pipedesc = pipedesc;
            //processes[thisPID].syscalls[process_sys_calls[thisPID]].syscall = SYS_PIPE;
        }
        else if(nwords == 4 && strcmp(words[1], "writepipe") == 0) {
            pipedesc = check_descriptor(words[2], lc);
            nbytes   = check_bytes(words[3], lc);
            processes[thisPID-1].syscalls[next].syscall = WRITING;
            processes[thisPID-1].syscalls[next].pipedesc = pipedesc;
            processes[thisPID-1].syscalls[next].nbytes = nbytes;

            
            
            
            ++processes[thisPID-1].nextsyscall;
            //processes[thisPID].syscalls[process_sys_calls[thisPID]].pipedesc = pipedesc;
           // processes[thisPID].syscalls[process_sys_calls[thisPID]].nbytes = nbytes;
            //processes[thisPID].syscalls[process_sys_calls[thisPID]].syscall = SYS_WRITE_PIPE;
        }
        else if(nwords == 4 && strcmp(words[1], "readpipe") == 0) {
            pipedesc = check_descriptor(words[2], lc);
            nbytes   = check_bytes(words[3], lc);
            
            processes[thisPID-1].syscalls[next].syscall = READING;
            processes[thisPID-1].syscalls[next].pipedesc = pipedesc;
            processes[thisPID-1].syscalls[next].nbytes = nbytes;

            
            
            ++processes[thisPID-1].nextsyscall;
            //processes[thisPID].syscalls[process_sys_calls[thisPID]].pipedesc = pipedesc;
            //processes[thisPID].syscalls[process_sys_calls[thisPID]].nbytes = nbytes;
            //processes[thisPID].syscalls[process_sys_calls[thisPID]].syscall = SYS_READ_PIPE;
        }
//  UNRECOGNISED LINE
        else {
            printf("%s: line %i of '%s' is unrecognized\n", program,lc,eventfile);
            exit(EXIT_FAILURE);
        }

    }
    fclose(fp);
    


#undef  LINELEN
#undef  WORDLEN
#undef  CHAR_COMMENT
}

//  ---------------------------------------------------------------------

//  CHECK THE COMMAND-LINE ARGUMENTS, CALL parse_eventfile(), RUN SIMULATION
int main(int argc, char *argv[])
{
    int timequantum, pipesize;
    //check argc == 4
       // if not error .... exit
    if(argc != 4){
        printf(" argument number is incorrect %i\n",argc);
        exit(EXIT_FAILURE);
    }
    
    //check timequantum > 0
    // if not error .... exit
    //check pipesize > 0
    // if not error .... exit
    
    timequantum = atoi(argv[1]);
    pipesize = atoi(argv[2]);
    
    if(timequantum < 0 || pipesize < 0){
        printf("enter only positive values in arguments");
        exit(EXIT_FAILURE);
    }

    
    init_processes();
    
    parse_eventfile(argv[0], argv[1]);
    
    run_simulation(timequantum, pipesize);
   
    printf("timetaken %i\n", timetaken);
    return 0;
}
