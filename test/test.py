import tempfile
import shutil
import sys
import os
#imports main script
sys.path.insert(0, sys.path[0] + '/../scripts/')
import process 

import unittest
    
class TestProcess(unittest.TestCase):
    
    def test_io(self):
        '''Works with command line arguments
        
        '''
        inpath, outpath = process.get_io()
        self.assertEqual(inpath, 'test/data/input.txt', msg='Expected test/data/input.txt, but got %s'%(inpath))
        self.assertEqual(outpath, 'test/data/output.md', msg='Expected test/data/output.md, but got %s'%(outpath))
    
    def test_tidy_up(self):
        '''Works with tidying text up
        
        '''
        line_1 = process.tidy_up('\xe2\x80\xa2  a new inspectorate, the United Nations Monitoring, Verification and Inspection ')
        line_2 = process.tidy_up('{{ internecine violence;')
        result_1 = '*  a new inspectorate, the United Nations Monitoring, Verification and Inspection '
        result_2 = ' *  internecine violence;' 
        self.assertEqual(line_1, result_1, msg='Expected "*  a new inspectorate, the United Nations Monitoring, Verification and Inspection ", but got "%s"'%(line_1))
        self.assertEqual(line_2, result_2, msg='Expected "*  internecine violence;", but got "%s"'%(line_2))
    
    def test_make_clone(self):
        '''Works with making page clone
        
        '''
        page = {1: 'line one', 2: 'line two'}
        clone = process.make_clone(page)
        self.assertEqual(page, clone, msg='Expected True, but got False')
        clone[3] = 'line three'
        self.assertNotEqual(page, clone, msg='Expected False, but got True')
    
    def test_yield_page(self):
        '''Works with chunking file into pages
        
        '''
        inpath, outpath = process.get_io()
        f = open(inpath, 'r')
        page_counter = 0
        for i in process.yield_page(f):
            page_counter +=  1
            page = i
        self.assertEqual(page_counter, 2, msg='Expected False, but got True')
        test = page[16]
        result = 'provisions. His ambitions to rebuild Iraq\xe2\x80\x99s weapons of mass destruction \n'
        message = 'Expected "provisions. His ambitions to rebuild Iraq\xe2\x80\x99s weapons of mass destruction \n", but got %s'%(page_counter)
        self.assertEqual(test, result, msg=message)
        f.close()
    
    def test_check_anchor(self):
        '''Works with detecting anchors
        
        '''
        page = {0: "of the international community.1",
                1: "resolution in December 1999, although China, France and Russia abstained.2",
                2: "55. President Bushs remarks36 on 26 November.2 renewed UK concerns that US "}
        test_1 = process.check_anchor(page, '1')
        test_2 = process.check_anchor(page, '2')    
        test_3 = process.check_anchor(page, '36')
        result_1 = {0: 'of the international community.[^1]',
                    1: 'resolution in December 1999, although China, France and Russia abstained.2',
                    2: '55. President Bushs remarks36 on 26 November.2 renewed UK concerns that US '}
        result_2 = {0: 'of the international community.1',
                    1: 'resolution in December 1999, although China, France and Russia abstained.[^2]',
                    2: '55. President Bushs remarks36 on 26 November.2 renewed UK concerns that US '}
        result_3 = {0: 'of the international community.1',
                    1: 'resolution in December 1999, although China, France and Russia abstained.2',
                    2: '55. President Bushs remarks[^36] on 26 November.2 renewed UK concerns that US '}
        
        self.assertEqual(test_1, result_1)
        self.assertEqual(test_2, result_2)
        self.assertEqual(test_3, result_3)
    
    def test_output(self):
        '''Works with whole output
        
        '''
        inpath, outpath = process.get_io()
        tmpdir = tempfile.mkdtemp()
        tmpfile = tmpdir + '/output.md'
        tidy_path = inpath.split('.')[0] + '-tidy.' + inpath.split('.')[1]
        
        self.assertFalse(os.path.exists(tmpfile))
        self.assertFalse(os.path.exists(tidy_path))
        
        process.write_file(inpath, tmpfile)
        
        self.assertTrue(os.path.exists(tmpfile))
        self.assertTrue(os.path.exists(tidy_path))
        
        test = open(tmpfile, 'r')
        result = open(outpath, 'r')
        tidy_test = open(tidy_path, 'r')
        test_data = test.readlines()
        result_data = result.readlines()
        tidy_test_data = tidy_test.readlines()
        result.close()
        test.close()
        tidy_test.close()
        shutil.rmtree(tmpdir)
        os.remove(tidy_path)
        
        self.assertEqual(len(test_data), len(result_data), msg="Expected %d, but got %d"%(len(test_data),len(result_data)))
        self.assertEqual(test_data, result_data, msg="Tested markdown file does not match with Result")
        
        self.assertEqual(len(tidy_test_data), len(result_data), msg="Expected %d, but got %d"%(len(tidy_test_data),len(result_data)))
        self.assertEqual(tidy_test_data, result_data, msg="Tested text file does not match with Result")
        
    
if __name__ == '__main__':
    unittest.main()
    
