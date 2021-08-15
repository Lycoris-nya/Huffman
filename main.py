from Huffman import Huffman
if __name__ == "__main__":
    huffman = Huffman()
    huffman.compress_file("Huffman.py", "Huffman.py.huf")
    huffman.decompress_file("Huffman.py.huf", "Huffman.py.huf.txt")
