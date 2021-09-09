import hashlib
import os.path

from node import Node
from priority_queue import PriorityQueue


class Huffman:
    def compress_file(self, data_filename, archive_filename):
        head, tail = os.path.split(data_filename)
        with open(data_filename, "rb") as data_file:
            data = data_file.read()
            archive = self.compress_file_bytes(data, tail)
        with open(archive_filename, "wb") as a:
            a.write(bytearray(archive))

    def decompress_file(self, archive_filename):
        head, tail = os.path.split(archive_filename)
        with open(archive_filename, "rb") as archive_file:
            archive_data = archive_file.read()
            data, file_correct, file_name = self.decompress_file_bytes(archive_data)
        if file_correct:
            with open(os.path.join(head, file_name), "wb") as a:
                a.write(bytearray(data))
        else:
            print("File is damaged")

    def decompress_file_bytes(self, archive_data):
        data_length, next_index, frequencies = self.parse_header(archive_data)
        next_index, hash_string = self.parse_hash(archive_data, next_index)
        root = self.create_huffman_tree(frequencies)
        next_index, file_name = self.parse_file_name(archive_data, next_index)
        data = self.decompress(archive_data, next_index, data_length, root)
        file_correct = self.check_integrity(hash_string, data)
        return data, file_correct, file_name

    @staticmethod
    def check_integrity(hash_string, data):
        hash_object = hashlib.md5(bytearray(data))
        hash_data = hash_object.digest()
        return list(hash_data) == hash_string

    @staticmethod
    def decompress(arch, start_index, data_length, root):
        size = 0
        curr = root
        data = []
        for i in range(start_index, len(arch)):
            bit = 1
            while bit <= 128:
                if (arch[i] & bit) == 0:
                    curr = curr.bit0
                else:
                    curr = curr.bit1
                if curr.bit0 is not None:
                    bit <<= 1
                    continue
                if size < data_length:
                    data.append(curr.symbol)
                size += 1
                curr = root
                bit <<= 1
        return data

    @staticmethod
    def parse_header(archive):
        data_length = archive[0] | (archive[1] << 8) | (archive[2] << 16) | (archive[3] << 24)
        frequencies = [0] * 256
        for i in range(256):
            frequencies[i] = archive[4 + i]
        start_index = 4 + 256
        return data_length, start_index, frequencies

    @staticmethod
    def parse_hash(archive, start_index):
        hash_string = []
        for i in range(16):
            hash_string.append(archive[start_index + i])
        return start_index + 16, hash_string

    @staticmethod
    def parse_file_name(archive, start_index):
        file_name = []
        for i in range(archive[start_index]):
            file_name.append(archive[start_index + 1 + i])
        name = bytearray(file_name).decode("UTF-8")
        return start_index + 1 + archive[start_index], name

    def compress_file_bytes(self, data, file_name):
        hash_object = hashlib.md5(data)
        hash_string = hash_object.digest()
        frequencies = self.calculate_freq(data)

        root = self.create_huffman_tree(frequencies)
        codes = self.create_huffman_code(root)
        bits = self.compress(data, codes)
        head = self.create_header(len(data), frequencies)
        return head + list(hash_string) + [len(file_name)] + list(file_name.encode("UTF-8")) + bits

    @staticmethod
    def create_header(data_length, frequencies):
        head = [data_length & 255, (data_length >> 8) & 255, (data_length >> 16) & 255, (data_length >> 24) & 255]
        for i in range(256):
            head.append(frequencies[i])
        return head

    @staticmethod
    def compress(data, codes):
        bits = []
        summa = 0
        bit = 1
        for symbol in data:
            for c in codes[symbol]:
                if c == "1":
                    summa |= bit
                if bit < 128:
                    bit = bit << 1
                else:
                    bits.append(summa)
                    summa = 0
                    bit = 1
        if bit > 1:
            bits.append(summa)
        return bits

    def create_huffman_code(self, root):
        codes = [None] * 256
        self.go_to_next_node(root, "", codes)
        return codes

    def go_to_next_node(self, node, code, codes):
        if node.bit0 is None:
            codes[node.symbol] = code
        else:
            self.go_to_next_node(node.bit0, code + "0", codes)
            self.go_to_next_node(node.bit1, code + "1", codes)

    def calculate_freq(self, data):
        frequencies = [0] * 256
        for byte in data:
            frequencies[byte] += 1
        self.normalize_frequencies(frequencies)
        return frequencies

    @staticmethod
    def normalize_frequencies(frequencies):
        max_item = max(frequencies)
        if max_item <= 255:
            return
        for i in range(256):
            if frequencies[i] > 0:
                frequencies[i] = 1 + frequencies[i] * 255 // (max_item + 1)

    @staticmethod
    def create_huffman_tree(frequencies):
        priority_queue = PriorityQueue()
        for i in range(256):
            if frequencies[i] > 0:
                priority_queue.enqueue(frequencies[i], Node(frequencies[i], symbol=i))
        while priority_queue.size > 1:
            bit0 = priority_queue.dequeue()
            bit1 = priority_queue.dequeue()
            freq = bit0.freq + bit1.freq
            next_node = Node(freq, bit0=bit0, bit1=bit1)
            priority_queue.enqueue(freq, next_node)
        return priority_queue.dequeue()
