from Rule import Rule
from Grammar import Grammar

def create_Grammar(file_name: str, type: str):
    with open(file_name, 'r') as f:
        lines = f.readlines()
    f.close()
    for i in range(4):
        lines[i] = lines[i][:lines[i].find('#')].strip()
    Vt = lines[0].split()
    Vn = lines[1].split()
    S = lines[2]
    P = []
    num_rules = int(lines[3])
    for i in range(num_rules):
        temp = lines[i + 5].split()
        if type == 'CFG' or temp[-1] not in Vn:
            P.append(Rule(temp[0], ''.join(temp[1:]), '', type))
        else:
            P.append(Rule(temp[0], ''.join(temp[1:-1]), temp[-1], type))
    if type == 'CFG':
        string = lines[-1]
        return Grammar(Vt, Vn, S, P, type), string
    return Grammar(Vt, Vn, S, P, type)
    