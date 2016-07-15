def test(file):
    '''test
    
    '''
    data = file.readlines()
    assert data[298][-4:-2] == '^1'
    assert data[494][31: 34] == '^16' 
    assert data[1093][-4:-1] == '^63'
    assert data[348][-4:-2] == '.5'
    assert data[3873][15:18] == '225' 
    assert data[306][-4:-2] == '^2', 'Anchore for footnote #2 needs to be corrected'

if __name__ == '__main__':
    fpath = 'data/test.md'
    file = open(fpath)
    test(file)