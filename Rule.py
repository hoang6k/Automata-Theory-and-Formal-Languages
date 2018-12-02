class Rule():
    def __init__(self, A: str, x: str, B: str, type: str):
        self.A = A
        self.x = x
        self.B = B
        self.type = type
    
    def print(self):
        if self.type == 'right':
            print(self.A + ' -> ' + self.x + self.B)
        else:
            print(self.A + ' -> ' + self.B + self.x)
        