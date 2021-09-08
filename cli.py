import os
import sys

from huffman import Huffman

HELP_STRING = \
    """\
    Программа для архивироания и разархивирования файлов, используя алгорит Хаффмана.
    USAGE:
        main.py -c, --compress   [path] {archive_name}
        main.py -d, --decompress [path]
        main.py -h, --help
    
    Examples:
        main.py -c abc/my_file.txt
        main.py -c abc/my_file.txt my_archived_file.huf
    
        main.py -d my_archived_file.huf
    """


def start():
    command_line_arguments = sys.argv
    if len(command_line_arguments) < 2:
        print("Введите аргументы для начала работы")

    elif command_line_arguments[1] == "-h" or command_line_arguments[1] == "--help":
        help()

    elif command_line_arguments[1] == "-c" or command_line_arguments[1] == "--compress":
        if len(command_line_arguments) < 3:
            print("Введите путь к файлу")
        elif len(command_line_arguments) == 3:
            compress(command_line_arguments[2])
        else:
            compress(command_line_arguments[2], command_line_arguments[3])

    elif command_line_arguments[1] == "-d" or command_line_arguments[1] == "--decompress":
        if len(command_line_arguments) < 3:
            print("Введите путь к архиву")
        elif len(command_line_arguments) == 3:
            decompress(command_line_arguments[2])
    else:
        print("Неправильный формат ввода")


def help():
    print(HELP_STRING)


def compress(path, file_name=None):
    if is_path_correct(path):
        huffman = Huffman()
        if file_name is None:
            huffman.compress_file(path, path + ".huf")
        else:
            head, end = os.path.split(path)
            huffman.compress_file(path, os.path.join(head, file_name) + ".huf")
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
