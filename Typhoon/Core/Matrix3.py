from Typhoon.Core.Vector import Vector

class Matrix3:
    '''
        Class responsible for representing a 3x3 Matrix
        ---------
        properties:
            data - List - hold 9 components of matrix in 1D array
        ---------
        methods:
            setComponent            -   Set matrix components from 3 vectors
            vectorProduct           -   Multiply current matrix with another one
            setInertiaTensorCoeffs  -   Set matrix value from inertia tensor values
            setDiagonal             -   Set matrx to be a diagonal matrix
            setBlockInertiaTensor   -   Sets the value of the matrix as an inertia tensor of a rectangular block
            setSkewSymmetric        -   Set matrix to be a skew symmetric matrix from a vector
            transform               -   Transform a vector by this matrix
            transformTranspose      -   Transform a vector by transpose of this matrix
            getRowVector            -   Return a vector representing a row in matrix
            getAxisVector           -   Return a vector representing a column in this matrix
            setInverse              -   Set current matrix by inverse of input matrix
            inverse                 -   Return a new matrix which is inverse of current
            invert                  -   invert current matrix
            setTranspose            -   Set matrix by transpose of a given matrix matrix
            transpose               -   Return the transpose of this matrix  
            setOrientation          -   Set matrix to be a rotational matrix of a quaternion
            linearInterpolate       -   Return a matrix with interploation of 2 other matrices
            copy                    -   Return a deep copied version of current matrix
        ---------
        opertaion overload:
            *=  -   multiply current matrix by a scaler or matrix
            *   -   Returns matrix3 or a vector depending on input
            +=  -   adds a matrix to current matrix
    '''
     
    
    def __init__(self, d0 = 0, d1 = 0, d2 = 0, d3 = 0, d4 = 0, d5 = 0, d6 = 0, d7 = 0, d8 = 0):
        '''
            Class constractor
            ---------
            args:
                d0-d8 - double = 0 - represent 9 components of 3x3 Matrix, filled as rows
        '''

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

    def setComponent(self, compOne , compTwo , compThree):
        '''
            Set data of tensor from three component vector
                v1.x  v2.x  v3.x
                v1.y  v2.y  v3.y
                v1.z  v2.z  v3.z
            ---------
            args:
                compOne - Vector
                compTwo - Vector
                compThree - Vector
        '''

        self.data[0] = compOne.x
        self.data[1] = compTwo.x
        self.data[2] = compThree.x;
        self.data[3] = compOne.y
        self.data[4] = compTwo.y
        self.data[5] = compThree.y
        self.data[6] = compOne.z
        self.data[7] = compTwo.z
        self.data[8] = compThree.z

    def __mul__(self,o):
        '''
            operation overload for * operator 
                - returns a 3x3 Matrix if o is Matrix3
                - return a vector if o is a Vector
            ---------
            args:
                o - Matrix3
                o - Vector 
        '''

        if isinstance(o, Matrix3):
            return Matrix3(\
                self.data[0]*o.data[0] + self.data[1]*o.data[3] + self.data[2]*o.data[6],\
                self.data[0]*o.data[1] + self.data[1]*o.data[4] + self.data[2]*o.data[7],\
                self.data[0]*o.data[2] + self.data[1]*o.data[5] + self.data[2]*o.data[8],\

                self.data[3]*o.data[0] + self.data[4]*o.data[3] + self.data[5]*o.data[6],\
                self.data[3]*o.data[1] + self.data[4]*o.data[4] + self.data[5]*o.data[7],\
                self.data[3]*o.data[2] + self.data[4]*o.data[5] + self.data[5]*o.data[8],\

                self.data[6]*o.data[0] + self.data[7]*o.data[3] + self.data[8]*o.data[6],\
                self.data[6]*o.data[1] + self.data[7]*o.data[4] + self.data[8]*o.data[7],\
                self.data[6]*o.data[2] + self.data[7]*o.data[5] + self.data[8]*o.data[8]
                )   
        else:
             return Vector(\
                o.x * self.data[0] + o.y * self.data[1] + o.z * self.data[2],\
                o.x * self.data[3] + o.y * self.data[4] + o.z * self.data[5],\
                o.x * self.data[6] + o.y * self.data[7] + o.z * self.data[8])

    def __iadd__(self,o):
        '''
            operation overload for += operator adds a matrix to current matrix
            ---------
            args:
                o - Matrix3
        '''

        self.data[0] += o.data[0]
        self.data[1] += o.data[1]
        self.data[2] += o.data[2]
        self.data[3] += o.data[3]
        self.data[4] += o.data[4]
        self.data[5] += o.data[5]
        self.data[6] += o.data[6]
        self.data[7] += o.data[7]
        self.data[8] += o.data[8]
        return self

    def __imul__(self,o):
        '''
            operation overload for *= operator for matrix multiplication 
            ---------
            args:
                o - Matrix3
                o - double 
        '''

        if isinstance(o, Matrix3):
            t1 = self.data[0]* o.data[0] + self.data[1]* o.data[3] + self.data[2]* o.data[6]
            t2 = self.data[0]* o.data[1] + self.data[1]* o.data[4] + self.data[2]* o.data[7]
            t3 = self.data[0]* o.data[2] + self.data[1]* o.data[5] + self.data[2]* o.data[8]
            self.data[0] = t1
            self.data[1] = t2
            self.data[2] = t3

            t1 = self.data[3]* o.data[0] + self.data[4]* o.data[3] + self.data[5]* o.data[6]
            t2 = self.data[3]* o.data[1] + self.data[4]* o.data[4] + self.data[5]* o.data[7]
            t3 = self.data[3]* o.data[2] + self.data[4]* o.data[5] + self.data[5]* o.data[8]
            self.data[3] = t1
            self.data[4] = t2
            self.data[5] = t3

            t1 = self.data[6]* o.data[0] + self.data[7]* o.data[3] + self.data[8]* o.data[6]
            t2 = self.data[6]* o.data[1] + self.data[7]* o.data[4] + self.data[8]* o.data[7]
            t3 = self.data[6]* o.data[2] + self.data[7]* o.data[5] + self.data[8]* o.data[8]
            self.data[6] = t1
            self.data[7] = t2
            self.data[8] = t3
        else:
            self.data[0] *= o
            self.data[1] *= o
            self.data[2] *= o
            self.data[3] *= o
            self.data[4] *= o
            self.data[5] *= o
            self.data[6] *= o
            self.data[7] *= o
            self.data[8] *= o
        return self

    def vectorProduct(self, matrix):
        '''
            Multiply current matrix with another one
            ---------
            args:
                matrix - Matrix3
        '''

        t1 = self.data[0]*matrix.data[0] + self.data[1]*matrix.data[3] + self.data[2]*matrix.data[6]
        t2 = self.data[0]*matrix.data[1] + self.data[1]*matrix.data[4] + self.data[2]*matrix.data[7]
        t3 = self.data[0]*matrix.data[2] + self.data[1]*matrix.data[5] + self.data[2]*matrix.data[8]

        self.data[0] = t1
        self.data[1] = t2
        self.data[2] = t3

        t1 = self.data[3]*matrix.data[0] + self.data[4]*matrix.data[3] + self.data[5]*matrix.data[6]
        t2 = self.data[3]*matrix.data[1] + self.data[4]*matrix.data[4] + self.data[5]*matrix.data[7]
        t3 = self.data[3]*matrix.data[2] + self.data[4]*matrix.data[5] + self.data[5]*matrix.data[8]

        self.data[3] = t1
        self.data[4] = t2
        self.data[5] = t3

        t1 = self.data[6]*matrix.data[0] + self.data[7]*matrix.data[3] + self.data[8]*matrix.data[6]
        t2 = self.data[6]*matrix.data[1] + self.data[7]*matrix.data[4] + self.data[8]*matrix.data[7]
        t3 = self.data[6]*matrix.data[2] + self.data[7]*matrix.data[5] + self.data[8]*matrix.data[8]

        self.data[6] = t1
        self.data[7] = t2
        self.data[8] = t3

    def setInertiaTensorCoeffs(self, ix, iy, iz, ixy=0, ixz=0, iyz=0):
        '''
            Set matrix value from inertia tensor values
            ---------
            args:
                ix  - double
                iy  - double
                iz  - double
                ixy - double = 0
                ixz - double = 0
                iyz - double = 0
        '''

        self.data[0] = ix
        self.data[1] = self.data[3] = -ixy
        self.data[2] = self.data[6] = -ixz
        self.data[4] = iy
        self.data[5] = self.data[7] = -iyz
        self.data[8] = iz
       
    def setDiagonal(self, a, b, c):
        '''
            Set matrx to be a diagonal matrix
            ---------
            args:
                a  - double
                b  - double
                c  - double
        '''

        self.setInertiaTensorCoeffs(a, b, c)

    def setBlockInertiaTensor(self, halfSizes, mass):
        '''
            Sets the value of the matrix as an inertia tensor of a rectangular block aligned with the body's coordinate
            system with the given axis half-sizes and mass.
            ---------
            args:
                halfSizes - Vector  
                mass      - double  
        '''
        
        squares = halfSizes.componentProduct(halfSizes)
        self.setInertiaTensorCoeffs(0.3*mass*(squares.y + squares.z), 0.3*mass*(squares.x + squares.z), 0.3*mass*(squares.x + squares.y))

    def setSkewSymmetric(self, vector):
        '''
            Set matrix to be a skew symmetric matrix from a vector
            ---------
            args:
                vector - Vector   
        '''

        self.data[0] = self.data[4] = self.data[8] = 0
        self.data[1] = -vector.z
        self.data[2] = vector.y
        self.data[3] = vector.z
        self.data[5] = -vector.x
        self.data[6] = -vector.y
        self.data[7] = vector.x
       
    def transform(self, vector):
        '''
            Transform a vector by this matrix
            ---------
            args:
                vector - Vector   
        '''

        return self * vector
        
    def transformTranspose(self,vector):
        '''
            Transform a vector by transpose of this matrix
            ---------
            args:
                vector - Vector   
        '''

        return Vector(
            vector.x * self.data[0] + vector.y * self.data[3] + vector.z * self.data[6], 
            vector.x * self.data[1] + vector.y * self.data[4] + vector.z * self.data[7], 
            vector.x * self.data[2] + vector.y * self.data[5] + vector.z * self.data[8])
           
    def getRowVector(self, i):
        '''
            return a vector representing row i in this matrix
            ---------
            args:
                i - int - number of row to return    
        '''

        return Vector(self.data[i*3], self.data[i*3+1], self.data[i*3+2])
        
    def getAxisVector(self, i):
        '''
            return a vector representing an a column in this matrix
            ---------
            args:
                i - int - number of column to return    
        '''

        return Vector(self.data[i], self.data[i+3], self.data[i+6])

    def setInverse(self, m):
        '''
            Set current matrix by inverse of m
            ---------
            args:
                m - Matrix3    
        '''

        t4 = m.data[0]*m.data[4]
        t6 = m.data[0]*m.data[5]
        t8 = m.data[1]*m.data[3]
        t10 = m.data[2]*m.data[3]
        t12 = m.data[1]*m.data[6]
        t14 = m.data[2]*m.data[6]

        #determinant    
        t16 = (t4*m.data[8] - t6*m.data[7] - t8*m.data[8]+
                t10*m.data[7] + t12*m.data[5] - t14*m.data[4])

        #singular matrix
        if t16 == 0: 
            return
        t17 = 1/t16

        self.data[0] = (m.data[4]*m.data[8]-m.data[5]*m.data[7])*t17
        self.data[1] = -(m.data[1]*m.data[8]-m.data[2]*m.data[7])*t17
        self.data[2] = (m.data[1]*m.data[5]-m.data[2]*m.data[4])*t17
        self.data[3] = -(m.data[3]*m.data[8]-m.data[5]*m.data[6])*t17
        self.data[4] = (m.data[0]*m.data[8]-t14)*t17
        self.data[5] = -(t6-t10)*t17
        self.data[6] = (m.data[3]*m.data[7]-m.data[4]*m.data[6])*t17
        self.data[7] = -(m.data[0]*m.data[7]-t12)*t17
        self.data[8] = (t4-t8)*t17

    def inverse(self):
        '''
            return a new inverse matrix 
        '''

        result = Matrix3()
        result.setInverse(self)
        return result
        
    def invert(self):
        '''
            invert current matrix
        '''

        self.setInverse(self)
        
    def setTranspose(self,m):
        '''
            Set matrix by transpose of a given matrix m
            ---------
            args:
                m - Matrix3    
        '''

        self.data[0] = m.data[0]
        self.data[1] = m.data[3]
        self.data[2] = m.data[6]
        self.data[3] = m.data[1]
        self.data[4] = m.data[4]
        self.data[5] = m.data[7]
        self.data[6] = m.data[2]
        self.data[7] = m.data[5]
        self.data[8] = m.data[8]

    def transpose(self):
        '''
            Return the transpose of this matrix  
        '''
        result = Matrix3()
        result.setTranspose(self)
        return result
        
    def setOrientation(self,q):
        '''
            Set matrix to be a rotational matrix of a quaternion
            ---------
            args:
                q - Quaternion    
        '''

        self.data[0] = 1 - (2*self.q.j*self.q.j + 2*self.q.k*self.q.k)
        self.data[1] = 2*self.q.i*self.q.j + 2*self.q.k*self.q.r
        self.data[2] = 2*self.q.i*self.q.k - 2*self.q.j*self.q.r
        self.data[3] = 2*self.q.i*self.q.j - 2*self.q.k*self.q.r
        self.data[4] = 1 - (2*self.q.i*self.q.i  + 2*self.q.k*self.q.k)
        self.data[5] = 2*self.q.j*self.q.k + 2*self.q.i*self.q.r
        self.data[6] = 2*self.q.i*self.q.k + 2*self.q.j*self.q.r
        self.data[7] = 2*self.q.j*self.q.k - 2*self.q.i*self.q.r
        self.data[8] = 1 - (2*self.q.i*self.q.i  + 2*self.q.j*self.q.j)
        
    def linearInterpolate(a, b, prop):
        '''
            Return a matrix with interploation of 2 other matrices
            ---------
            args:
                a - Vector  
                b - Vector
                prop - interploation value 
        '''

        result = Matrix()
        for i in range(9):
            result.data[i] = a.data[i] * (1-prop) + b.data[i] * prop
        return result;

    def copy(self):
        '''
            Return a deep copied version of current matrix
        '''

        return Matrix3(self.data[0], self.data[1], self.data[2], self.data[3], self.data[4], self.data[5],self.data[6], self.data[7], self.data[8])
        
    def __str__(self):
        i=1
        s = ""
        for data in self.data:
            s += str(data) + " "
            if i%3==0: s+= "\n"
            i+=1
        return s