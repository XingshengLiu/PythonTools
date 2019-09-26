# @File  : testcount.py
# @Author: LiuXingsheng
# @Date  : 2018/7/21
# @Desc  : 通过unittest测试框架测试count

import unittest
from count import Calculator


class Counttest(unittest.TestCase):
    def setUp(self):
        self.cal = Calculator(8, 4)

    def tearDown(self):
        pass

    def test_sub(self):
        result = self.cal.sub()
        self.assertEqual(result, 4)

    def test_add(self):
        result = self.cal.add()
        self.assertEqual(result, 12)

    def test_mul(self):
        result = self.cal.mul()
        self.assertEqual(result, 32)

    def test_div(self):
        result = self.cal.div()
        self.assertEqual(result, 2)


if __name__ == '__main__':
    # main方法和下边注释打开之后的效果是一样的
    unittest.main()
    # 构造测试集
    # suite = unittest.TestSuite()
    # suite.addTest(Counttest('test_add'))
    # suite.addTest(Counttest('test_sub'))
    # suite.addTest(Counttest('test_mul'))
    # suite.addTest(Counttest('test_div'))
    # # 执行测试
    # runner = unittest.TextTestResult()
    # runner.run(suite)
