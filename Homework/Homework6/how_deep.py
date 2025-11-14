""" 
    File : how_deep.py
    Author : Jayden Mautsa 
    Date : 10/31/2025
    Section : Homework 9
    E-mail : jmautsa1@umbc.edu
    Description : 
    """


def how_deep(list_struct):
    """
    :param list_struct: the list we are checking
    :return: a number of the deepest level
    """
    
     # if the list is empty = 1 level deep
    if not (list_struct): return 1
    
    max_depth = 0
    
    for sub_list in list_struct:
        
        list_depth = how_deep(sub_list)
        
         # change the depth if we found a deeper list
        if list_depth > max_depth:
            max_depth = list_depth
            
    return max_depth + 1


def main():
    
    # professor testing
    print(how_deep([[[], [], [], [[[]]]], []]))  
    print(how_deep([]))                          
    print(how_deep([[], []]))                    
    print(how_deep([[[]], [], [[]], [[[]]]]))    
    print(how_deep([[[[], [[]], [[[]]], [[[[]]]]]]]))  
    print(how_deep([[[], []], [], [[], []]]))    

if __name__ == '__main__':
    main()
  