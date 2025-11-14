""" 
    File : str_equality.py
    Author : Jayden Mautsa 
    Date : 10/31/2025
    Section : Homework 9
    E-mail : jmautsa1@umbc.edu
    Description : 
    """
    

def string_equality(f_Word, s_Word):
    """
    :param f_Word: the first string
    :param s_Word: the second string
    :return: True if both strings match 
    """
    
    num_f = len(f_Word)
    num_s = len(s_Word)
    
    if ((num_f == 0) and (num_s == 0)):
        return True

    #checks length of the 2 strings
    if (num_f != num_s):
        return False
    
    #checks the first chararcter
    if (f_Word[0] != s_Word[0]):
        return False
    
    #checks the rest of the strings 
    return string_equality(f_Word[1:], s_Word[1:])


if __name__ == '__main__':
    
    # ask user for strings 
    first = input('Enter a first string: ')
    second = input('Enter a second string: ')
    
    while first != 'quit' and second != 'quit':
        
        print(string_equality(first, second))
        
        first = input('Enter a first string: ')
        second = input('Enter a second string: ')