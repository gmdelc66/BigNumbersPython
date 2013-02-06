'''
Created on 05.02.2013.

@author: igor.crevar
'''
import unittest

import sys
# Add the ptdraft folder path to the sys.path list
sys.path.append('../bignumbers/')

from BigNumber import BigNumber

class Test(unittest.TestCase):

    @staticmethod
    def is_equal(big, string):
        return big.str() == string
    
    @staticmethod
    def is_valid(big):
        return big.length == len(big.digit)
        
    def setUp(self):
        print self.__str__()

    def tearDown(self):
        pass

    def testInit(self):
        a = BigNumber()
        self.assertEqual(a.length == 0 and len(a.digit) == 0, True)
        a.zero()
        self.assertEqual(str(a), '0')
 
    def testZero(self):
        a = BigNumber(-150674)
        self.assertEqual(str(a), '-150674')
        a.parse(5430)
        self.assertEqual(str(a), '5430')
        
    def testAdd(self):
        return
        b1 = BigNumber()
        b2 = BigNumber()
        b3 = None
        invalid = False;
        for i in xrange(-364, 164):
            if (invalid):
                break;
            for j in xrange(-34, 56):
                b1.parse(i)
                b2.parse(j)
                b3 = b1 + b2
                bstr = str(b3)
                vstr = str(i + j)
                if (bstr != vstr) :
                    invalid = True
                    break
        self.assertEqual(invalid, False, 
                    "should be {0} but its {1} for {2} {3} (big: {4} and {5})".
                        format(vstr, bstr, i, j, b1, b2))

    def testShiftLeft(self):
        b = BigNumber(125)
        b.shift_left(1)
        self.assertEqual(str(b), '1250')
        b.shift_left(3)
        self.assertEqual(str(b), '1250000')
        b.parse(0)
        b.shift_left(3)
        self.assertEqual(b.is_zero(), True)
        
    def testShiftRight(self):
        b = BigNumber([5, 2, 1])
        b.shift_right(1)
        self.assertEqual(str(b), '12')
        b.shift_right(1)
        self.assertEqual(str(b), '1')
        b.shift_right(1)
        self.assertEqual(str(b), '0')
        
    def testSplit(self):
        a = BigNumber(1257892)
        (b1, b2, n1, b1b2len) = a.split()
        val = str(b1) == '125'
        val = val and str(b2) == '7892'
        val = val and n1 == 4
        val = val and b1b2len == 7
        self.assertEqual(val, True)
        
    def testMultiply(self):
        x = 3564591
        y = 278034
        b1 = BigNumber(x)
        b2 = BigNumber(y)
        b3 = b1 * b2
        z  = x * y
        str1 = str(b3)
        str2 = str(z)
        self.assertEqual(str1 == str2, True, \
                         "Its {0} but it should be {1}".format(str1, str2))   

if __name__ == "__main__":
    #import sys; sys.argv = ['', 'Test.testName']
    unittest.main()