from Typhoon.Core.Vector import Vector
from Typhoon.Core.Quaternion import Quaternion

#Trasform matrix of size 3x4 where rest is assumed to be 0,0,0,1
#it hold a rotation matrix and a position
class Matrix4:

    def __init__(self, d0 = 1, d1 = 0,d2 = 0, d3 = 0,d4 = 0, d5 = 1,d6 = 0, d7 = 0,d8 = 0, d9=0, d10=1, d11=0):
        #Holds matrix data in array form
        self.data = []  
        self.data.append(d0)
        self.data.append(d1)
        self.data.append(d2)
        self.data.append(d3)
        self.data.append(d4)
        self.data.append(d5)
        self.data.append(d6)
        self.data.append(d7)
        self.data.append(d8)
        self.data.append(d9)
        self.data.append(d10)
        self.data.append(d11)

    #Set diagonal of rotational matrix
    def setDiagonal(self,a,b,c):
        self.data[0] = self.a
        self.data[1] = self.b
        self.data[2] = self.c

    #Return a new matrix bulit by multplying this matrix with a given matrix
    #or
    #Return a new vector built by multiplying this matrix with a given vector
    def __mul__(self,o):
        if isinstance(o, Matrix4):
            result  = Matrix4()
            result.data[0] = (o.data[0]*self.data[0]) + (o.data[4]*self.data[1]) + (o.data[8]*self.data[2])
            result.data[4] = (o.data[0]*self.data[4]) + (o.data[4]*self.data[5]) + (o.data[8]*self.data[6])
            result.data[8] = (o.data[0]*self.data[8]) + (o.data[4]*self.data[9]) + (o.data[8]*self.data[10])

            result.data[1] = (o.data[1]*self.data[0]) + (o.data[5]*self.data[1]) + (o.data[9]*self.data[2])
            result.data[5] = (o.data[1]*self.data[4]) + (o.data[5]*self.data[5]) + (o.data[9]*self.data[6])
            result.data[9] = (o.data[1]*self.data[8]) + (o.data[5]*self.data[9]) + (o.data[9]*self.data[10])

            result.data[2] = (o.data[2]*self.data[0]) + (o.data[6]*self.data[1]) + (o.data[10]*self.data[2])
            result.data[6] = (o.data[2]*self.data[4]) + (o.data[6]*self.data[5]) + (o.data[10]*self.data[6])
            result.data[10] = (o.data[2]*self.data[8]) + (o.data[6]*self.data[9]) + (o.data[10]*self.data[10])

            result.data[3] = (o.data[3]*self.data[0]) + (o.data[7]*self.data[1]) + (o.data[11]*self.data[2]) + self.data[3]
            result.data[7] = (o.data[3]*self.data[4]) + (o.data[7]*self.data[5]) + (o.data[11]*self.data[6]) + self.data[7]
            result.data[11] = (o.data[3]*self.data[8]) + (o.data[7]*self.data[9]) + (o.data[11]*self.data[10]) + self.data[11]

            return result
        else:
            return Vector(
                o.x * self.data[0] +
                o.y * self.data[1] +
                o.z * self.data[2] + self.data[3],

                o.x * self.data[4] +
                o.y * self.data[5] +
                o.z * self.data[6] + self.data[7],

                o.x * self.data[8] +
                o.y * self.data[9] +
                o.z * self.data[10] + self.data[11]
                )

    #Transform the given vector by this matrix.
    def transform(self,vector):
        return self * vector

    def getDeterminant(self):
        return -self.data[8]*self.data[5]*self.data[2]+\
                self.data[4]*self.data[9]*self.data[2]+\
                self.data[8]*self.data[1]*self.data[6]-\
                self.data[0]*self.data[9]*self.data[6]-\
                self.data[4]*self.data[1]*self.data[10]+\
                self.data[0]*self.data[5]*self.data[10]

    #Set this matrix to inverse of a given matrix m
    def setInverse(self, m):
        #Nonzero determine check
        det = self.getDeterminant()
        if (det == 0): return
        det = 1/det

        data[0] = (-m.data[9]*m.data[6]+m.data[5]*m.data[10])*det
        data[4] = (m.data[8]*m.data[6]-m.data[4]*m.data[10])*det
        data[8] = (-m.data[8]*m.data[5]+m.data[4]*m.data[9])*det

        data[1] = (m.data[9]*m.data[2]-m.data[1]*m.data[10])*det
        data[5] = (-m.data[8]*m.data[2]+m.data[0]*m.data[10])*det
        data[9] = (m.data[8]*m.data[1]-m.data[0]*m.data[9])*det

        data[2] = (-m.data[5]*m.data[2]+m.data[1]*m.data[6])*det
        data[6] = (+m.data[4]*m.data[2]-m.data[0]*m.data[6])*det
        data[10] = (-m.data[4]*m.data[1]+m.data[0]*m.data[5])*det

        data[3] = (m.data[9]*m.data[6]*m.data[3]
                   -m.data[5]*m.data[10]*m.data[3]
                   -m.data[9]*m.data[2]*m.data[7]
                   +m.data[1]*m.data[10]*m.data[7]
                   +m.data[5]*m.data[2]*m.data[11]
                   -m.data[1]*m.data[6]*m.data[11])*det
        data[7] = (-m.data[8]*m.data[6]*m.data[3]
                   +m.data[4]*m.data[10]*m.data[3]
                   +m.data[8]*m.data[2]*m.data[7]
                   -m.data[0]*m.data[10]*m.data[7]
                   -m.data[4]*m.data[2]*m.data[11]
                   +m.data[0]*m.data[6]*m.data[11])*det
        data[11] =(m.data[8]*m.data[5]*m.data[3]
                   -m.data[4]*m.data[9]*m.data[3]
                   -m.data[8]*m.data[1]*m.data[7]
                   +m.data[0]*m.data[9]*m.data[7]
                   +m.data[4]*m.data[1]*m.data[11]
                   -m.data[0]*m.data[5]*m.data[11])*det

    #Return a new matrix of inverse of this matrix
    def inverse(self):
        result = Matrix4()
        result.setInverse(self)
        return result

    #Set this matrix to its inverse
    def invert(self):
        self.setInverse(self)

    #Return a new vector of the transform of the given direction vector by this matrix.
    def transformDirection(self,vector):
        return Vector(
            vector.x * self.data[0] +
            vector.y * self.data[1] +
            vector.z * self.data[2],

            vector.x * self.data[4] +
            vector.y * self.data[5] +
            vector.z * self.data[6],

            vector.x * self.data[8] +
            vector.y * self.data[9] +
            vector.z * self.data[10]
            )

    #Return a new vector of the transform of the given direction vector by inverse of this matrix.
    #It is assumed that this matrix is a pure rotation matrix
    #meaning that its inverse is the transpose
    def transformInverseDirection(self,vector):
        return Vector(
                vector.x * self.data[0] +
                vector.y * self.data[4] +
                vector.z * self.data[8],

                vector.x * self.data[1] +
                vector.y * self.data[5] +
                vector.z * self.data[9],

                vector.x * self.data[2] +
                vector.y * self.data[6] +
                vector.z * self.data[10]
                )

    #Return a new vector of the transform of the given direction vector by transformational inversen of this matrix
    #It is assumed that this matrix is a pure rotation matrix
    #meaning that its inverse is the transpose
    def transformInverse(self,vector):
        tmp = Vector(vector.x,vector.y,vector.z)
        tmp.x -= self.data[3];
        tmp.y -= self.data[7];
        tmp.z -= self.data[11];
        return Vector(
            tmp.x * self.data[0] +
            tmp.y * self.data[4] +
            tmp.z * self.data[8],

            tmp.x * self.data[1] +
            tmp.y * self.data[5] +
            tmp.z * self.data[9],

            tmp.x * self.data[2] +
            tmp.y * self.data[6] +
            tmp.z * self.data[10]
            )

    #Return a new vector representing a column in this matrix
    def getAxisVector(self,i):
        return Vector(self.data[i], self.data[i+4], self.data[i+8])

    # Sets this matrix to be the rotation matrix corresponding to  the given quaternion.
    def setOrientationAndPos(self,q,pos):
        self.data[0] = 1 - (2*q.j*q.j + 2*q.k*q.k);
        self.data[1] = 2*q.i*q.j + 2*q.k*q.r;
        self.data[2] = 2*q.i*q.k - 2*q.j*q.r;
        self.data[3] = pos.x;

        self.data[4] = 2*q.i*q.j - 2*q.k*q.r;
        self.data[5] = 1 - (2*q.i*q.i  + 2*q.k*q.k);
        self.data[6] = 2*q.j*q.k + 2*q.i*q.r;
        self.data[7] = pos.y;

        self.data[8] = 2*q.i*q.k + 2*q.j*q.r;
        self.data[9] = 2*q.j*q.k - 2*q.i*q.r;
        self.data[10] = 1 - (2*q.i*q.i  + 2*q.j*q.j);
        self.data[11] = pos.z;





    def copy(self):
        return Matrix4(self.data[0], self.data[1], self.data[2], self.data[3],
                       self.data[4], self.data[5], self.data[6], self.data[7],
                       self.data[8], self.data[9], self.data[10], self.data[11]
                       )
    
    def __str__(self):
        i=1
        s = ""
        for data in self.data:
            s += str(data) + " "
            if i%3==0: s+= "\n"
            i+=1
        return s