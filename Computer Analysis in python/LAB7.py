##Q1:

#""" RETURN ZODIAC BY ENTERING NAME AND BDAY"""
#def zod():
    #""" SMTH"""
    #zodiac_signs = [
        #('Capricorn', 0, 1, 19, 1),
        #('Aquarius', 20, 1, 18, 2),
        #('Pisces', 19, 2, 20, 3),
        #('Aries', 21, 3, 19, 4),
        #('Taurus', 20, 4, 20, 5),
        #('Gemini', 21, 5, 20, 6),
        #('Cancer', 21, 6, 22, 7),
        #('Leo', 23, 7, 22, 8),
        #('Virgo', 23, 8, 22, 9),
        #('Libra', 23, 9, 22, 10),
        #('Scorpio', 23, 10, 21, 11),
        #('Sagittarius', 22, 11, 21, 12),
        #('Capricorn', 22, 12, 31, 12)]
    
    #name = input("What is your name? ")
    #dob = input("Enter your birthday in the form DD/MM e.g. 3/11: ")
    #day_string, month_string = dob.split('/')
    #day = int(day_string)
    #month = int(month_string)
    #for sign, day0, month0, day1, month1 in zodiac_signs:
        #if (month0, day0) <= (month, day) <= (month1, day1):
            #print("Hi {}, your Zodiac sign is {}.".format(name, sign))
##zod()

## *** YOUR CODE *** [Hint: only docstrings and imports can go at the start. 
## *** Only one of those two is relevant here. Which one?]
#""" COMPUTE PRICE IN MAIN"""

## *** YOUR CODE *** [Hint: only docstrings and imports can go at the start. 
## *** Only one of those two is relevant here. Which one?]
#""" COMPUTE PRICE IN MAIN"""

#def fun_function(n_items, cost_per_item, discount_percent, discount_threshold):
    ## *** YOUR CODE *** The body of fun_function goes here    
    #"""compute the total cost"""
    #cost = n_items * cost_per_item                  # line 1
    #if n_items > discount_threshold:                # line 2
        #cost = cost * (1 - discount_percent / 100)  # line 3
    #return cost
    
  


#def main():
    #"""RUN FUN FUNCTION"""
    ## *** YOUR CODE ***The body of the main function    # Get the number of items in this delivery
    #n_items = int(input("How many items? "))
    
     ## First initialise all variables
     
    #cost_per_item = 27      # Without discount
    #discount_percent = 10
    #discount_threshold = 20
    ## Now compute the total cost
    #fun_function(n_items, cost_per_item, discount_percent, discount_threshold)
    #cost = fun_function(n_items, cost_per_item, discount_percent, discount_threshold)
    #print('{} items cost ${:.2f}'.format(n_items, cost))
    
#main()

#"""Program to demonstrate extracting of an arbitrary block of
    #code as a separate function. This version has the function returning
    #a tuple rather than a single value."""

#def fun_function(items_per_pack, packs_per_carton, n_cartons):
    #"""Return n_items and total weight given a number of items per pack,
    #the number of packs per carton and the number of cartons. Each item
    #is assumed to weigh 100 grams."""

    ## ????? What goes here ?????
    #n_packs = n_cartons * packs_per_carton  # line 1
    #n_items = n_packs * items_per_pack      # line 2
    #weight = n_items * 100                  # line 3
    #return n_items, weight


#def main():
    #"""Every home should have one"""
    #items_per_pack = 6
    #packs_per_carton = 20
    #n_cartons = 5
    #n_items, weight = fun_function(items_per_pack, packs_per_carton, n_cartons)
    #print('{0} cartons'.format(n_cartons))
    #print('{0} items'.format(n_items))
    #print('{0} grams'.format(weight))
    
#main()
#import math
#"""Print all the perfect squares from zero up to a given maximum.
   #This version is refactored to make it more understandable
   #and more maintainable."""

#def read_bound(msg):
    #"""Reads the upper and lower bound from the standard input (keyboard).
       #If the user enters something that is not a positive integer
       #the function issues an error message and retries
       #repeatedly"""
    
    ## WHAT GOES HERE?
    #upper_bound = None
    #while upper_bound is None:
        #line = input(msg)
        #if line.isnumeric():
            #upper_bound = int(line)
        #else:
            #print("You must enter a positive number.")  
    #return upper_bound
    
    


#def is_perfect_square(num):
    #"""
    #Return true if and only if num is a perfect square
    #"""
    #root = math.sqrt(num)
    #return int(root) - root == 0
    

#def calculate_squares(lower_bound, upper_bound):
    #return filter(is_perfect_square, range(lower_bound, upper_bound))

#def print_squares(lower_bound, upper_bound, squares):
    #"""
    #Print a given list of all the squares up to a given upper bound
    #"""
    #print("The perfect squares between {} and {} are: ". format(lower_bound, upper_bound))
    #for square in squares:
        #print(square, end=' ')
    #print()  

    

#def main():
    #"""Every home should have one"""
    #lower_bound = read_bound("Enter the lower bound: ")
    #upper_bound = read_bound("Enter the upper bound: ")
    
    #squares = []
    #for num in range(lower_bound, upper_bound + 1):
        #if is_perfect_square(num):
            #squares.append(num)
    
    #print_squares(lower_bound, upper_bound,
                  #calculate_squares(lower_bound, upper_bound + 1))


#main()

#"""Test area module"""
#import area

#def main():
    #"""Main program calls each method of the area module"""
    #print(area.triangle_area(10.0, 7.0))  # Should print 35.0
    #print(area.rectangle_area(9.0, 7.0))  # Should print 63.0

#main()

#def print_gymnastic_score(mark_gained, *args):
    
    #if not args:
        #maximum = 40
    #else:
        #maximum = args[0]
    #perc = 100 * mark_gained / maximum
    #perc = float(perc)
    
    #text = "Your score: {:.1f}/{:.1f} ({:.1f}%)".format(mark_gained, maximum, perc)
    #print(text)
    

#def describe(**kwargs):
    #""" DEFINE SMTH (UNKNOWN NUMBER OF VAR)"""
    #if not kwargs:
        #name = "unknown"
        #species = "unknown"
        #age = "unknown"
    
        
    #print(text = "{} is a {}, age: {}.".format(kwargs))

#def main():
    #"""Test the describe function """
    #describe(name='Angus', species='chipmunk')
    #print(30 * '=')
    #describe(species='human', name='Marina')
    #print(30 * '=')
    #describe(age='17')
    #print(30 * '=')
    #describe('Peter', 'penguin', 10)

#main()

#def file_size(filename):
    #"""counts number of characters in file"""
    #file = open(filename, 'r')
    
    #for line in file:
        #result = len(line)
    #file.close()
    #return result

#def file_size(filename):
    #"""counts number of characters in file"""
    #with open(filename, 'r') as file:
    	#filename = file.read()
    	#len_chars = sum(len(word) for word in filename)
    #return len_chars

#def get_stats (filename):
    #""" """
    #result = 0
    #maxs = 0.0
    #with open(filename, 'w') as file:
	#filename = file.read
	#for num in filename:
	    #if num > filename[num+1]
	    #maxs  = num
	#for num in filename:
	    #if num > filename[num+1]
	    #mins  = num
    	#for num in filename:
	    #result += num
	#average = result / len(filename)
	#return maxs, mins, filename
	
