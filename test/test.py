def test(file):
    '''test
    
    '''
    data = file.readlines()
    
    assert data[298][-6:-2] == '[^1]', 'expected [^1], but got %s'%(data[298][-6:-2])
    assert data[306][-4:-2] == '.2', 'expected .2, but got %s'%(data[306][-4:-2])
    assert data[494][31: 36] == '[^16]', 'expected [^16], but got %s'%(data[494][31: 36])
    assert data[1093][-6:-1] == '[^63]', 'expected [^63], but got %s'%(data[1093][-6:-1])
    assert data[348][-4:-2] == '.5', 'expected .5, but got %s'%(data[348][-4:-2])
    assert data[3873][15:18] == '225', 'expected 225, but got %s'%(data[3873][15:18])
    assert '[^283.]' in data[-1], 'expected True, but got False'
    assert not '[^284.]' in data[-1], 'expected False, but got True'

if __name__ == '__main__':
    fpath = 'data/test.md'
    file = open(fpath)
    test(file)
    file.close()