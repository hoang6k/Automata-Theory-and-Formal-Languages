def main():
    from create_Grammar import create_Grammar
    file_name = 'data/CFG_3'
    CFG= create_Grammar(file_name, 'G')
    CFG.print()
    Gc = CFG.convert_to_Gc()
    Gc.print()

if __name__ == '__main__':
    main()
