class Grammar():
    def __init__(self, Vt: list, Vn: list, S: str, P: list, type: str):
        self.Vt = Vt
        self.Vn = Vn
        self.S = S
        self.P = P
        self.type = type
    
    def print(self):
        if self.type == 'CFG':
            print('\nCFG:')
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

    def convert_to_DT(s: str):
        pass





