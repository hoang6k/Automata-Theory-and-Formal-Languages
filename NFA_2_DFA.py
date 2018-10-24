from collections import deque

class Automata():
    def __init__(self, Q, A, delta, q0, F):
        self.Q = Q
        self.A = A
        self.delta = delta
        self.q0 = q0
        self.F = F
    
    def print_automata(self):
        print('\tQ:', end=' ')
        for item in self.Q:
            print(item, end=' ')
        print('\n\tA:', end=' ')
        for item in self.A:
            print(item, end=' ')
        print('\n\tdelta:')
        for item in self.delta:
            print('', end='\t\t')
            item.print()
        print('\tq0:', end=' ')
        print(self.q0, end='')
        print('\n\tF:', end=' ')
        for item in self.F:
            print(item, end=' ')
    
    @staticmethod
    def create_NFA(file_name):
        with open(file_name, 'r') as f:
            lines = f.readlines()
        for i in range(4):
            lines[i] = lines[i][:lines[i].find('#')].strip()
        A_DFA = lines[0].split()
        Q = [''.join(['q', str(i)]) for i in range(int(lines[1]))]
        F = set([''.join(['q', i]) for i in lines[2].split()])
        num_delta = int(lines[3])
        delta = []
        for i in range(num_delta):
            nums = [''.join(['q', item]) for item in lines[i + 5].split()]
            delta.append(Delta([nums[0]], nums[1][1:], nums[2:]))
        del lines, nums, i
        print('NFA:')
        NFA = Automata(Q, A_DFA, delta, 'q0', F)
        NFA.print_automata()
        return NFA
    
    def convert_DFA(NFA):
        Q_DFA = []
        delta_DFA = []
        S = deque([[NFA.q0]])
        while len(S) > 0:
            p = S.popleft()
            Q_DFA.append(p)
        #    print(p)
            delta_set = []
            for item in p:
                delta_set += Delta.find_state(NFA.delta, [item])
            for c in NFA.A:
                q_set = []
                for item in delta_set:
                    if item.a == c:
                        for q in item.set:
                            q_set.append(q)
                if len(q_set) == 0:
                    continue
                q_set = list(set(q_set))
                q_set.sort()
                delta_DFA.append(Delta(p, c, q_set))
        #        delta_DFA[-1].print()
                try:
                    Q_DFA.index(q_set)
                except ValueError:
                    S.append(q_set)
        Q_DFA = sorted(Q_DFA, key=lambda item: len(item))
        delta_DFA = sorted(delta_DFA, key=lambda item: len(item.q))
        F_DFA = [item for item in Q_DFA if set(item) & NFA.F]
        print('\nDFA:')
        DFA = Automata(Q_DFA, NFA.A, delta_DFA, [NFA.q0], F_DFA)
        DFA.print_automata()

class Delta():
    def __init__(self, q, a, set):
        self.q = q
        self.q.sort()
        self.a = a
        self.set = set
    
    def print(self):
        print('delta({}, {}) = {}'.format(self.q, self.a, self.set))
    
    @staticmethod
    def find_state(delta, q):
        result = []
        for item in delta:
            if item.q == q:
                result.append(item)
        return result

file_name = 'automata_NFA.txt'
NFA = Automata.create_NFA(file_name)
DFA = Automata.convert_DFA(NFA)




