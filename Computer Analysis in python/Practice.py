def print_3d_vector(x_coord, y_coord, z_coord):
    """ PRINT COORD"""
    print("[x,y,z] = [ {:.2f}, {:.2f}, {:.2f} ]".format(x_coord, y_coord, z_coord))
    
def append_list(data1, data2):
    """ APPEND DATA """
    #data1 = data1 + data2
    data1.extend(data2)
    return data1

def second(data):
    return data[1]
    
def dinner_calculator(meal_cost, drinks_cost, coupon):
    discount = 0.30
    GST = 1.1
    
    if coupon == True:
        if (drinks_cost * discount) < 5:
            total = (meal_cost * GST + drinks_cost * (1 - discount) * GST)
            total = total * 0.95
        elif (drinks_cost * discount) > 5:
            total = (meal_cost * GST + drinks_cost * GST * (1 - discount) )
    else:
        total = (meal_cost * GST + drinks_cost * GST)
    return round(total, 2)

def concat_long_words(s):
    """Returns a concatenation of all the words in s that are at least
        4 characters in length.
    """
    words = s.split()
    result = ''
    i = 0
    
    while i < len(words):
        word = words[i]
        if len(word) >= 4 or word.startswith("b"):
            result = result + word
        i += 1
    return result
    
def concat_long_word(s):
    """ """
    result = ""
    words = s.split()
    
    for word in words:
        if len(word) >= 4 or word.startswith("b"):
            result = result + word
    return result

def remove(index,data):
    """ REMOVE ITEM AT INDEX IN LIST"""
    del data[index]
    return data

def remove1(index, data):
    data.pop([index])
    return data
            
def similar(eng_sentence):
    """ HOW MANY WORDS ARE TRANSLATED"""

    dictionary = eng_sentence
    haj_sentence = translate(eng_sentence, dictionary, "", "english")
    
    eng = eng_sentence.split()
    haj = haj_sentence.split()
    count = 0
    for char in range(len(eng)):
        if eng[char] == haj[char]:
            count += 1
    return count
    