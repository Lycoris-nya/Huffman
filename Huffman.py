from Node import Node
from PriorityQueue import Priority_queue


class Huffman:
    def compress_file(self, data_filename, arch_filename):
        with open(data_filename, "rb") as data:
            read_data = data.read()
            arch = self.compress_file_bytes(read_data)
        with open(arch_filename, "wb") as a:
            a.write(bytearray(arch))

    def decompress_file(self, arch_filename, data_filename):
        with open(arch_filename, "rb") as arch:
            read_arch = arch.read()
            data = self.decompress_file_bytes(read_arch)
        with open(data_filename, "wb") as a:
            a.write(bytearray(data))

    def decompress_file_bytes(self, read_arch):
        data_length, start_index, freqs = self.parse_header(read_arch)
        root = self.create_Huffman_tree(freqs)
        data = self.decompress(read_arch, start_index, data_length, root)
        return data

    def decompress(self, arch, start_index, data_length, root):
        size = 0
        curr = root
        data = []
        for i in range(start_index,len(arch)):
            bit = 1
            while bit <= 128:
                if (arch[i] & bit) == 0:
                    curr = curr.bit0
                else:
                    curr = curr.bit1
                if curr.bit0 is not  None:
                    bit <<= 1
                    continue
                size += 1
                if size <= data_length:
                    data.append(curr.symbol)
                curr = root
                bit <<= 1
        return data


    def parse_header(self, arch):
        data_length = arch[0] | (arch[1] << 8) | (arch[1] << 16) | (arch[1] << 24)
        freqs = [0] * 256
        for i in range(256):
            freqs[i] = arch[4 + i]
        start_index = 4 + 256
        return data_length, start_index, freqs



    def compress_file_bytes(self, data):
        freqs = self.calculate_freq(data)

        root = self.create_Huffman_tree(freqs)
        codes = self.create_Huffman_code(root)
        bits = self.compress(data, codes)
        head = self.create_header(len(data), freqs)
        return head + bits

    def create_header(self, data_length, freqs):
        head = []
        head.append(data_length & 255)
        head.append((data_length >> 8) & 255)
        head.append((data_length >> 16) & 255)
        head.append((data_length >> 24) & 255)
        for i in range(256):
            head.append(freqs[i])
        return head

    def compress(self, data, codes):
        bits = []
        sum = 0
        bit = 1
        for symbol in data:
            for c in codes[symbol]:
                if c == "1":
                    sum |= bit
                if bit < 128:
                    bit = bit << 1
                else:
                    bits.append(sum)
                    sum = 0
                    bit = 1
        if bit > 1:
            bits.append(sum)
        return bits

    def create_Huffman_code(self, root):
        codes = [None]*256
        self.go_to_next_node(root, "", codes)
        return codes

    def go_to_next_node(self, node, code, codes):
        if node.bit0 is None:
            codes[node.symbol] = code
        else:
            self.go_to_next_node(node.bit0, code + "0", codes)
            self.go_to_next_node(node.bit1, code + "1", codes)


    def calculate_freq(self, data):
        freqs = [0] * 256
        for byte in data:
            freqs[byte] += 1
        self.normalize_freqs(freqs)
        return freqs

    def normalize_freqs(self, freqs):
        max_item = max(freqs)
        if max_item <= 255:
            return
        for i in range(256):
            if freqs[i] > 0:
                freqs[i] = 1 + freqs[i] * 255 // (max_item + 1)

    def create_Huffman_tree(self, freqs):
        priority_queue = Priority_queue()
        for i in range(256):
            if freqs[i] > 0:
                priority_queue.enqeue(freqs[i], Node(freqs[i], symbol=i))
        while priority_queue.size > 1:
            bit0 = priority_queue.dequeu()
            bit1 = priority_queue.dequeu()
            freq = bit0.freq + bit1.freq
            next_node = Node(freq, bit0 = bit0, bit1 = bit1)
            priority_queue.enqeue(freq, next_node)
        return priority_queue.dequeu()
