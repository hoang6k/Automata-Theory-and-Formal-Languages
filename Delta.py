class Delta():
    def __init__(self, q, c, set, union='no'):
        self.q = q
        self.c = c
        self.set = set
        if union == 'yes':
            self.q.sort()
            self.set.sort()

    def print(self):
        print('δ({}, {}) = {}'.format(self.q, self.c, self.set))

    @staticmethod
    def find_delta(delta, q):
        return [_delta for _delta in delta if _delta.q == q]
