import unittest
from collections import Counter
from typing import Union
import math

def is_prime(n: int) -> bool:
    """
    Optimized algorithm to check if a number is prime with
    O(sqrt(n) complexity
    :param n : int
        number to check
    
    :return: bool
        true if the input number is prime, false otherwise
        
    Raises
    ------
    TypeError
        is raised when input is incorrect 
    """
    
    if not isinstance(n, int):
        raise TypeError('Incorrect input. Acceptable type is int')
    
    match n:
        case 1:
            return False
        case 2: 
            return True
        case _:
            for i in range(2, int(math.sqrt(n))+1):
                if (n%i) == 0:
                    return False
            return True


def solve_problem(a: Union[list[int], tuple[int]],
                  b: Union[list[int], tuple[int]]) -> list[int]:
    """
    Creates a sequence based on sequence A and sequence B
    given as input. The assumption was made to consider both
    lists and tuples as possible input types.

    :param a : list or tuple containing integers
        sequence A
    :param b : list or tuple containing integers
        sequence B
        
    :return: list generated according to input 

    Raises
    ------
    TypeError
        is raised when input is incorrect 
        
    """
    
    # look before you leap input validation
    if not isinstance(a, (list, tuple)) or not isinstance(b, (list, tuple)):
        raise TypeError('Incorrect input. Acceptable types are list and tuple')
    
    # Counter counts the occurences of each element in sequence b and stores the counts as 
    # dictionary values with corresponding elements as keys
    counter = Counter(b)
    
    """ debugging
    
    for value in counter.keys():
        print(f"Value: {value} Count: {counter[value]} Is prime: {is_prime(counter[value])}")
    """
    
    # using list comprehension to create the final sequence
    # 
    c = [element for element in a if not is_prime(counter[element]) or element not in counter.keys()]
        
    return c

class TestSolution(unittest.TestCase):
    
    def test_normal_input1(self):
        self.assertEqual(solve_problem(a=[2,3,9,2,5,1,3,7,10], b=[2,1,3,4,3,10,6,6,1,7,10,10,10]), [2,9,2,5,7,10])
    
    def test_normal_input2(self):
        self.assertEqual(solve_problem(a=(2,3,9,2,5,1,3,7,10), b=[2,1,3,4,3,10,6,6,1,7,10,10,10]), [2,9,2,5,7,10])
        
    def test_empty_input(self):
        self.assertEqual(solve_problem(a=[], b=[]), [])
        
    def test_exception1(self):
        with self.assertRaises(TypeError):
            solve_problem(a=1, b=[3])
            
    def test_exception2(self):
        with self.assertRaises(TypeError):
            solve_problem(a=[2,3], b=1)


if __name__ == "__main__":
    
    unittest.main()

    