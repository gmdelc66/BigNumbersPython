'''
Created on 05.02.2013.

@author: igor.crevar
'''
from bignumbers.BigNumber import BigNumber
import math

def digits(x):
    # return int(math.log10(x))+1
    return len(str(x))

def get(x):
    n = digits(x)
    n2 = n // 2 + n % 2
    div = math.pow(10, n2)
    div = long(div)
    v = (x // div, x % div, n2, n)
    return v

def mul(x, y):
    #if x == 0 or y == 0:
    #   return 0l
    (a, b, n1, digits1) = get(x)
    (c, d, n2, digits2) = get(y)
    #print "({0}, {1}, {2}) ({3}, {4}, {5})".format(a, b, n1, c, d, n2)
    if digits1 <= 1 and digits2 <= 1:
        #print "{0}. {1}, {2}, {3}".format(a, b, c, d)
        return b * d
    
    powab = long(math.pow(10, n1 + n2))
    powad = long(math.pow(10, n1))
    powbc = long(math.pow(10, n2))
    number = powab * mul(a, c) + \
             powad * mul(a, d) + \
             powbc * mul(b, c) + \
                     mul(b, d)
    
    return number

if __name__ == '__main__':
    a = 3412354435
    b = 45356461
    print mul(a, b)
    print a * b
    a = BigNumber(2359)
    b = BigNumber(a)
    print b
    a = BigNumber(134583)
    c = b * a
    print c
    print 134583 * 2359