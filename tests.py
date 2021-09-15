import unittest
import os
import random
from cli import compress, decompress


class MyTestCase(unittest.TestCase):
    def test_empty_file(self):
        self.assertTrue(is_run_correct_without_password("test1"))
        self.assertTrue(is_run_correct_with_password("test1", "asd", "asd"))

    def test_a(self):
        self.assertTrue(is_run_correct_without_password("test2"))
        self.assertTrue(is_run_correct_with_password("test2", "asd", "asd"))
        self.assertFalse(is_run_correct_with_password("test2", "asd", get_random_passeword()))

    def test_10a(self):
        self.assertTrue(is_run_correct_without_password("test3"))
        self.assertTrue(is_run_correct_with_password("test3", "a1sdy", "a1sdy"))
        self.assertFalse(is_run_correct_with_password("test3", "a1sdy", get_random_passeword()))

    def test_100a(self):
        self.assertTrue(is_run_correct_without_password("test4"))
        self.assertTrue(is_run_correct_with_password("test4", "adfsdy", "adfsdy"))
        self.assertFalse(is_run_correct_with_password("test4", "adfsdy", get_random_passeword()))

    def test_1000a(self):
        self.assertTrue(is_run_correct_without_password("test5"))
        self.assertTrue(is_run_correct_with_password("test5", "ffadfsdy", "ffadfsdy"))
        self.assertFalse(is_run_correct_with_password("test5", "ffadfsdy", get_random_passeword()))

    def test_10000a(self):
        self.assertTrue(is_run_correct_without_password("test6"))
        self.assertTrue(is_run_correct_with_password("test6", "f90fadfsdy", "f90fadfsdy"))
        self.assertFalse(is_run_correct_with_password("test6", "f90fadfsdy", get_random_passeword()))

    def test_random_text(self):
        for i in range(7, 18):
            self.assertTrue(is_run_correct_without_password("test" + str(i)))
            self.assertTrue(
                is_run_correct_with_password("test" + str(i), "f9&0fadfsdy" + str(i), "f9&0fadfsdy" + str(i)))
            self.assertFalse(
                is_run_correct_with_password("test" + str(i), "f9&0fadfsdy" + str(i), get_random_passeword()))


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


def get_random_passeword():
    length = random.randint(5, 15)
    data = ""
    for i in range(length):
        data += chr(random.randint(ord("A"), ord("z")))
    return data


if __name__ == '__main__':
    unittest.main()
