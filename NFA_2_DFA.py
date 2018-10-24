from collections import deque

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
    
with open('automata_NFA.txt', 'r') as f:
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
    delta[-1].print()
del lines, nums, i

Q_DFA = []
delta_DFA = []
S = deque([['q0']])
while len(S) > 0:
    p = S.popleft()
    Q_DFA.append(p)
#    print(p)
    delta_set = []
    for item in p:
        delta_set += Delta.find_state(delta, [item])
    for c in A_DFA:
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
F_DFA = [item for item in Q_DFA if set(item) & F]
for item in Q_DFA:
    print(item)
for item in delta_DFA:
    item.print()
for item in F_DFA:
    print(item)


