# test_rational.py
# Start of TODO 1
# TODO: 从 rational_module 中导入 Rational 类
from rational import Rational
# End of TODO 1

def test_rational():
    # Start of TODO 2
    # TODO: 通过类实例化定义计算数并进行计算，参照实验二
    result = Rational(666,999) + Rational(233,114) *  Rational(233,514) - Rational(787878,1000000) 
    # End of TODO 2
    solution = Rational(5898312589, 7324500000)
    print(f"> Your RESULT is: {result}")
    print(f"> The SOLUTION is: {solution}")
    if (result == solution):
        print("Correct! Congratulations! ^o^")
    else:
        print("Wrong... Try again! qwq")

if __name__ == "__main__":
    test_rational()
