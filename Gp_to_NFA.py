def main():
    from create_Grammar import create_Grammar
    from create_graph import create_graph_FA
    
    file_name = 'data/Gp_1'
    Gp = create_Grammar(file_name, 'right')
    Gp.print()
    NFA = Gp.convert_to_NFA()
    NFA.print()
    
    create_graph_FA(NFA, type='NFA', new='yes')

if __name__ == '__main__':
    main()
