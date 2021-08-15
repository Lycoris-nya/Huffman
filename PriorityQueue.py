from queue import Queue


class Priority_queue:

    def __init__(self):
        self.storage = dict()
        self.size = 0

    def enqeue(self, priority, item):
        if priority not in self.storage.keys():
            self.storage[priority] = Queue()
        self.storage[priority].put(item)
        self.size += 1

    def dequeu(self):
        if self.size == 0:
            raise RuntimeError("Очередь пуста")
        self.size -= 1
        list_keys = list(self.storage.keys())
        list_keys.sort()
        for i in list_keys:
            if self.storage[i].qsize() > 0:
                return self.storage[i].get()
        raise RuntimeError("Queue error")
