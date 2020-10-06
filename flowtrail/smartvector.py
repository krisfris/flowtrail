import numpy as np


class SmartVector:
    def __init__(self):
        self.vec = np.array([], np.float32)
        self.id_count = 0
        self.indices = {}
        self.freed_ids = []

    def data(self):
        return self.vec

    def my_data(self, id_):
        index, length = self.indices[id_]
        return self.vec[index:index+length]

    def find_in_freed(self, size):
        for id in self.freed_ids:
            idx, s = self.indices[id]
            if s == size:
                return id

    def register(self, size, data=None):
        found = self.find_in_freed(size)
        if found:
            if data is not None:
                self.update_data(found, data)
            self.freed_ids.remove(found)
            return found

        id_ = self.id_count
        self.id_count += 1
        self.indices[id_] = (len(self.vec), size)

        if data is None:
            data = np.empty(size, np.float32)

        self.vec = np.concatenate((self.vec, data))

        return id_

    def push_data(self, data):
        return self.register(data.size, data)

    def erase(self, id_):
        self.zero(id_)
        #del self.indices[id_]
        self.freed_ids.append(id_)

    def zero(self, id_):
        index, length = self.indices[id_]
        self.vec[index:index+length] = np.zeros(length)

    def update_data(self, id_, data):
        index, length = self.indices[id_]
        self.vec[index:index+length] = data
