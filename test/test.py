import tempfile
import shutil
import sys, getopt

def tyde_up(line):
    """Tyides the given line up
    
    """
    result = line.replace('{{', '* ').replace('\xe2\x80\xa2 ', '* ')
    return result

def make_clone(data):
    '''Returns Cloned data
    
    '''
    clone = {}
    for key in data:
        clone[key] = data[key]
    return clone

def yield_page(file):
    '''Devides whole file into the pages and yields one by one
    Removes page numbers
    '''
    global PAGE_NUMBER
    page = {}
    line = 0
    page_num = False
    for row in file:
        try:
            int(row[:-1])
            if int(row[:-1]) == PAGE_NUMBER:
                PAGE_NUMBER += 1
                page[line] = '' #removes page number
            else:
                page[line] = tyde_up(row)
            page_num = True
        except:
            if page_num:
                yield page
                page = {}
                line = 0
                page_num = False
            page[line] = tyde_up(row)
            line += 1

def check_anchor(page, num):
    '''Checks whether given page has given footnote number more then once.
    If not modifies the line, adding ^ symbol before number
    Returns modified page
    
    '''
    occured = []
    clone = make_clone(page)
    for line in page:
        page_line = page[line]
        # get's rid from the pragraph numbers in the begining of the line
        while True:
            try:
                int(page_line[0])
                page_line = page_line[1:]
            except:
                break        
        if num in page_line:
            num_index = page_line.index(num)
            previous_char = page_line[num_index - 1]
            try:
                int(previous_char)
                more_then_once = len(page_line.split(num)) > 2
                if more_then_once:
                    occured.append(line)
            except:
                if previous_char != ' ':
                    occured.append(line)
                    
    if len(occured) == 1:
        clone[occured[0]]= page[occured[0]].replace(num, '[^%s]'%(num))
    else:
        pass
        # print 'More than one or no candidate for footnote %s found: Please correct manually.'%(num)
    return clone    

def modify_page(page):
    '''Takes single page as input, Returns modified page.
    Collects fottnotes and appends to global variable.

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
    '''Reads file that needs to be modified and creates new file in outpath directory
    
    '''    
    readfile = open(inpath, 'r')
    writefile = open(outpath, 'w')
    
    for page in yield_page(readfile):
        new_page = modify_page(page)
        for line in new_page:
            writefile.write(new_page[line])
            
    for line in FOOTNOTE_LIST:
        writefile.write(line)
        
    readfile.close()
    writefile.close()
    

def get_io(argv):
    """Takes comand line arguments as input and returns tuple of path to input and output file
    
    """
    inputfile = 'test/data/executive-summary.txt'
    outputfile = 'test/data/test.md'
    try:
       opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
       print 'test.py -i <inputfile> -o <outputfile>'
       sys.exit(2)
    for opt, arg in opts:
       if opt == '-h':
          print 'test.py -i <inputfile> -o <outputfile>'
          sys.exit()
       elif opt in ("-i", "--ifile"):
          inputfile = arg
       elif opt in ("-o", "--ofile"):
          outputfile = arg
          
    return inputfile, outputfile

def test():
    '''Test function for helper functions and output
    
    '''
    # test get_io
    inpath, outpath = get_io(sys.argv[1:])
    assert inpath == 'test/data/executive-summary.txt', 'Expected test/data/executive-summary.txt, but got %s'%(inpath)
    assert outpath == 'test/data/test.md', 'Expected test/data/test.md, but got %s'%(outpath)
    print 'Works with Command Line arguments'    
    print
    # test tidy_up
    line_1 = tyde_up('\xe2\x80\xa2  a new inspectorate, the United Nations Monitoring, Verification and Inspection ')
    line_2 = tyde_up('{{ internecine violence;')
    assert line_1 == '*  a new inspectorate, the United Nations Monitoring, Verification and Inspection ', 'Expected "*  a new inspectorate, the United Nations Monitoring, Verification and Inspection ", but got "%s"'%(line_1)
    assert line_2 == '*  internecine violence;', 'Expected "*  internecine violence;", but got "%s"'%(line_2)
    print 'Works with bullet points'
    print
    # test make_clone
    page = {1: 'line one', 2: 'line two'}
    clone = make_clone(page)
    assert page == clone, 'Expected True, but got False'
    clone[3] = 'line three'
    assert not page == clone, 'Expected False, but got True'
    print "Works with cloning pages"
    print
    # test yield_page
    f = open(inpath, 'r')
    page_counter = 0
    for i in yield_page(f):
        page_counter +=  1
        page = i
    assert page_counter == 152, 'Expected 152, but got %s'%(page_counter)
    assert page[20] == 'Departure of the last UK naval training team from Iraq\n', 'Expected "Departure of the last UK naval training team from Iraq\n", but got %s'(page[20])
    print 'Works with dividing whole file into page chunks'
    print
    f.close()
    # test check_anchor
    page = {0: "of the international community.1",
            1: "resolution in December 1999, although China, France and Russia abstained.2",
            2: "55. President Bushs remarks36 on 26 November.2 renewed UK concerns that US "}
    result_1 = check_anchor(page, '1')
    result_2 = check_anchor(page, '2')
    result_3 = check_anchor(page, '36')
    assert result_1 == {0: 'of the international community.[^1]', 1: 'resolution in December 1999, although China, France and Russia abstained.2', 2: '55. President Bushs remarks36 on 26 November.2 renewed UK concerns that US '}
    assert result_2 == {0: 'of the international community.1', 1: 'resolution in December 1999, although China, France and Russia abstained.[^2]', 2: '55. President Bushs remarks36 on 26 November.2 renewed UK concerns that US '}
    assert result_3 == {0: 'of the international community.1', 1: 'resolution in December 1999, although China, France and Russia abstained.2', 2: '55. President Bushs remarks[^36] on 26 November.2 renewed UK concerns that US '}
    print 'Works with anchors'
    print
    # test whole output
    tmpdir = tempfile.mkdtemp()
    tmpfile = tmpdir + '/test.md'
    write_file(inpath, tmpfile)
    f = open(tmpfile, 'r')
    data = f.readlines()
    assert data[298][-6:-2] == '[^1]', 'expected [^1], but got %s'%(data[298][-6:-2])
    assert data[306][-4:-2] == '.2', 'expected .2, but got %s'%(data[306][-4:-2])
    assert data[494][31: 36] == '[^16]', 'expected [^16], but got %s'%(data[494][31: 36])
    assert data[1093][-6:-1] == '[^63]', 'expected [^63], but got %s'%(data[1093][-6:-1])
    assert data[348][-4:-2] == '.5', 'expected .5, but got %s'%(data[348][-4:-2])
    assert data[3873][15:18] == '225', 'expected 225, but got %s'%(data[3873][15:18])
    assert '[^283.]' in data[-1], 'expected True, but got False'
    assert not '[^284.]' in data[-1], 'expected False, but got True'
    print 'Works with footnotes'
    print
    print 'All tests passed'
    f.close()
    shutil.rmtree(tmpdir)
    
if __name__ == '__main__':
    PAGE_NUMBER = 1    
    FOOTNOTE_LIST = ['\n']
    FOOTNOTE_COUNTER = 1
    PAGE_NUMBER = 1
    test()
    