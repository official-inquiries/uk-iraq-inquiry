def make_clone(data):
    '''Returns Cloned data
    
    '''
    clone = {}
    for key in data:
        clone[key] = data[key]
    return clone

def yield_page(file):
    '''Devides whole file into the pages and yields one by one
    
    '''
    page = {}
    line = 0
    page_num = False
    for row in file:
        try:
            int(row[:-1])
            page[line] = row
            page_num = True
        except:
            if page_num:
                yield page
                page = {}
                line = 0
                page_num = False
            page[line] = row
            line += 1

def check_anchor(page, num):
    '''Checks whether given page has given footnote number more then once.
    If not modifies the line, adding ^ symbol before number
    Returns modified page
    
    '''
    occured = []
    clone = make_clone(page)
    for line in page:
        if num in page[line]:
            num_index = page[line].index(num)
            try:
                int(page[line][num_index - 1])
            except:
                if page[line][num_index -1] != ' ' and num_index:
                    occured.append(line)
    if len(occured) == 1:
        clone[occured[0]]= page[occured[0]].replace(num, '^%s'%(num))
    else:
        print 'More than one or no candidate for footnote %s: Please correct manually.'%(num)
    
    return clone    

def modify_page(page):
    '''Takes single page as input, Returns modified page.
    Collects fottnotes and appaends to globall variable.
    
    '''
    global FOOTNOTE_LIST, FOOTNOTE_COUNTER
    footnote = False
    clone = make_clone(page)            
    for line in page:  
        try:
            int(page[line][0])
            char = 1
            search = True
            footnote = False
            while search:
                try:
                    int(page[line][char])
                    char += 1
                except:
                    search = False
                    if page[line][char] == ' ' and str(FOOTNOTE_COUNTER) == page[line][:char]:
                        footnote_num = page[line][:char]
                        text = page[line][char+1:].replace('\n', '')
                        FOOTNOTE_LIST.append('[^%s.] '%(footnote_num) + text)
                        FOOTNOTE_COUNTER += 1
                        clone[line] = '' 
                        footnote = True
                        clone = check_anchor(clone, footnote_num)
        except:
            if footnote and len(page[line]) != 1:
                FOOTNOTE_LIST[-1]+= page[line].replace('\n', '')
                clone[line] = ''
    return clone          
    
def write_file(inpath, outpath):    
    '''Reads file that needs to b modified and creates new file in outpath directory
    
    '''
    file = open(inpath, 'r')
    f = open(outpath, 'w')
    
    for page in yield_page(file):
        new_page = modify_page(page)
        for line in new_page:
            f.write(new_page[line])
            
    for line in FOOTNOTE_LIST:
        f.write(line)
        
    file.close()
    f.close()
    
if __name__ == '__main__':
    FOOTNOTE_LIST = []
    FOOTNOTE_COUNTER = 1
    write_file('data/executive-summary.txt', 'data/test.md')