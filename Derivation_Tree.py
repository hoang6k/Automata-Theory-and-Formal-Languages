def main():
    from create_Grammar import create_Grammar
    file_name = 'data/CFG_1'
    CFG, s = create_Grammar(file_name, type='CFG')
    CFG.print()
    P, routes = CFG.create_DT(s)
    print('Xau s: ' + s)
    print('Ap dung cac luat sinh lien tiep cho phan tu thuoc Vn trai nhat:', end='\n\t')
    print(P)
    print('Qua trinh bien doi lien tiep ve xau s tu trang thai ban dau:', end='\n\t')
    print(routes)

if __name__ == '__main__':
    main()
