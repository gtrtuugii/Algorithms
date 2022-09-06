def word_swapper(sentence, word):
    """ Swap the given word in the sentence with 'ABC'."""
    default = "ABC"
    subwords = sentence.replace(word, default)
    return(subwords)

def find_word(sentence, word):
    """Find the given word within the sentence"""
    result = sentence.find(word)
    return result

def top_and_tail(string):
    """Remove the first and last letter of the String"""
    return string[1:-1]

def half_string(string):
    """ Return half of the string"""
    n = len(string)
    half = n // 2
    return string[:half]

def first_nth_string(string, n):
    """Return first n characters of string"""
    nth = n //1
    return string[:nth]

def print_vector(x_coord, y_coord):
    """ Print vectors using format"""
    s = "[x,y] = [{:.1f}, {:.1f}]".format(x_coord, y_coord)
    print(s)
    
def print_date(year, month, day):
    """ Print out the date, formatted as
            year.month.day
    """
    s = "{:1.0f}.{:1.0f}.{:1.0f}".format(year, month, day)
    print(s)
    
def insert_item(data, item, ind):
    """Print new list that contains item at index ind in data."""
    data.insert(ind, item)
    return data

def count_item(data, item):
    """ Return the number of times "item" appears in "data". """
    c = data.count(item)
    return c

def second(data):
    """Return second item in data"""
    return data[1]

def append_list_new(data1, data2):
    """ Add data2 to data1 with the order data1 , data2 without 
    referencing any items in the old lists"""
    data1.extend(data2)
    new_data = data1[:]
    return new_data

def append_lists(data1, data2):
    """ add data2 to data1, in the order data1, data2"""
    data1 = data1 + data2
    return data1

def almost_last(data):
    """Return second-last item in list"""
    return data[len(data)-2]

def remove(data):
    """ Remove second item in the list i.e index number 1"""
    del data[1]
    return data

def duplicate_last(data):
    """ Duplicate the list data with last item appearing twice"""
    new_data = data[:]
    new_data.append(data[-1])
    return new_data

def cubed_tuple(number):
    """ return the number with the number cubed"""
    number1 = int(number)
    tuple1 = (number1, (number1 ** 3))
    return tuple1

def num_words(string):
    """ Count the number of words in the string"""
    words = string.split()
    counts = len(words)
    return counts