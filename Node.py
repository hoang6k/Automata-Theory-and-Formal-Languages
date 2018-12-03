class Node():
    def __init__(self, label: str, type: str, children: list = []):
        self.label = label
        self.type = type
        self.children = children
    
    def fill(self, CFG, c):
        if self.type == 'leaf':
            return False
        else:
            print(len(self.children))
            if len(self.children) > 0:
                for i in range(len(self.children)):
                    print(self.children[i].label)
                    check = self.children[i].fill(CFG, c)
                    print('ket thuc dc mot lan check')
                    if check == True:
                        return True
                return False
            else:
                for c in CFG.P[int(c).x]:
                    if c in CFG.Vt:
                        self.children.append(Node(c, 'leaf'))
                    else:
                        self.children.append(Node(c, 'non_leaf'))
                return True
    