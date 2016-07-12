def collect_footnote(file):
    '''funcion to collent lines that are footnotes. returns list of furnotes
    
    '''
    footnote_counter = 1
    footnote_list = []
    footnote = False
    for line in file:
        try:
            int(line[0])
            char = 1
            search = True
            footnote = False
            while search:
                try:
                    int(line[char])
                    char += 1
                except:
                    search = False
                    if line[char] == ' ' and footnote_counter == int(line[:char]):
                        footnote_counter += 1
                        footnote = True
                        footnote_list.append(line.replace('\n', ''))
                        search = False
                    elif line[char] == ' ' and footnote_counter != int(line[:char]) and footnote:
                        footnote_list[-1] += line.replace('\n', '')
                        footnote = False
        except:
            if footnote and len(line) != 1:
                footnote_list[-1]+= line.replace('\n', '')
                footnote = False

    return footnote_list

def test(data):
    '''test 
    '''
    import random
    random_number = random.randrange(len(data))
    
    assert(int(data[0][0]) == 1), 'Numbering fails: Result should be 1, but got %s'%(data[0][0])
    assert(int(data[-1][:3]) == len(data)), 'Numbering fails: Result should be %s, but got %s'%(len(data), data[-1][:3])
    assert(data[random_number - 1][:len(str(random_number - 1))] == str(random_number)), 'Numbering fails: Result should be %s, but got %s'%(random_number, data[-1][:3], data[random_number - 1][:len(str(random_number - 1))])
    print 'Footnote Numbering match passed'
    assert(data[-1] == "283 Foreign Secretary, November 2003, The Decision to go to War in Iraq Response of the Secretary of State for Foreign and Commonwealth Affairs, November 2003, Cm6062, paragraph 27."), "Content does not match - Should be: '283 Foreign Secretary, November 2003, The Decision to go to War in Iraq Response of the Secretary of State for Foreign and Commonwealth Affairs, November 2003, Cm6062, paragraph 27.' but got %s"%(data[-1])
    print 'Content match passed'
    print
    print 'Footnote# ' + data[random_number]
    print 
    print 'file contains %s footnotes. All tests passed'%(len(data))

if __name__ == '__main__':
    fpath = 'data/executive-summary.txt'
    file = open(fpath)
    data = collect_footnote(file)
    test(data)