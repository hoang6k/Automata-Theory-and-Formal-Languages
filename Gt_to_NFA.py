def main():
    from create_Grammar import create_Grammar
    from create_graph import create_graph_FA

    file_name = 'data/Gt_1'
    Gt = create_Grammar(file_name, 'left')
    Gt.print()
    NFA = Gt.convert_to_NFA()
    NFA.print()
    create_graph_FA(NFA, type='NFA', new='yes')

if __name__ == '__main__':
    main()
