import os
import sys

from huffman import Huffman

HELP_STRING = \
    """\
    Программа для архивироания и разархивирования файлов, используя алгорит Хаффмана.
    USAGE:
        main.py -c, --compress   [path] {archive_name} (-p password)
        main.py -d, --decompress [path] (-p password)
        main.py -h, --help
    
    Examples:
        main.py -c abc/my_file.txt
        main.py -c abc/my_file.txt my_archived_file.huf
        
        main.py -c abc/my_file.txt my_archived_file.huf -p my_password
    
        main.py -d my_archived_file.huf
        main.py -d my_archived_file.huf -p my_password
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
        elif len(command_line_arguments) > 3:
            if command_line_arguments[3] == "-p":
                if len(command_line_arguments) == 4:
                    print("Введите пароль")
                else:
                    compress(command_line_arguments[2], password=command_line_arguments[4])
        else:
            compress(command_line_arguments[2], command_line_arguments[3])

    elif command_line_arguments[1] == "-d" or command_line_arguments[1] == "--decompress":
        if len(command_line_arguments) < 3:
            print("Введите путь к архиву")
        elif len(command_line_arguments) == 3:
            decompress(command_line_arguments[2])
        elif len(command_line_arguments) > 3:
            if command_line_arguments[3] == "-p":
                if len(command_line_arguments) == 4:
                    print("Введите пароль")
                else:
                    decompress(command_line_arguments[2], password=command_line_arguments[4])

    else:
        print("Неправильный формат ввода")


def help():
    print(HELP_STRING)


def compress(path, file_name=None, password=None):
    if is_path_correct(path):
        huffman = Huffman()
        archive_name = ""
        if file_name is None:
            archive_name = path + ".huf"
        else:
            head, end = os.path.split(path)
            archive_name = os.path.join(head, file_name) + ".huf"
        if password is None:
            huffman.compress_file(path, archive_name)
        else:
            huffman.compress_file_with_password(path, archive_name, password)
    else:
        print("Путь указан неверно")


def decompress(path, password=None):
    if is_path_correct(path):
        huffman = Huffman()
        if password is None:
            huffman.decompress_file(path)
        else:
            huffman.decompress_file_with_password(path, password)
    else:
        print("Путь указан неверно")


def is_path_correct(path):
    return os.path.isfile(path)
