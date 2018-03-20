import numpy as np


class scale():
    weight_memory = []
    is_jumping = False
    treshhold = 0.2

    def __init__(self):
        pass

    def updated(self, new_value):
        self.weight_memory.append(new_value)
        if len(self.weight_memory) > 50:
            del self.weight_memory[0]

    def detect_jump(self):
        if not self.is_jumping and abs(self.weight_memory[-1] - self.weight_memory[-2]) > self.treshhold:
            self.is_jumping = True
        if self.is_jumping and abs(self.weight_memory[-1] - self.weight_memory[-2]) <= self.treshhold:
            self.is_jumping = False
            return True
        return False

    def jump_size(self):
        j = 0
        a = [[self.weight_memory[-1]]]
        for w in self.weight_memory[-1::-1]:
            if abs(a[j][-1] - w) > self.treshhold:
                a.append([w])
                j += 1
            else:
                a[j].append(w)
        a[:] = [np.mean(i) for i in a if len(i) > 1]
        return a[0] - a[1]


a = np.random.random([100])
s = scale()
for i in a:
    s.updated(i)

for i in a:
    s.updated(i)
    b = s.detect_jump()
    print(i, b)
    if b:
        print(s.jump_size())
