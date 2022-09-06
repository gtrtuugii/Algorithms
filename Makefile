# Makefile for the CITS3003 project running on Linux
#
# Du Huynh
# April 2016

GCC_OPTIONS = -I lib/angel/include -I lib/lab_pc_specific/assimp/include -I lib/bitmap/include/ \
        -I lib/bitmap -I lib/freeglut/freeglut/freeglut/include/ -I lib/glew/include/ \
	-L /usr/lib64 -l:libGLEW.so.1.10 \
	-L lib/lab_pc_specific/assimp -l:libassimp.so.3 \
	-w -fpermissive -O3 -g \
        -std=c++11 \
	-D LAB_PC
GL_OPTIONS = -lglut -lGL -lXmu -lX11 -lm -Wl,-rpath,

LIBRARY = -Wl,-rpath,.

OPTIONS=$(GCC_OPTIONS) $(GL_OPTIONS)

SRC = src/scene-start.cpp lib/angel/src/InitShader.cpp lib/bitmap/src/bitmap.c

PROGRAM = scene-start
DIRT = $(wildcard *.o *.i *~ */*~ *.log assimp_log.txt)

RM = /bin/rm

# -------- rules for building programs --------

.PHONY: clean rmprogram clobber

default all: $(PROGRAM) 

scene-start: $(SRC)
	g++ -o scene-start $(SRC) $(OPTIONS) $(LIBRARY)

run: export LD_LIBRARY_PATH=lib/lab_pc_specific/assimp
run: scene-start
	./$(PROGRAM)

# -------- rules for cleaning up files that can be rebuilt --------

clean:
	$(RM) -f $(DIRT)

rmprogram:
	$(RM) -f $(PROGRAM) $(INIT_SHADER)

clobber: clean rmprogram
