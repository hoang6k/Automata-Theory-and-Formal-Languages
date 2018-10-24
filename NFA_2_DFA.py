from collections import deque
from create_graph import create_graph_FA

class Automata():
    def __init__(self, Q, A, delta, q0, F, type='NFA'):
        self.Q = Q
        self.A = A
        self.delta = delta
        self.q0 = q0
        self.F = F
        self.type = type
    
    def print_automata(self):
        print(self.type)
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
            delta.append(Delta(nums[0], nums[1][1:], nums[2:]))
        del lines, nums, i
        NFA = Automata(Q, A_DFA, delta, 'q0', F)
        return NFA
    
    def convert_to_DFA(NFA):
        Q = []
        delta = []
        S = deque([[NFA.q0]])
        while len(S) > 0:
            p = S.popleft()
            Q.append(p)
        #    print(p)
            delta_set = []
            for item in p:
                delta_set += Delta.find_state(NFA.delta, item)
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
                delta.append(Delta(p, c, q_set, type='DFA'))
        #        delta_DFA[-1].print()
                try:
                    Q.index(q_set)
                except ValueError:
                    S.append(q_set)
        Q = sorted(Q, key=lambda item: len(item))
        delta = sorted(delta, key=lambda item: len(item.q))
        F = [item for item in Q if set(item) & NFA.F]
        DFA = Automata(Q, NFA.A, delta, [NFA.q0], F, 'DFA')
        return DFA

class Delta():
    def __init__(self, q, a, set, type='NFA'):
        self.q = q
        if type == 'DFA':
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
NFA.print_automata()
DFA = Automata.convert_to_DFA(NFA)
DFA.print_automata()

create_graph_FA(NFA)
create_graph_FA(DFA, type='DFA')