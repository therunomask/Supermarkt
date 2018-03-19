import numpy as np


class scale:
    weight_memory=[]
    is_jumping=False
    treshhold=10
    def updated(self,new_value):
        self.weight_memory+=new_value
        if len(self.weight_memory)>10:
            del self.weight_memory[0]
    def detect_jump(self):
        if not self.is_jumping and abs(self.weight_memory[-1]-self.weight_memory[-2])>self.treshhold:
            self.is_jumping=True
        if self.is_jumping and abs(self.weight_memory[-1]-self.weight_memory[-2])<=self.treshhold:
            self.is_jumping=False
            return True
        return False
    def jump_size(self):
        j=0
        a=[[self.weight_memory[-1]]]
        for num,w in enumerate(self.weight_memory[1::-1]):
            if abs(j[-1]-w)>10:
                a.append([w])
                j+=1
            else:
                a[j].append(w)
        a[:]=[np.mean(i) for i in a if len(i)>1]
        return a[0]-a[1]

    
def scale_jumps():