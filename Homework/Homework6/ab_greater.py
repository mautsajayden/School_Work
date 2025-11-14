""" 
    File : ab_greater.py
    Author : Jayden Mautsa 
    Date : 10/31/2025
    Section : Homework 9
    E-mail : jmautsa1@umbc.edu
    Description : 
    """
    
def ab_greater(n, k=0, current=''):
    """
    
    :param n: length of the string
    :param k: keeps track of how many more a's than b's so far
    :param current: the new string
    :return:  just prints the valid strings
    """
    
    if n == 0:
        
        #prints if there are more a > b 
        if k > 0:
            print(current)
            
        return

    
    ab_greater(n - 1, k + 1, current + 'a')
    
    ab_greater(n - 1, k - 1, current + 'b')


if __name__ == '__main__':
    
    # ask the user for how long the string should be
    num = int(input("What length do you want to run? "))
    ab_greater(num)