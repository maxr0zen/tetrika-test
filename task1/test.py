from solution.solution import strict
import unittest

@strict
def sum_two(a: int, b: int,) -> int:
    return a + b

@strict
def div_two(a:int, b:int) -> int:
    if b == 0:
        raise ValueError(f'Cannot divide by 0')
    return a / b

@strict
def int_div_two(a:int, b:int) -> int:
    if b == 0:
        raise ValueError(f'Cannot divide by 0')
    return a // b

@strict
def join_tree(a:int, b, c:int) -> str:
    return f'{a}{b}{c}'


class StrictTest(unittest.TestCase):
    def test_params_annotation_mismatch(self):
        self.assertRaises(TypeError, sum_two, 1, 0.4)
        
        
    def test_params_annotation_match(self):
        try:
            sum_two(1, 1)
        except Exception as e:
            raise self.failureException(f'Unexpected exception raised {e}')
        
    
    def test_return_annotation_mismatch(self):
        self.assertRaises(TypeError, div_two, 2, 2)
    

    def test_return_annotation(self):
        try:
            int_div_two(1, 1)
        except Exception as e:
            raise self.failureException(f'Unexpected exception raised {e}')
    
    
    def test_semi_annotated_params(self):
        try:
            join_tree(1, True, 0)
        except Exception as e:
            raise self.failureException(f'Unexpected exception raised {e}')
    
    
        
        


if __name__ == '__main__':
    unittest.main()
