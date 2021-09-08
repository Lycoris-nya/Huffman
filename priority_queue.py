from queue import Queue


class PriorityQueue:

    def __init__(self):
        self.storage = dict()
        self.size = 0

    def enqueue(self, priority, item):
        if priority not in self.storage.keys():
            self.storage[priority] = Queue()
        self.storage[priority].put(item)
        self.size += 1

    def dequeue(self):
        if self.size == 0:
            raise RuntimeError("Очередь пуста")

        max_priority = min(self.storage.keys())

        if self.storage[max_priority].qsize() > 0:
            element = self.storage[max_priority].get()
            self.size -= 1
            if self.storage[max_priority].qsize() == 0:
                self.storage.pop(max_priority)
            return element

        raise RuntimeError("Queue error")
