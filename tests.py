import unittest
import os
from cli import compress, decompress

class MyTestCase(unittest.TestCase):
    def test_empty_file(self):
        self.assertTrue(is_run_correct_without_password("test1"))
        self.assertTrue(is_run_correct_with_password("test1", "asd", "asd"))

    def test_a(self):
        self.assertTrue(is_run_correct_without_password("test2"))
        self.assertTrue(is_run_correct_with_password("test2", "asd", "asd"))

    def test_10a(self):
        self.assertTrue(is_run_correct_without_password("test3"))

    def test_100a(self):
        self.assertTrue(is_run_correct_without_password("test4"))

    def test_1000a(self):
        self.assertTrue(is_run_correct_without_password("test5"))

    def test_10000a(self):
        self.assertTrue(is_run_correct_without_password("test6"))

    def test_random_text(self):
        for i in range(7, 18):
            self.assertTrue(is_run_correct_without_password("test" + str(i)))


def is_content_same(path1, path2):
    with open(path1, "rb") as data_file:
        data1 = data_file.read()
    with open(path2, "rb") as data_file:
        data2 = data_file.read()
    return data1 == data2


def is_run_correct_without_password(name):
    path = os.path.join("tests", name)
    compress(path)
    decompress(path + ".huf")
    return is_content_same(path, os.path.join("tests", name + "_copy"))


def is_run_correct_with_password(name, password1, password2):
    path = os.path.join("tests", name)
    compress(path, password=password1)
    decompress(path + ".huf", password=password2)
    return is_content_same(path, os.path.join("tests", name + "_copy"))


if __name__ == '__main__':
    unittest.main()
