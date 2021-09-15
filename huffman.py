import hashlib
import math
import os
import os.path
from datetime import datetime, timezone

from node import Node
from priority_queue import PriorityQueue


class Huffman:
    ACCESS = {0: "---", 1: "--x", 2: "-w-", 3: "-wx", 4: "r--", 5: "r-x", 6: "rw-", 7: "rwx"}

    def compress_file_with_password(self, data_filename, archive_filename, password):
        head, tail = os.path.split(data_filename)
        with open(data_filename, "rb") as data_file:
            data = data_file.read()
            hassh = hashlib.sha512(password.encode("UTF-8"))
            hash_digest = hassh.hexdigest().encode("UTF-8")
            new_data = bytearray()

            for i, byte in enumerate(data):
                new_data.append(byte ^ hash_digest[i % len(hash_digest)])

            archive = self.compress_file_bytes(new_data, tail, data_filename)
        with open(archive_filename, "wb") as a:
            a.write(bytearray(archive))

    def compress_file(self, data_filename, archive_filename):
        head, tail = os.path.split(data_filename)
        with open(data_filename, "rb") as data_file:
            data = data_file.read()
            archive = self.compress_file_bytes(data, tail, data_filename)
        with open(archive_filename, "wb") as a:
            a.write(bytearray(archive))

    def _decompress_file(self, archive_filename):
        head, tail = os.path.split(archive_filename)
        with open(archive_filename, "rb") as archive_file:
            archive_data = archive_file.read()
            data, file_correct, file_name = self.decompress_file_bytes(archive_data)
            return file_correct, file_name, bytearray(data)

    def decompress_file(self, archive_filename):
        head, tail = os.path.split(archive_filename)
        is_ok, file_name, data = self._decompress_file(archive_filename)
        if is_ok:
            with open(os.path.join(head, file_name), "wb") as a:
                a.write(data)
        else:
            print("Файл поврежден")

    def decompress_file_with_password(self, archive_filename, password):
        head, tail = os.path.split(archive_filename)
        is_ok, file_name, data = self._decompress_file(archive_filename)
        hash = hashlib.sha512(password.encode("UTF-8"))
        hash_digest = hash.hexdigest().encode("UTF-8")
        new_data = bytearray()

        for i, byte in enumerate(data):
            new_data.append(byte ^ hash_digest[i % len(hash_digest)])

        if is_ok:
            with open(os.path.join(head, file_name), "wb") as a:
                a.write(new_data)
        else:
            print("Файл поврежден")

    def decompress_file_bytes(self, archive_data):
        data_length, next_index, frequencies = self.parse_header(archive_data)
        next_index, hash_string = self.parse_hash(archive_data, next_index)
        next_index, file_name = self.parse_file_name(archive_data, next_index)
        next_index, metadata = self.decompress_metadata(archive_data, next_index)
        data = []
        if data_length > 0:
            root = self.create_huffman_tree(frequencies)
            data = self.decompress(archive_data, next_index, data_length, root)
        file_correct = self.check_integrity(hash_string, data)
        self.show_metadata(metadata)
        return data, file_correct, file_name

    def show_metadata(self, metadata):
        print(
            f"Size: {metadata['size']}\nDevice: {metadata['device']}\nLinks: {metadata['link']}\nAccess: {self.ACCESS[metadata['access'][0]]} {self.ACCESS[metadata['access'][1]]} {self.ACCESS[metadata['access'][2]]}\nUid: {metadata['uid']}\nGid: {metadata['gid']}\nAccess: {metadata['access_time']}\nModify: {metadata['modify_time']}\nChange: {metadata['change_time']}")

    def decompress_metadata(self, archive_data, index):
        metadata = dict()
        metadata["access"] = [archive_data[index], archive_data[index + 1], archive_data[index + 2]]
        metadata["link"] = archive_data[index + 3]
        metadata["size"] = archive_data[index + 4] | (archive_data[index + 5] << 8) | (
                archive_data[index + 6] << 16) | (archive_data[index + 7] << 24)
        metadata["uid"] = archive_data[index + 8] | (archive_data[index + 9] << 8) | (archive_data[index + 10] << 16)
        metadata["gid"] = archive_data[index + 11] | (archive_data[index + 12] << 8) | (archive_data[index + 13] << 16)
        index, metadata["access_time"] = self.decompress_time(archive_data, index + 14)
        index, metadata["modify_time"] = self.decompress_time(archive_data, index)
        index, metadata["change_time"] = self.decompress_time(archive_data, index)
        dev_len = archive_data[index]
        metadata["device"] = archive_data[index + 1]
        for i in range(1, dev_len):
            metadata["device"] = metadata["device"] | archive_data[index + 1 + i] << 8 * i
        return index + dev_len + 1, metadata

    def decompress_time(self, archive_data, index):
        year = archive_data[index] * 100 + archive_data[index + 1]
        data = datetime(year, archive_data[index + 2], archive_data[index + 3], hour=archive_data[index + 4],
                        minute=archive_data[index + 5], second=archive_data[index + 6], tzinfo=timezone.utc)
        return index + 7, data

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
                if root.bit0 is not None:
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

    def compress_file_bytes(self, data, file_name, full_name):
        hash_object = hashlib.md5(data)
        hash_string = hash_object.digest()

        frequencies = self.calculate_freq(data)
        if len(data)>0:
            root = self.create_huffman_tree(frequencies)
            codes = self.create_huffman_code(root)
            bits = self.compress(data, codes)
        else:
            bits = []

        head = self.create_header(len(data), frequencies)
        return head + list(hash_string) + [len(file_name)] + list(file_name.encode("UTF-8")) + self.get_metadata(
            full_name) + bits

    def get_metadata(self, full_name):
        statistics = os.stat(full_name)
        access = oct(statistics.st_mode)[-3:]
        links = [statistics.st_nlink]
        if (statistics.st_size > 2 ** 32):
            raise Exception("Файл слишком большой")
        size = [statistics.st_size & 255, (statistics.st_size >> 8) & 255, (statistics.st_size >> 16) & 255,
                (statistics.st_size >> 24) & 255]
        uid = [statistics.st_uid & 255, (statistics.st_uid >> 8) & 255, (statistics.st_uid >> 16) & 255]
        gid = [statistics.st_gid & 255, (statistics.st_gid >> 8) & 255, (statistics.st_gid >> 16) & 255]
        access_time = self.compress_time(statistics.st_atime)
        modify_time = self.compress_time(statistics.st_mtime)
        change_time = self.compress_time(statistics.st_ctime)
        dev_len, dev_commpress = self.commpress_dev(statistics.st_dev)
        return [int(access[0]), int(access[1]), int(
            access[2])] + links + size + uid + gid + access_time + modify_time + change_time + dev_len + dev_commpress

    def commpress_dev(self, dev):
        n = math.ceil(1 / 6 * math.log(dev, 2))
        res_dev = [dev & 255]
        for i in range(1, n):
            res_dev.append((dev >> 8 * i) & 255)
        return [n], res_dev

    def compress_time(self, time):
        data = datetime.fromtimestamp(time, tz=timezone.utc)
        return [data.year // 100, data.year % 100, data.month, data.day, data.hour, data.minute, data.second]

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
            if code == "":
                codes[node.symbol] = "1"
            else:
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
