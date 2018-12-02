from create_FA import create_FA
from create_graph import create_graph_FA

file_name = 'data/NFA_3'
NFA = create_FA(file_name, type='NFA')
NFA.print()
Gp = NFA.convert_to_Grammar()
Gp.print()

create_graph_FA(NFA, type='NFA', new='yes')
