"""
File: hailstone.py
Author:
Date:
Section:
E-mail:
Description: This file contains python code that implements the "flight"
of a hailstone, following the HOTPO rules (also known as the Collatz
Conjecture), recursively
"""

# NO CONSTANTS NEEDED, THE NUMBERS USED IN flight() ARE
# PART OF A FORMULA/MATHEMATICAL CONJECTURE

def flight(height):
    """
    recursively calculates the path of a hailstone
    :param height: the height of the hailstone
    :return: a recursive call, which at the end returns the number
             of "steps" taken for the hailstone to reach a height of 1
    """
    # BASE CASES
    if height <= 0:
        print("Invalid input. Height must be a positive integer.")
        return 0
    if height == 1:
        return 0  # no more steps needed, already at ground

    # RECURSIVE CASES
    if height % 2 == 0:
        return 1 + flight(height // 2)
    else:
        return 1 + flight(height * 3 + 1)


if __name__ == "__main__":
    print("Welcome to the Hailstone Simulator!")
    msg = "Please enter a height for the hailstone to start at: "
    start_height = int(input(msg))

    steps = flight(start_height)  # recursive call goes here

    print("\nIt took", steps, "steps to hit the ground.")
    print("Thank you for using the Hailstone Simulator!\n")
