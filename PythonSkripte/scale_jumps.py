import numpy as np
import usb.core
import usb.util


class scale():
    delay = 5
    weight_memory = [0]
    jump_memory = [False]
    treshhold = 20
    dev = []
    endpoint = []

    def __init__(self, delay=5, treshhold=20):
        self.delay = delay
        self.treshhold = treshhold
        self.dev = usb.core.find(idVendor=0x0922, idProduct=0x8003)
        self.dev.set_configuration()
        self.endpoint = self.dev[0][(0, 0)][0]

    def get_weight(self):
        data = self.dev.read(self.endpoint.bEndpointAddress,
                             self.endpoint.wMaxPacketSize)
        return data[-1] * 255 + data[-2]

    def updated(self, new_value):
        self.weight_memory.append(new_value)
        if abs(self.weight_memory[-1] - self.weight_memory[-2]) > self.treshhold:
            self.jump_memory.append(True)
        else:
            self.jump_memory.append(False)
        if len(self.weight_memory) > 50:
            del self.weight_memory[0]
            del self.jump_memory[0]

    def detect_jump(self):
        if self.jump_memory[:-self.delay:-1] == [False for i in range(self.delay - 1)] and self.jump_memory[-self.delay] == True:
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
        a[:] = [np.mean(i) for i in a if len(i) > self.delay]
        return a[0] - a[1]


s = scale()
for i in range(30):
    print(i)
    s.updated(s.get_weight())

for i in range(1000):
    s.updated(s.get_weight())
    b = s.detect_jump()
    if b:
        print(s.jump_size())
