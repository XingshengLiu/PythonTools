# @File  : structure.py
# @Author: LiuXingsheng
# @Date  : 2018/7/31
# @Desc  : 数据结构和算法
p = (4, 5)
x, y = p
print(x)
print(y)

data = ['ACME', 50, 91.1, (2012, 12, 21)]
# name, shares, price, date = data
# print(name)
# print(date)
name, shares, price, (year, month, day) = data
print(year, month, day)
print("hello %s" % "wrold")
name_lxs = 'lxs'
print("Hi,%s you have $%d" % (name_lxs, 1000))
print("rate %d%%" % 7)

test = []
if test:
    print("True")
else:
    print("False")
# BMI = int(input("请输入bmi指数：\n"))
# if BMI > 32:
#     print("严重肥胖")
# elif 28 < BMI < 32:
#     print("肥胖")
# elif 25 < BMI < 28:
#     print("过重")
# elif 18.5 < BMI < 25:
#     print("正常")
# else:
#     print("过轻")

d = {'Michine': 95, 'Bob': 85, 'Tracy': 85}
print("content is %s" % d['Michine'])
print('tomas is exist ? %s' % d.get('tomas'))

print(abs(-100))


def test(x):
    x = 10
    if not isinstance(x, (int, float)):
        raise TypeError('bad operand type')
    if x >= 0:
        return 1, 2, 3
    else:
        return 4, 5, 6


def move(n, a, b, c):
    if n == 1:
        print(a, '-->', c)
    else:
        move(n - 1, a, c, b)
        move(1, a, b, c)
        move(n - 1, b, a, c)


def iter():
    d = {'a': '1', 'b': '2', 'c': 3}
    for key, value in d.items():
        print(key, value)


def lower():
    L = ['Hello', 'World', 'IBM', 'Apple']
    print([s.lower() for s in L])


def odd():
    print('step 1')
    yield 1
    print('step 2')
    yield (3)
    print('step 3')
    yield (5)


def fib(max):
    n, a, b = 0, 0, 1
    while n < max:
        yield b
        a, b = b, a + b
        n = n + 1
    return 'done'


def is_odd(n):
    return n % 2 == 1


def _odd_iter():
    n = 1
    while True:
        n = n + 2
        yield n


def _not_divisible(n):
    return lambda x: x % n > 0


def primes():
    yield 2
    it = _odd_iter()
    while True:
        n = next(it)
        yield n
        it = filter(_not_divisible(n), it)


def test_1():
    for n in primes():
        if n < 1000:
            print(n)
        else:
            break


def buid(x, y):
    return lambda: x * x + y * y


def log(func):
    def wrapper(*args, **kw):
        print('call %s():' % func.__name__)
        return func(*args, **kw)

    return wrapper


@log
def now():
    print('2015-3-5')


if __name__ == '__main__':
    list_test = [1, 2, 4, 5, 6, 9, 10, 15]
    print(list(filter(is_odd, list_test)))
    test_1()
    x = buid(1, 2)
    print(x())
    f = now
    print(now.__name__)
    print(f.__name__)
    now()


# o = fib(10)
# for i in o:
#     print(i)
class Employ(object):
    @property
    def select(self):
        return self._birth

    @select.setter
    def select(self, value):
        self.name = value
