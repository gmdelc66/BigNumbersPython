'''
Created on 05.02.2013.

@author: igor.crevar
'''

class BigNumber(object):
    '''
    classdocs
    '''
    digit = []
    is_negative = False
    length = 0
    
    def __init__(self, number = None, ):
        '''
        Constructor
        '''
        if number is not None:
            if isinstance(number, list):
                self.digit = number
                self.is_negative = False
                self.length = len(number)
            elif isinstance(number, BigNumber):
                self.copyfrom(number)
            else:    
                self.parse(number)
        else:
            self.digit = []
            self.is_negative = False
            self.length = 0
    
    '''
    Defines zero 
    '''
    def zero(self):
        self.is_negative = False
        self.length = 1;
        self.digit = [0]
        return self
    
    def copyfrom(self, other):
        self.digit = list(other.digit)
        self.is_negative = other.is_negative
        self.length = other.length
    
    def is_valid(self):
        return self.length == len(self.digit)
    
    def is_zero(self):
        return self.length == 1 and len(self.digit) == 1 and self.digit[0] == 0
    
    def parse(self, number):
        if (number == 0):
            self.zero()
            return
        elif number < 0:
            number = -number
            self.is_negative = True
        else:
            self.is_negative = False
       
        self.digit = []
        while number > 0:
            self.digit.append(number % 10)
            number //= 10
        
        self.length = len(self.digit)
         
    def __str__(self, *args, **kwargs):
        if (self.length != len(self.digit)):
            return "invalid"
        if (self.length == 0):
            return "undefined"
        digit_holder = []
        if self.is_negative:
            digit_holder.append('-')
        for i in reversed(xrange(0, len(self.digit))):
            number = self.digit[i]
            char = chr(number + ord('0'))
            digit_holder.append(char)
        return ''.join(digit_holder)
            
    def are_same_sign(self, other):
        return (self.is_negative ^ other.is_negative) == False
        
    def __cmp__(self, other):
        if not self.are_same_sign(other):
            return -1 if self.is_negative else 1
        elif self.length > other.length:
            return 1
        elif self.length < other.length:
            return -1
        else:
            i = self.length - 1;
            while i >= 0 and self.digit[i] == other.digit[i]:
                i -= 1
            if i < 0:
                return 0
            else:
                return 1 if self.digit[i] > other.digit[i] else -1
    
    '''
    Add two big number, operator +
    '''
    def __add__(self, other):
        #def __radd__(self, other):
        # sub if not same sign
        if not self.are_same_sign(other):
            return self._sub(other)
        
        ret = BigNumber()
        add = 0
        i = 0
        
        # 1st
        minlen = self.length if self.length <= other.length else other.length
        while i < minlen:
            add += self.digit[i] + other.digit[i]
            ret.digit.append(add % 10)
            add //= 10
            i += 1

        # 2nd
        tmp = self if self.length >= other.length else other
        while i < tmp.length:
            add += tmp.digit[i];
            ret.digit.append(add % 10)
            add //= 10
            i += 1
        
        # 3rd
        while add > 0:
            ret.digit.append(add % 10)
            add //= 10
        
        ret.is_negative = self.is_negative
        ret.length = len(ret.digit)
        return ret
        
    def _sub(self, other):
        ret = BigNumber()
        # first one must be greater by absolute value
        # must make numbers absolute and then rollback old value
        old_self_is_negative = self.is_negative
        old_other_is_negative = other.is_negative
        self.is_negative = False
        other.is_negative = False
        cmp_val = self.__cmp__(other)
        self.is_negative = old_self_is_negative
        other.is_negative = old_other_is_negative
        #end compare
        
        # are they same just return zero value
        if cmp_val == 0:
            return ret.zero()
            
        a = self
        b = other            
        if cmp_val == -1:
            a = other
            b = self
        
        add = 0;
        for i in xrange(0, a.length):
            sub = b.digit[i] if b.length > i else 0
            diff = a.digit[i] - sub - add
            add = 0
            if diff < 0:
                while diff < 0:
                    add += 1
                    diff += 10 
            
            ret.digit.append(diff % 10);        
   
        # update length
        ret.length = len(ret.digit)
        
        # fix length
        for i in reversed(xrange(0, ret.length)):
            if ret.digit[i] > 0:
                break
            else:
                ret.length -= 1
        
        # slice digits
        ret.digit = ret.digit[0:ret.length]
        # sign of first operand is sign of returned bn
        ret.is_negative = a.is_negative
    
        # fix if length is zero
        if ret.length < 1:
            ret.zero()
        
        return ret
    
    def shift_left(self, power):
        # can not shift zero!
        if (self.is_zero()):
            return self
        self.length += power
        for i in xrange(0, power):
            self.digit.insert(0, 0)
        return self 
            
    def shift_right(self, power):
        if (power >= self.length):
            return self.zero()
        
        self.digit = self.digit[power:]
        self.length -= power
        return self
    
    def split(self):
        n = self.length
        n2 = n // 2 + n % 2
        if (n2 < self.length) :
            b1 = BigNumber(self.digit[n2:])
            b2 = BigNumber(self.digit[:n2])
        else:
            b1 = BigNumber(0)
            b2 = BigNumber(self.digit[:n2])
        return (b1, b2, n2, n)
    
    @staticmethod
    def _multiple(x, y):
        (a, b, n1, digits1) = x.split()
        (c, d, n2, digits2) = y.split()
        if digits1 <= 1 and digits2 <= 1:
            val1 = b.digit[0] if digits1 == 1 else 0
            val2 = d.digit[0] if digits1 == 1 else 0
            return BigNumber(val1 * val2)
        
        ac = BigNumber._multiple(a, c).shift_left(n1 + n2)
        ad = BigNumber._multiple(a, d).shift_left(n1)
        bc = BigNumber._multiple(b, c).shift_left(n2)
        bd = BigNumber._multiple(b, d)
        return ac + ad + bc + bd
    
    def __mul__(self, other):
        x = BigNumber(self)
        y = BigNumber(other)
        x.is_negative = False
        y.is_negative = False
        val = BigNumber._multiple(x, y)
        val.is_negative = not self.are_same_sign(other)
        return val
        
        
        
        