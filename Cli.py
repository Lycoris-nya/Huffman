from Huffman import Huffman
import sys
import os


def start():
    command_line = sys.argv
    if len(command_line) < 2:
        print("Введите необходимые аргументы для начала работы")

    elif command_line[1] == "-h" or command_line[1] == "--help":
        help()

    elif command_line[1] == "-c" or command_line[1] == "--compress":
        if len(command_line) < 3:
            print("Введите путь к файлу с указанием имени файла")
        elif len(command_line) == 3:
            compress(command_line[2])
        else:
            compress(command_line[2], command_line[3])

    elif command_line[1] == "-d" or command_line[1] == "--decompress":
        if len(command_line) < 3:
            print("Введите путь к файлу с указанием имени файла")
        elif len(command_line) == 3:
            decompress(command_line[2])
    else:
        print("Неправильный формат ввода")


def help():
    print(
        "Архивирует или разархивирует указанный файл\nmain.py [--compress [path] [arh-name]]\nmain.py [--decompress [path]]")


def compress(path, file_name=None):
    if is_path_correct(path):
        huffman = Huffman()
        if file_name is None:
            huffman.compress_file(path, path + ".huf")
        else:
            head, end = os.path.split(path)
            huffman.compress_file(path, head + file_name + ".huf")
    else:
        print("Путь указан неверно")


def decompress(path):
    if is_path_correct(path):
        huffman = Huffman()
        huffman.decompress_file(path)
    else:
        print("Путь указан неверно")


def is_path_correct(path):
    return os.path.isfile(path)
