""" 
    File : derangements.py
    Author : Jayden Mautsa 
    Date : 10/31/2025
    Section : Homework 9
    E-mail : jmautsa1@umbc.edu
    Description : 
    """
    
num1 = 1
num2 = -1

def derangement(n):
    """
    :param n: number to find derangement for
    :return: the derangement 
    """
    
    if n == 0:
        return n
    
     # derangement formula 
    return n * derangement(n - num1) + ((num2) ** n)

if __name__ == '__main__':
    
    for i in range(20):
        print(i, derangement(i))