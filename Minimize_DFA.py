from create_FA import create_FA
from create_graph import create_graph_FA

file_name = 'DFA_1'
DFA = create_FA(file_name, type='DFA')
DFA.print()
m_DFA = DFA.minimize_DFA()
m_DFA.print()

create_graph_FA(DFA, new='yes')
create_graph_FA(m_DFA)
