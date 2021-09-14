# Huffman
Архиватор Huffman c CLI интерфейсом
'''
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
'''
