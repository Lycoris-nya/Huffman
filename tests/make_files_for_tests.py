import random


def create_files(name, data):
    with open(name, "w+") as a:
        a.write(data)
    with open(name + "_copy", "w+") as a:
        a.write(data)


def make_random_test():
    length = random.randint(100, 10000)
    data = ""
    for i in range(length):
        data += chr(random.randint(ord("a"), ord("z")))
    return data


if __name__ == "__main__":
    create_files("test1", "")
    create_files("test2", "a")
    create_files("test3", "a" * 10)
    create_files("test4", "a" * 100)
    create_files("test5", "a" * 1000)
    create_files("test6", "a" * 10000)
    create_files("test6", "a" * 100000)
    for i in range(7, 18):
        name = "test" + str(i)
        create_files(name, make_random_test())
