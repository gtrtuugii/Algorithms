#"""Read and process a file of student names and marks.
   #Written for COSC121S2.
   #Author: Angus McGurkinshaw
   #Date: 29 July 2017.
#"""
#import statistics as stat

#def get_filename():
    #"""Return the name of the student data file to be processed"""
    #return "data.csv"


#def read_data(filename):
    #"""Read and return the contents of the given file.
       #The file is assumed to exist, or an exception will occur.
       #It is also assumed that each line of the file consists of a
       #student name, a comma, and a floating-point mark.
       #Returns: a list of (name, mark) tuples, where name is a string
       #and mark is a floating-point number.
    #"""
    ## ****** YOUR CODE HERE ******
    #infile = open(filename)
    #contents = infile.read()
    #lines = contents.splitlines()
    #result = []
    #for line in lines:
        #data = line.split(",")
        #name, mark = data
        #name = str(name)
        #mark = float(mark)
        #result.append((name, mark))
    #return result
        


#def statistics(student_data):
    #"""Given a list of (name, mark) pairs, returns a tuple
       #containing statistics extracted from the list. The tuple elements are
       #minimum_mark, maximum_mark, average_mark and top_students. The
       #first three are just floating point values. The last one is an
       #alphabetically ordered list of the names of all students whose
       #marks are equal to the maximum_mark.
    #"""
    ## ****** YOUR CODE HERE ******
    #marks = []
    #top_students = []
    #for name, mark in student_data:
        #marks.append(mark)
    #minimum_mark = min(marks)
    #maximum_mark = max(marks)
    #average_mark = stat.mean(marks)
    #for name, mark in student_data:
        #if mark == maximum_mark:
            #top_students.append(name)    
    #top_students.sort()
    #result = (minimum_mark, maximum_mark, average_mark, top_students)
    #return result    


#def print_results(stats):
    #"""Print the statistics given. The parameters 'stats' is a
       #tuple of the form returned by the 'statistics' function
       #above.
    #"""
    #(minimum, maximum, average, top_students) = stats
    #print("Minimum mark is: {:.1f}".format(minimum))
    #print("Maximum mark is: {:.1f}".format(maximum))
    #print("Average mark is: {:.1f}".format(average))

    #if len(top_students) == 1:
        #print("Top student: {}".format(top_students[0]))
    #else:
        #print("Top-equal students:\n  {}".format(", ".join(top_students)))



#def main():
    #"""The main function (see module docstring)"""
    #filename = get_filename()
    #data = read_data(filename)
    #stats = statistics(data)
    #print_results(stats)

#main()
def case_converter(filename):
   """ MAKE EVERYTHING UPPERCASE"""
   result_file = "data1.txt"
   with open(filename, 'r') as inp:
      y = inp.read().upper()
   with open(result_file, 'w') as out:
      out.write(y)
   return result_file
      
def write_reversed_file(input_filename, output_filename):
    """ REVERSE ORDER OF LINES"""
    s = ""
    file = open(input_filename, "r")
    #lines = file.read().rstrip()
    
    
    lines = file.read().split("\n")
    
    file.close()
    print(lines)
    for line in reversed(lines):
        s += line.rstrip() + "\n"
    file = open(output_filename, "w")
    file.write(s)
    file.close()