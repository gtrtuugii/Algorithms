cmake_minimum_required(VERSION 3.10)
project(start_scene)

set(CMAKE_CXX_STANDARD 17)

set(OpenGL_GL_PREFERENCE "GLVND")
set(BUILD_SHARED_LIBS OFF CACHE BOOL "" FORCE)

set(ONLY_LIBS ON CACHE BOOL "" FORCE)
set(glew-cmake_BUILD_SHARED OFF CACHE BOOL "" FORCE)
set(glew-cmake_BUILD_STATIC ON CACHE BOOL "" FORCE)
include_directories(lib/glew/include)
include_directories(lib/glew/include/GL)
add_compile_definitions(GLEW_INCLUDE=<${CMAKE_SOURCE_DIR}/lib/glew/include/GL/glew.h>)
add_compile_definitions(GLEW_STATIC)
add_subdirectory(lib/glew EXCLUDE_FROM_ALL)

include_directories(lib/freeglut/freeglut/freeglut/include)
include_directories(lib/freeglut/freeglut/freeglut/include/GL)
if (NOT APPLE)
	set(FREEGLUT_BUILD_DEMOS OFF CACHE BOOL "" FORCE)
	set(FREEGLUT_BUILD_SHARED_LIBS OFF CACHE BOOL "" FORCE)
	set(FREEGLUT_BUILD_STATIC_LIBS ON CACHE BOOL "" FORCE)
	add_compile_definitions(FREEGLUT_STATIC)
	add_subdirectory(lib/freeglut/freeglut/freeglut EXCLUDE_FROM_ALL)
endif()

set(ASSIMP_BUILD_ASSIMP_TOOLS OFF CACHE BOOL "" FORCE)
set(ASSIMP_BUILD_TESTS OFF CACHE BOOL "" FORCE)
set(ASSIMP_INSTALL OFF CACHE BOOL "" FORCE)
add_subdirectory(lib/assimp EXCLUDE_FROM_ALL)

add_subdirectory(lib/bitmap)
add_subdirectory(lib/angel)

add_executable(start_scene src/scene-start.cpp src/gnatidread.h src/gnatidread2.h)

if (MSVC)
	set_property(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR} PROPERTY VS_STARTUP_PROJECT start_scene)
	set_property(TARGET start_scene PROPERTY VS_DEBUGGER_WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}")
endif(MSVC)

if (APPLE)
	target_link_libraries(start_scene angel libglew_static "-framework GLUT" assimp bitmap)
else()
	target_link_libraries(start_scene angel libglew_static freeglut_static assimp bitmap)
endif()

add_custom_command(TARGET start_scene
		POST_BUILD
		COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:start_scene> ${CMAKE_SOURCE_DIR})