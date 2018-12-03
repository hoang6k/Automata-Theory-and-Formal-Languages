from Node import Node
class Tree():
    def __init__(self, root: Node):
        self.root = root
    
    def fill(self, node: Node, CFG, c):
        if node.type == 'leaf':
            return False
        else:
            print(len(node.children))
            if len(node.children) > 0:
                for child in node.children:
                    print(child.label)
                    check = self.fill(child, CFG, c)
                    print('ket thuc dc mot lan check')
                    if check == True:
                        return True
                return False
            else:
                print('Da tim thay dinh moi')
                print(node.label + ' chuyen thanh ' + CFG.P[int(c)].x)
                for c in CFG.P[int(c).x]:
                    if c in CFG.Vt:
                        node.children.append(Node(c, 'leaf'))
                    else:
                        node.children.append(Node(c, 'non_leaf'))
                return True
                    
    