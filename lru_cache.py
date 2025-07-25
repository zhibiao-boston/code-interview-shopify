from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.table = OrderedDict()

    def get(self, key):
        if key in self.table:
            self.table.move_to_end(key)
            return self.table[key]
        return -1

    def put(self, key, value):
        if key in self.table:
            self.table.move_to_end(key)
        self.table[key] = value
        if len(self.table) > self.capacity:
            self.table.popitem(last=False)