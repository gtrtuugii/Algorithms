def record_check(age, gender, location):
    """ ABOVE 18 MALE PERTH OR SYD"""
    if age > 18 and gender == "M" and (location == "Perth" or location == "Sydney"):
        return "Found him!"
    return "Did not find him."

def should_shutdown(battery_level, time_on):
    """ SHOUD IT SHUT DOWN?"""
    result = False
    if time_on < 60 and battery_level < 4.7:
        result = True
    elif time_on >= 60 and battery_level < 4.8:
        result = True
    else:
        result = False
    return result 

def thing(i, j):
    """Does something silly"""
    return 10 < i < 20 and j >= 5

def balance_list(items):
    """ ADJUST LIST IF ODD"""
    if not len(items) % 2 == 0:
        items.append(items[-1])
    return items

def are_anagrams(word1, word2):
    """ ARE THEY ANAGRAMS?"""
    wo1 = list(word1)
    wo2 = list(word2)
    wo1.sort()
    wo2.sort()
      
    if word1 == word2:
        return False
    elif wo1 == wo2:
        return True
    else:
        return False

def locate_person(age_list, name_list, age, name):
    """ LOCATE PERSON WITH GIVEN NAME AND AGE IN LIST"""
    indexofperson = 0
    if age in age_list and name in name_list:
        indexofperson = name_list.index(name)
    return indexofperson


    
def format_listss(items):
    """ FORMAT ITEMS IN LIST"""
    if len(items) == 1:
        return items[0]
    elif len(items) == 2:
        text = "{word0:10} - {word1:}"
        return text.format(word0 = items[0], word1 = items[1])
    else:
        print("Invalid input!")
        
def format_list(items):
    """ FORMAT ITEMS IN LIST"""
    if len(items) == 1:
        return items[0]
    elif len(items) == 2:
        text = "{:<10}-{:>10}"
    return text.format(items[0], items[1])
        
def check_temperature(temperature, limit):
    """ TEMP IS CEL AND LIMITS IS FAHREN"""
    #fahrenheit = celsius x 9 / 5 + 32
    limit = (limit - 32) * 5 / 9
    if limit > temperature:
        return True
    return False

def can_jump(speed, power, name, injured):
    """ DISTANCE ATHLETE CAN JUMP"""
    if injured is False:
        distance = speed * power
    elif injured is True:
        distance = 0.8 * speed * power
    if distance < 1:
        text = "{} made a false attempt!".format(name)
    else:
        text = "{} can jump {:.2f}m!".format(name,distance)
    return text

def compare_strings(string1, string2):
    """ COMPARE STRING BASED ON FIRST OR LAST LETTER"""
    result = ""
    string1list = list(string1)
    string2list = list(string2)
    
    if string1list[0] == string2list[0]:
        if len(string1) == len(string2):
            result = "error"
        elif len(string1) > len(string2):
            result = string1
        elif len(string1) < len(string2):
            result = string2
    elif string1list[0] != string2list[0]:
        if string1list[-1] == string2list[-1]:
            result = "error"
        elif string1list[-1] > string2list[-1]:
            result = string1
        elif string1list[-1] < string2list[-1]:
            result = string2
    return result
        

           
           