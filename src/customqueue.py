from queue import Queue

class CustomQueue(Queue):

    def __init__(self, *args):
        super().__init__()
        
        for k in args:
            self.put(k)

    def add_list(self, l):
        for elt in l:
            self.put(elt)

    def __add__(self, other):
        res = CustomQueue()
        
        for elt in self:
            res.put(elt)
        
        for elt in other:
            res.put(elt)
        
        return res
    
    def __iter__(self):
        self.current = -1
        return self

    def __next__(self):
        self.current += 1
        if self.current >= self.qsize():
            raise StopIteration
        
        return self.queue[self.current]

    def __str__(self) -> str:
        return "[" + ", ".join(self.queue) + "]"





    