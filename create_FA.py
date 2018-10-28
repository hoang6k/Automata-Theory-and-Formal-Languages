from Delta import Delta
from Automata import Automata


def create_FA(file_name, type):
    with open(file_name, 'r') as f:
        lines = f.readlines()
    for i in range(4):
        lines[i] = lines[i][:lines[i].find('#')].strip()
    A = lines[0].split()
    Q = [''.join(['q', str(i)]) for i in range(int(lines[1]))]
    F = [''.join(['q', i]) for i in lines[2].split()]
    delta = []
    num_delta = int(lines[3])
    if type == 'NFA':
        for i in range(num_delta):
            temp = [''.join(['q', item]) for item in lines[i + 5].split()]
            delta.append(Delta(temp[0], temp[1][1:], temp[2:]))
    else:
        for i in range(num_delta):
            temp = lines[i + 5].split()
            delta.append(Delta('q' + temp[0], temp[1], 'q' + temp[2]))
    del lines
    return Automata(Q, A, delta, 'q0', F, type=type)
