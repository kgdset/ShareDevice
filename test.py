import unittest
from unittest import TestCase
class BaseTestRecharge(unittest.TestCase):
    # 不放在__init__或者setup里面是为了在生成suite的时候就获取到env,这样后面即使有并行执行,可以各自执行不同的env。


    def setUp(self):
        pass

    def tearDown(self):
        pass
    def test_ddd(self):
        # case4:校验服务协议展示



