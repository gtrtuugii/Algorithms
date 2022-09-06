#LAB 10
import numpy as np
#Q1
def numpy_extract(nplist, row):
    """ xxx"""
    return nplist[row]

#Q2

def numpy_ones(n):
    """ xxx"""
    result = np.ones([n, n])
    return result

#Q3

def numpyfied(numlist):
    """ xxx"""
    result = np.array(numlist)
    return result
#Q4

def numpy_slice(numlist, start, end, skip):
    """ xxx"""
    result = np.array(numlist)
    return result[start:end:skip]

#Q5
def odd_arrays(numlist):
    '''Xxx'''
    nums = np.array(numlist)
    new_list = nums[1::2]
    print(new_list)
    
#Q6

def reshaped_by_row(nums, row):
    '''Xxx'''
    num_list = np.array(nums)
    column = int(len(nums) / row)
    if len(nums) % row == 0:
        reshaped_nums = np.reshape(num_list, (row, column))
    else:
        reshaped_nums = None
    return reshaped_nums

#Q7

def squared(numlist):
    """Xxx"""
    
    res = np.array(numlist)
    res = res ** 2
    return res

#Q8

def correct_rainfall(rainfall, day, correction):
    """Xxx"""
    data = np.array(rainfall)
    for row in data:
        row[day] += correction
        
    return data

#Q9

