from create_Grammar import create_Grammar
from create_graph import create_graph_DT

file_name = 'data/CFG_1'
CFG, s = create_Grammar(file_name, type='CFG')
CFG.print()
DT = CFG.create_DT(s)
print('Xau s: ' + s)
DT.print()

create_graph_DT(DT)
