from Typhoon.Core.Constants import *

class Quaternion:
       
        ##Initialize zero rotation quaternion
        def __init__(self,r = 1,i = 0,j = 0,k = 0):
            self.r = r
            self.i = i
            self.j = j
            self.k = k

        ##Sets quaternion rotation components
        def setComponent(self,r,i,j,k):
            self.r = r
            self.i = i
            self.j = j
            self.k = k

        #normalizes quartenion
        def normalize(self):

            d = self.r*self.r+self.i*self.i+self.j*self.j+self.k*self.k

            if d<REAL_EPSILON:
                self.r = 1
                return
            d = 1/d**0.5
            self.r *= d
            self.i *= d
            self.j *= d
            self.k *= d

        #Overload *= operator for quartenion
        def __imul__(self, multiplier):
        
            r = self.r*multiplier.r - self.i*multiplier.i - self.j*multiplier.j - self.k*multiplier.k
            i = self.r*multiplier.i + self.i*multiplier.r + self.j*multiplier.k - self.k*multiplier.j
            j = self.r*multiplier.j + self.j*multiplier.r + self.k*multiplier.i - self.i*multiplier.k
            k = self.r*multiplier.k + self.k*multiplier.r + self.i*multiplier.j - self.j*multiplier.i
            self.r = r
            self.i = i
            self.j = j
            self.k = k
            return self

        #Adds scaled vector
        def addScaledVector(self, vector, scale):

            q = Quaternion(0, vector.x * scale, vector.y * scale, vector.z * scale)
            q *= self;
            self.r += q.r * 0.5
            self.i += q.i * 0.5
            self.j += q.j * 0.5
            self.k += q.k * 0.5

        def rotateByVector(self,vector):
            q = Quaternion(0, vector.x, vector.y, vector.z)
            self *= q
        

        def __str__(self):
            return "" +str(self.r) +" + " + str(self.i) + "i + " + str(self.j) + "j + " + str(self.k) + "k"

