from Typhoon.Core.Constants import *

class Quaternion:
    '''
        Class responsible for representing a 3x3 Matrix
        ---------
        properties:
            data - List - hold 9 components of matrix in 1D array
        ---------
        methods:
            setComponent    -  Set matrix components from 3 vectors
            normalize       -  normalizes quartenion
            addScaledVector -  Add a scaled vector to the quaternion
            rotateByVector  -  rotate quaternion by current vector

        ---------
        opertaion overload:
            *=  -   multiply current quaternion by another quaternion
    '''

    ##Initialize zero rotation quaternion
    def __init__(self,r = 1,i = 0,j = 0,k = 0):
        '''
            Class constractor
        ---------
            args:
                r - double = 0 
                i - double = 0
                j - double = 0
                k - double = 0
        '''
        self.r = r
        self.i = i
        self.j = j
        self.k = k

    def setComponent(self,r,i,j,k):
        '''
            Sets quaternion rotation components
            ---------
            args:
                r - double
                i - double 
                j - double 
                k - double
        '''

        self.r = r
        self.i = i
        self.j = j
        self.k = k

    #normalizes quartenion
    def normalize(self):
        '''
            normalizes quartenion
        '''

        d = self.r*self.r+self.i*self.i+self.j*self.j+self.k*self.k

        if d<REAL_EPSILON:
            self.r = 1
            return
        d = 1/d**0.5
        self.r *= d
        self.i *= d
        self.j *= d
        self.k *= d

    def __imul__(self, multiplier):
        '''
            operation overload for *= operator for quartenion 
            ---------
            args:
                multiplier - double
        '''
        
        r = self.r*multiplier.r - self.i*multiplier.i - self.j*multiplier.j - self.k*multiplier.k
        i = self.r*multiplier.i + self.i*multiplier.r + self.j*multiplier.k - self.k*multiplier.j
        j = self.r*multiplier.j + self.j*multiplier.r + self.k*multiplier.i - self.i*multiplier.k
        k = self.r*multiplier.k + self.k*multiplier.r + self.i*multiplier.j - self.j*multiplier.i
        self.r = r
        self.i = i
        self.j = j
        self.k = k
        return self

        
    def addScaledVector(self, vector, scale):
        '''
            Add a scaled vector to the quaternion
            ---------
            args:
                vector - Vector
                scale  - double
        '''
        q = Quaternion(0, vector.x * scale, vector.y * scale, vector.z * scale)
        q *= self;
        self.r += q.r * 0.5
        self.i += q.i * 0.5
        self.j += q.j * 0.5
        self.k += q.k * 0.5

    def rotateByVector(self,vector):
        '''
            rotate quaternion by current vector
            ---------
            args:
                vector - Vector
        '''

        q = Quaternion(0, vector.x, vector.y, vector.z)
        self *= q
        

    def __str__(self):
        return "" +str(self.r) +" + " + str(self.i) + "i + " + str(self.j) + "j + " + str(self.k) + "k"

