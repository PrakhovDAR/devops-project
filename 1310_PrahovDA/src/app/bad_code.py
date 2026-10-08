import os
import sys

x = 10

INTENTIONALLY_VERY_LONG_LINE_NAME = "This string literal is deliberately crafted to exceed one hundred characters in total line length"

def calculate(a_var, b_var, unused_param):
    result = 42
    return a_var + b_var

def calculate_redefined(value):
    pass
def calculate_redefined():
    pass

class SimpleClass:
    def only_method(self):
        return self

def test_shadow():
    x = 20
    return x
