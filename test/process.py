def write_md_file(file):
    '''Takes .txt file as input, outputs new .md file with footnotes at the end of the file.
    Outpu file is placed in data/ directory under test.md name
    
    '''
    footnote_counter = 1
    footnote_list = []
    footnote = False
    
    f = open('data/test.md', 'w')
    
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
                        footnote_list.append('[^%s.] '%(footnote_counter) + line[char+1:].replace('\n', ''))
                        footnote_counter += 1
                        search = False
                        footnote = True
                    else:
                        f.write(line.replace('.' + str(footnote_counter), '[^%s]'%(footnote_counter)))
        except:
            if footnote and len(line) != 1:
                footnote_list[-1]+= line.replace('\n', '')
            else:
                f.write(line.replace('.' + str(footnote_counter), '[^%s]'%(footnote_counter)))
    for note in footnote_list:
        f.write(note)
    

if __name__ == '__main__':
    fpath = 'data/executive-summary.txt'
    file = open(fpath, 'r')
    write_md_file(file)