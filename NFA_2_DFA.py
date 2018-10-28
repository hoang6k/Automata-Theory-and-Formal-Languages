from create_FA import create_FA
from create_graph import create_graph_FA

file_name = 'NFA_1'
NFA = create_FA(file_name, type='NFA')
NFA.print()
DFA = NFA.convert_to_DFA()
DFA.print()

create_graph_FA(NFA, type='NFA', new='yes')
create_graph_FA(DFA)
