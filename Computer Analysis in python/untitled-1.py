def is_even(number):
    """ Return True if the given number is even, False otherwise. """
    if number % 2 == 0:
        return True
    return False

def to_celsius(fahrenheit):
    """Return the given fahrenheit temperature in degrees celsius"""
    degrees_celsius = (fahrenheit - 32) * (5 / 9)
    return degrees_celsius

def to_fahrenheit(celsius):
    """Return the given celsius temperature in degrees fahrenheit"""
    fahrenheit = celsius * 9 / 5 + 32
    return fahrenheit


    