"""
File:    lab.py
Author:  Jayden Mautsa
Date:    10/30/2025
Section: 36
E-mail:  jmautsa1@umbc.edu
Description: its creating a 2d list 
"""


def create_new_weird_2d_list(height, width, value):
    """
    Creates a 2d list where all values are initialized to the supplied value
    :param height: the amount of sublists
    :param width: the size of each sublist
    :param value: the value to initialize each item in the list
    :return: a 2d list
    """
    row = []
    mat = []

    for i in range(width):
        row.append(value)

    for i in range(height):
        mat.append(row)

    return mat


def create_new_not_weird_2d_list(height, width, value):
    """
    Creates a 2d list where all values are initialized to the supplied value
    :param height: the amount of sublists
    :param width: the size of each sublist
    :param value: the value to initialize each item in the list
    :return: a 2d list
    """
    # hint hint hint: make two nested for loops that utilize range()
    
    mat = []
    
    for i in range(height):          
        row = []
        
        for j in range(width):       
            row.append(value)  
                  
        mat.append(row)              
        
    return mat


if __name__ == '__main__':
    matrix = create_new_weird_2d_list(4, 4, 0)
    matrix[0][1] = 1
    matrix[2][3] = 2
    print(matrix)
    # I'm expecting [[0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 2], [0, 0, 0, 0]]
    
    # but what do I get..[0, 1, 0, 2], [0, 1, 0, 2], [0, 1, 0, 2], [0, 1, 0, 2].?

    matrix = create_new_not_weird_2d_list(4, 4, 0)
    matrix[0][1] = 1
    matrix[2][3] = 2
    print(matrix)