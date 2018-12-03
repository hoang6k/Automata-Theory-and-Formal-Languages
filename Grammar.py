from collections import deque

class Grammar():
    def __init__(self, Vt: list, Vn: list, S: str, P: list, type: str):
        self.Vt = Vt
        self.Vn = Vn
        self.S = S
        self.P = P
        self.type = type
    
    def print(self):
        if self.type == 'CFG' or self.type == 'G':
            print('\nCFG:'.format(self.type))
        elif self.type == 'Gc':
            print('\nGc:'.format(self.type))
        else:
            print('\n{}-linear Grammar:'.format(self.type.capitalize()))
        print('\tVt:', end=' ')
        for A in self.Vt:
            print(A, end=' ')
        print('\n\tVn:', end=' ')
        for A in self.Vn:
            print(A, end=' ')
        print('\n\tS: ' + self.S, end='')
        print('\n\tP:')
        for rule in self.P:
            print('', end='\t\t')
            rule.print()
    
    def convert_to_NFA(self):
        from Delta import Delta
        from Automata import Automata
        Q = self.Vn
        A = self.Vt
        q0 = self.S
        delta = []
        count = 0
        for item in self.P:
            if item.B == '':
                F = ['V_f']
                Q.append('V_f')
                break
        for item in self.P:
            if item.B != '':
                if len(item.x) == 1:
                    delta.append(Delta(item.A, item.x, item.B))
                    continue
                count += 1
                V_new = 'V_' + str(count)
                Q.append(V_new)
                delta.append(Delta(item.A, item.x[0], V_new))
                for i in range(1, len(item.x) - 1):
                    count += 1
                    V_new = 'V_' + str(count)
                    delta.append(Delta(Q[-1], item.x[i], V_new))
                    Q.append(V_new)
                delta.append(Delta(Q[-1], item.x[-1], item.B))
        for item in self.P:            
            if item.B == '':
                if len(item.x) == 1:
                    delta.append(Delta(item.A, item.x, F[0]))
                    continue
                count += 1
                V_new = 'V_' + str(count)
                Q.append(V_new)
                delta.append(Delta(item.A, item.x[0], V_new))
                for i in range(1, len(item.x) - 1):
                    count += 1
                    V_new = 'V_' + str(count)
                    delta.append(Delta(Q[-1], item.x[i], V_new))
                    Q.append(V_new)
                delta.append(Delta(Q[-1], item.x[-1], F[0]))
        return Automata(Q, A, delta, q0, F, 'NFA')
    
    def convert_to_Gc(self):
        from Rule import Rule
        from Grammar import Grammar
        Vt = self.Vt
        Vn = self.Vn
        S = self.S
        P = []
        P += [item for item in self.P if item.x in self.Vt]
        Vn2Vt = ['X_' + c for c in self.Vt]
        Vn += Vn2Vt
        P += [Rule(item, item[-1], '', 'CFG') for item in Vn2Vt]
        rules = deque([item for item in self.P if item.x not in self.Vt])
        Vn2Vn = deque([[c for c in item.x] for item in rules])
        count = 0
        for i in range(len(Vn2Vn)):
            for j in range(len(Vn2Vn[0])):
                if Vn2Vn[0][j] in Vt:
                    Vn2Vn[0][j] = 'X_' + Vn2Vn[0][j]
            if len(Vn2Vn[0]) == 2:
                P.append(Rule(rules[0].A, ''.join(Vn2Vn[0]), '', 'CFG'))
                rules.popleft()
                Vn2Vn.popleft()
            else:
                for j in range(len(Vn2Vn[0]) - 1):
                    if j == 0:
                        count += 1
                        P.append(Rule(rules[0].A, Vn2Vn[0][j] + 'D_' + str(count), '', 'CFG'))
                    elif j < len(Vn2Vn[0]) - 2:
                        count += 1
                        P.append(Rule('D_' + str(count - 1), Vn2Vn[0][j] + 'D_' + str(count), '', 'CFG'))
                    else:
                        P.append(Rule('D_' + str(count), Vn2Vn[0][j] + Vn2Vn[0][j + 1], '', 'CFG'))
                rules.popleft()
                Vn2Vn.popleft()
        return Grammar(Vt, Vn, S, P, 'Gc')

    def create_DT(self, s: str):
        from Node import Node
        from Tree import Tree
        root = Node(self.S, type='non_leaf')
        words = deque([item.x for item in self.P if item.A == root.label])
        routes = deque([str(i) for i in range(len(self.P)) if self.P[i].A == root.label])
        found = False
        while not found:
            count = len(words)
            for i in range(len(words)):
                item = words[0]
                if len(item) > len(s):
                    count -= 1
                    words.popleft()
                    routes.popleft()
                    continue
                for j in range(len(item)):
                    if item[j] == s[j]:
                        if j < len(item) - 1:
                            continue
                        else:
                            if len(item) < len(s):
                                words.popleft()
                                routes.popleft()
                                break
                            found = True
                            result = routes[0]
                    elif item[j] in self.Vn:
                        words += [item[:j] + rule.x + item[j+1:] for rule in self.P if rule.A == item[j]]
                        routes += [routes[0] + str(k) for k in range(len(self.P)) if self.P[k].A == item[j]]
                        words.popleft()
                        routes.popleft()
                        break
                    else:
                        words.popleft()
                        routes.popleft()
                        break
                if found:
                    break
            if found or count == 0:
                break
        if not found:
            print('Not found')
            return Tree(root)
        routes = []
        state = self.S
        routes = [state]
        for idx in result:
            for i in range(len(state)):
                if state[i] in self.Vn:
                    temp = state[:i] + self.P[int(idx)].x + state[i+1:]
                    state = temp
                    routes.append(state)
        P = [self.P[int(c)].A + ' -> ' + self.P[int(c)].x for c in result]
        return P, routes
        """
        print(self.P[int(result[0])].x)
        for c in self.P[int(result[0])].x:
            if c in self.Vt:
                root.children.append(Node(c, 'leaf'))
            else:
                root.children.append(Node(c, 'non_leaf'))
        print(root.label)
        print(len(root.children))
        for child in root.children:
            print(child.label)
        result = result[1:]
        print(result)
        for c in result:
            root.fill(self, c)
            print('Da qua mot vong lap')
        """
