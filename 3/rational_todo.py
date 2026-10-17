# rational.py

"""
Module for performing arithmetic operations for rational numbers.

To run the module, user needs to supply three named parameters:
1. op stands for the operation:
    add for addition
    sub for subtraction
    mul for multiplication
    div for division
2. x stands for the first operand
3. y stands for the second operand

x and y must be enclosed in paired parentheses.

For example:

>>> run rational.py --op add --x (2/3) --y (-70/40)
-13/12
>>> run rational.py --op sub --x (-20/3) --y (120/470)
-976/141
>>> run rational.py --op mul --x (-6/19) --y (-114/18)
2/1
>>> run rational.py --op div --x (-6/19) --y (-114/-28)
-28/361
"""

import sys, math

### TODO 1: 补全测试函数以利用上述测试用例来测试结果 ###
def test_all_functions():  

### TODO 1 结束 ###

def gcd(a, b):  
    while a != b:
        if a > b:
            a -= b
        else:
            b -= a
    return a

### TODO 2: 补全 reduce 函数以对有理数 [n, d] 进行约分
def reduce(n, d): 

### TODO 2 结束 ###

### TODO 3: 补全有理数的四则运算 ###
### ==============================

def add(x, y):  

def sub(x, y):  

def mul(x, y):  

def div(x, y):  

### ==============================
### TODO 3 结束 ###

### TODO 4: 补全 output 和 get_rational
### output: 输入为列表形式 x=[n,d]，直接打印在终端上；
### get_rational: 输入为用户输入的字符串，输出为其有理数形式 [n,d]
### ==============================

def output(x):  

def get_rational(s):  

### ==============================
### TODO 4 结束 ###

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print(__doc__)
    elif len(sys.argv) == 2 and sys.argv[1] == '-h':
        print(__doc__)
    elif len(sys.argv) == 2 and sys.argv[1] == 'test':
        test_all_functions()
    else:
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument('--op', type=str)
        parser.add_argument('--x', type=str)
        parser.add_argument('--y', type=str)
        args = parser.parse_args()
        op = args.op
        x = get_rational(args.x); y = get_rational(args.y)
        f = {'add':add, 'sub':sub, 'mul':mul, 'div':div}
        output(f[op](x, y))