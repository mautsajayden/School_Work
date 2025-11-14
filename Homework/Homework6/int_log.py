""" 
    File : int_log.py
    Author : Jayden Mautsa 
    Date : 10/31/2025
    Section : Homework 9
    E-mail : jmautsa1@umbc.edu
    Description : 
    """
    
def int_log(base, number):
    """
    :param base: the base of the logarithm
    :param number: the number we are taking the log of
    :return:  the anser to the log 
    """

    if number <= 1:
        return 0
    
    # keeps dividing by base and count
    return 1 + int_log(base, number // base)


if __name__ == '__main__':
    
     # ask user for base of log
    base = int(input("What is the base of the logarithm? "))
    
     # ask user for numbe
    num = int(input("What number are we taking the log of? "))
    
    print(int_log(base, num))