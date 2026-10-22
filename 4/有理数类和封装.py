'''有理数类和封装
该实验计划考察类的定义、初始化函数的编写、类方法函数的编写、多态。
将上一个基础实验中实现的有理数表示与运算封装成一个类。参考代码已经给出了类的框架，并给出了
相应的测试代码。要求补全其中的重写运算方法，使得 Rational 类成为有自己运算与读取方式的一个
类型。
参考代码如下'''
# rational_def.py
def gcd(a, b):
    while a != b:
        if a > b:
            a -= b
        else:
            b -= a
    return a
    
class Rational:
    def __init__(self, n=0, d=1):
        _nu = n; _de = d
        self.__dict__['nu'] = _nu; self.__dict__['de'] = _de
    def __setattr__(self, name, value):
        raise TypeError('Error: Rational objects are immutable')
    def __str__(self): return '%d/%d' % (self.nu, self.de)
    def __add__(self, other): # addition
        n = self.nu * other.de + other.nu * self.de
        d = self.de * other.de
        g = gcd(abs(n), abs(d))
        return Rational(n // g, d // g)
    def __sub__(self, other): # subtraction
        n = self.nu * other.de - other.nu * self.de
        d = self.de * other.de
        g = gcd(abs(n), abs(d))
        return Rational(n // g, d // g)
    def __mul__(self, other): # multiplication
        n = self.nu * other.nu
        d = self.de * other.de
        g = gcd(abs(n), abs(d))
        return Rational(n // g, d // g)
    def __truediv__(self, other): # true division
        n = self.nu * other.de
        d = self.de * other.nu
        g = gcd(abs(n), abs(d))
        return Rational(n // g, d // g)
    def __eq__(self, other): # equal
        return self.nu * other.de == other.nu * self.de
    def __ne__(self, other): # not equal
        return self.nu * other.de != other.nu * self.de
    def __gt__(self, other): # greater than
        return self.nu * other.de > other.nu * self.de
    def __lt__(self, other): # less than
        return self.nu * other.de < other.nu * self.de
    def __ge__(self, other): # greater or equal
        return self.nu * other.de >= other.nu * self.de
    def __le__(self, other): # less or equal
        return self.nu * other.de <= other.nu * self.de

def test():
    testsuite = [
    ('Rational(2, 3) + Rational(-70, 40)',
    Rational(-13, 12)),
    ('Rational(-20, 3) - Rational(120, 470)',
    Rational(-976,141)),
    ('Rational(-6, 19) * Rational(-114, 18)',
    Rational(2, 1)),
    ('Rational(-6, 19) / Rational(-114, -28)',
    Rational(-28,361)),
    ('Rational(-6, 19) == Rational(-14, 41)', False),
    ('Rational(-6, 19) != Rational(-14, 41)', True),
    ('Rational(6, -19) > Rational(14, -41)', True),
    ('Rational(-6, 19) < Rational(-14, 41)', False),
    ('Rational(-6, 19) >= Rational(-14, 41)', True),
    ('Rational(6, -19) <= Rational(14, -41)', False),
    ('Rational(-15, 8) == Rational(120, -64)', True),
    ('Rational(-15, 8) != Rational(120, -64)', False),
    ('Rational(-15, 8) > Rational(120, -64)', False),
    ('Rational(-15, 8) < Rational(120, -64)', False),
    ('Rational(-15, 8) >= Rational(120, -64)', True),
    ('Rational(-15, 8) <= Rational(120, -64)', True)
    ]
    
    for t in testsuite:
        try:
            result = eval(t[0])
        except:
            print('Error in evaluating ' + t[0])
            continue
        if result != t[1]:
            print('Error: %s != %s' % (t[0], t[1]))
if __name__ == '__main__':
    test()
