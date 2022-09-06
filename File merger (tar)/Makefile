C99	= cc -std=c99 -Wall -pedantic -Werror

mergetars : mergetars.o tar.o 
	$(C99) -o mergetars \ 
		mergetars.c tar.o -lm

mergetars.o : mergetars.c mergetars.h
	$(C99) -c mergetars.c
	
tar.o : tar.c mergetars.h
	$(C99) -c tar.c

clean:
	rm -f *.o mergetars