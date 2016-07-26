import sys, getopt
# Global variables
FOOTNOTE_COUNTER = 1
PAGE_NUMBER = 1
MESSAGE = ''

def tidy_up(line):
    """Tidies the given line up
    
    """
    result = line.replace('{{', '* ').replace('\xe2\x80\xa2', '*')
    # Removes document title and report name form the begining of the page
    if '\x0c' in result:
        result = result[result.index('\x0c') + 1:]
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
                page[line] = ''
            else:
                page[line] = tidy_up(row)
            yield page
            page = {}
            line = 0
            page_num = False
        except:                
            page[line] = tidy_up(row)
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
        if MESSAGE:
            print MESSAGE%(num)
    return clone    

def modify_page(page):
    '''Takes single page as input, Returns modified page.
    Collects fottnotes and appends to global variable.

    '''
    global FOOTNOTE_COUNTER
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
                        text = page[line][char+1:].replace('\n', '') + '\n'
                        FOOTNOTE_COUNTER += 1
                        clone[line] = ''
                        footnote = True
                        clone = check_anchor(clone, footnote_num)
                        clone[line] = '[^%s]: '%(footnote_num) + text
        except:
            if footnote and len(page[line]) != 1:
                page[line-1] = page[line-1].replace('\n', '') + page[line].replace('\n', '') + '\n'
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
        
    readfile.close()
    writefile.close()
    

def get_io(argv=None):
    """Takes comand line arguments as input and returns tuple of path to input and output file
    
    """
    inputfile = 'test/data/input.txt'
    outputfile = 'test/data/output.md'
    try:
       opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
       print 'process.py -i <inputfile> -o <outputfile>'
       sys.exit(2)
    for opt, arg in opts:
       if opt == '-h':
          print 'process.py -i <inputfile> -o <outputfile>'
          sys.exit()
       elif opt in ("-i", "--ifile"):
          inputfile = arg
       elif opt in ("-o", "--ofile"):
          outputfile = arg
          
    return inputfile, outputfile
    
if __name__ == '__main__':    
    INPATH, OUTPATH = get_io(sys.argv[1:])
    MESSAGE = 'More than one or no candidate for footnote %s found: Please correct manually.'
    write_file(INPATH, OUTPATH)
    