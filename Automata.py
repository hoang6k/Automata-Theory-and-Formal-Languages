from Delta import Delta
from collections import deque


class Automata():
    def __init__(self, Q, A, delta, q0, F, type):
        self.Q = Q
        self.A = A
        self.delta = delta
        self.q0 = q0
        self.F = F
        self.type = type

    def print(self):
        print('\n' + self.type)
        print('\tQ:', end=' ')
        for q in self.Q:
            print(q, end=' ')
        print('\n\tA:', end=' ')
        for c in self.A:
            print(c, end=' ')
        print('\n\tDelta:')
        for delta in self.delta:
            print('', end='\t\t')
            delta.print()
        print('\tq0:', end=' ')
        print(self.q0, end='')
        print('\n\tF:', end=' ')
        for q in self.F:
            print(q, end=' ')

    def convert_to_DFA(self):
        Q = []
        delta = []
        S = deque([[self.q0]])
        while len(S) > 0:
            p = S.popleft()
            Q.append(p)
            # print(p)
            delta_set = []
            for q in p:
                delta_set += Delta.find_delta(self.delta, q)
            for c in self.A:
                q_set = []
                for _delta in delta_set:
                    if _delta.c == c:
                        for q in _delta.set:
                            q_set.append(q)
                if len(q_set) == 0:
                    continue
                q_set = list(set(q_set))
                q_set.sort()
                delta.append(Delta(p, c, q_set, union='yes'))
                # delta_DFA[-1].print()
                try:
                    Q.index(q_set)
                except ValueError:
                    S.append(q_set)
        Q = sorted(Q, key=lambda _q: len(_q))
        delta = sorted(delta, key=lambda _delta: len(_delta.q))
        F = [q for q in Q if set(q) & set(self.F)]
        return Automata(Q, self.A, delta, [self.q0], F, 'DFA')

    def remove_unreachable_state(self):
        reachable_states = ['q0']
        new_states = ['q0']
        while 1:
            temp = []
            for q in new_states:
                for c in self.A:
                    temp += [_delta.set for _delta in self.delta if _delta.q == q and _delta.c == c]
            temp = list(set(temp))
            new_states = [q for q in temp if q not in reachable_states]
            reachable_states = list(set(reachable_states + new_states))
            new_states.sort()
            reachable_states.sort()
            if len(new_states) == 0:
                break
        return reachable_states

    def minimize_DFA(self):
        reachable_states = self.remove_unreachable_state()
        P = deque([self.F, [q for q in reachable_states if q not in self.F]])
        W = deque([self.F])
        while len(W) > 0:
            A = W.popleft()
            for c in self.A:
                X = [delta.q for delta in self.delta if delta.c == c and delta.set in A]
                if len(X) == 0:
                    continue
                for i in range(len(P)):
                    Y = P[i]
                    inter_Y_X = [q for q in Y if q in X]
                    recom_X_Y = [q for q in Y if q not in X]
                    if not inter_Y_X or not recom_X_Y:
                        continue
                    idx = P.index(Y)
                    P.remove(Y)
                    P.insert(idx, inter_Y_X)
                    P.insert(idx, recom_X_Y)
                    try:
                        idx = W.index(Y)
                    except ValueError:
                        if len(inter_Y_X) <= len(recom_X_Y):
                            W.append(inter_Y_X)
                        else:
                            W.append(recom_X_Y)
                    else:
                        W.remove(Y)
                        W.insert(idx, inter_Y_X)
                        W.insert(idx, recom_X_Y)
        Q = sorted(P, key=lambda _q: _q[0])
        q0 = str(Q[0])
        F = [q for q in Q if set(q) & set(self.F)]
        delta = []
        for q in Q:
            for c in self.A:
                for _delta in self.delta:
                    if _delta.q == q[0] and _delta.c == c:
                        for q_set in Q:
                            if _delta.set in q_set:
                                delta.append(Delta(q, c, q_set, union='yes'))
        return Automata(Q, self.A, delta, q0, F, 'DFA')
