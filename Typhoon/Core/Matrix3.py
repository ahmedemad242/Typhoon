from Typhoon.Core.Vector import Vector

class Matrix3:
     
     #Creates a new matrix
    def __init__(self, d0 = 0, d1 = 0, d2 = 0, d3 = 0, d4 = 0, d5 = 0, d6 = 0, d7 = 0, d8 = 0):
         
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

    #Set data of tensor from three component vector
    # v1.x  v2.x  v3.x
    # v1.y  v2.y  v3.y
    # v1.z  v2.z  v3.z
    def setComponent(self, compOne , compTwo , compThree):
        self.data[0] = compOne.x
        self.data[1] = compTwo.x
        self.data[2] = compThree.x;
        self.data[3] = compOne.y
        self.data[4] = compTwo.y
        self.data[5] = compThree.y
        self.data[6] = compOne.z
        self.data[7] = compTwo.z
        self.data[8] = compThree.z


    #Overloads * operator where Martrix3 * Matrix3
    def __mul__(self,o):
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



    #Overload += operator for matrix addition
    def __iadd__(self,o):
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

    #Overload *= operator for matrix multiplied by scaler
    def __imul__(self,o):
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


    #Vector multiplicaton of 2 matrices
    def vectorProduct(self, vector):
        t1 = self.data[0]*vector.data[0] + self.data[1]*vector.data[3] + self.data[2]*vector.data[6]
        t2 = self.data[0]*vector.data[1] + self.data[1]*vector.data[4] + self.data[2]*vector.data[7]
        t3 = self.data[0]*vector.data[2] + self.data[1]*vector.data[5] + self.data[2]*vector.data[8]

        self.data[0] = t1
        self.data[1] = t2
        self.data[2] = t3

        t1 = self.data[3]*vector.data[0] + self.data[4]*vector.data[3] + self.data[5]*vector.data[6]
        t2 = self.data[3]*vector.data[1] + self.data[4]*vector.data[4] + self.data[5]*vector.data[7]
        t3 = self.data[3]*vector.data[2] + self.data[4]*vector.data[5] + self.data[5]*vector.data[8]

        self.data[3] = t1
        self.data[4] = t2
        self.data[5] = t3

        t1 = self.data[6]*vector.data[0] + self.data[7]*vector.data[3] + self.data[8]*vector.data[6]
        t2 = self.data[6]*vector.data[1] + self.data[7]*vector.data[4] + self.data[8]*vector.data[7]
        t3 = self.data[6]*vector.data[2] + self.data[7]*vector.data[5] + self.data[8]*vector.data[8]

        self.data[6] = t1
        self.data[7] = t2
        self.data[8] = t3

    #Set matrix value from inertia tensor values
    def setInertiaTensorCoeffs(self, ix, iy, iz, ixy=0, ixz=0, iyz=0):
        self.data[0] = ix
        self.data[1] = self.data[3] = -ixy
        self.data[2] = self.data[6] = -ixz
        self.data[4] = iy
        self.data[5] = self.data[7] = -iyz
        self.data[8] = iz
       
    #Set diagonal of the matrix
    def setDiagonal(self, a, b, c):
        self.setInertiaTensorCoeffs(a, b, c)

     
    #Sets the value of the matrix as an inertia tensor of
    #a rectangular block aligned with the body's coordinate
    #system with the given axis half-sizes and mass.
    def setBlockInertiaTensor(self, halfSizes, mass):
        squares = halfSizes.componentProduct(halfSizes)
        self.setInertiaTensorCoeffs(0.3*mass*(squares.y + squares.z), 0.3*mass*(squares.x + squares.z), 0.3*mass*(squares.x + squares.y))

    #Set matrix to be a skew symmetric matrix from a vector
    def setSkewSymmetric(self, vector):
        self.data[0] = self.data[4] = self.data[8] = 0
        self.data[1] = -vector.z
        self.data[2] = vector.y
        self.data[3] = vector.z
        self.data[5] = -vector.x
        self.data[6] = -vector.y
        self.data[7] = vector.x
       

    #Transform a vector by this matrix
    def transform(self, vector):
        return self * vector
        
        
    #Transform a vector by transpose of this matrix
    def transformTranspose(self,vector):
        return Vector(
            vector.x * self.data[0] + vector.y * self.data[3] + vector.z * self.data[6], 
            vector.x * self.data[1] + vector.y * self.data[4] + vector.z * self.data[7], 
            vector.x * self.data[2] + vector.y * self.data[5] + vector.z * self.data[8])
           
    #return a vector representing row i in this matrix
    def getRowVector(self, i):
        return Vector(self.data[i*3], self.data[i*3+1], self.data[i*3+2])
        
    #return a vector representing an a column in this matrix
    def getAxisVector(self, i):
        return Vector(self.data[i], self.data[i+3], self.data[i+6])

        
    #Set current matrix by its inverse
    def setInverse(self, m):
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

    #return a new inverse matrix
    def inverse(self):
        result = Matrix3()
        result.setInverse(self)
        return result
        
    #invert cureent matrix
    def invert(self):
        self.setInverse(self)
        
    #Set matrix by transpose of a given matrix
    def setTranspose(self,m):
        self.data[0] = m.data[0]
        self.data[1] = m.data[3]
        self.data[2] = m.data[6]
        self.data[3] = m.data[1]
        self.data[4] = m.data[4]
        self.data[5] = m.data[7]
        self.data[6] = m.data[2]
        self.data[7] = m.data[5]
        self.data[8] = m.data[8]

    #Return the transpose of this matrix
    def transpose(self):
        result = Matrix3()
        result.setTranspose(self)
        return result
        
    #Set matrix to be a rotational matrix of a quaternion
    def setOrientation(self,q):
        self.data[0] = 1 - (2*self.q.j*self.q.j + 2*self.q.k*self.q.k)
        self.data[1] = 2*self.q.i*self.q.j + 2*self.q.k*self.q.r
        self.data[2] = 2*self.q.i*self.q.k - 2*self.q.j*self.q.r
        self.data[3] = 2*self.q.i*self.q.j - 2*self.q.k*self.q.r
        self.data[4] = 1 - (2*self.q.i*self.q.i  + 2*self.q.k*self.q.k)
        self.data[5] = 2*self.q.j*self.q.k + 2*self.q.i*self.q.r
        self.data[6] = 2*self.q.i*self.q.k + 2*self.q.j*self.q.r
        self.data[7] = 2*self.q.j*self.q.k - 2*self.q.i*self.q.r
        self.data[8] = 1 - (2*self.q.i*self.q.i  + 2*self.q.j*self.q.j)
        
    #Return a matrix with interploation of 2 other matrices
    def linearInterpolate(a, b, prop):
        result = Matrix()
        for i in range(9):
            result.data[i] = a.data[i] * (1-prop) + b.data[i] * prop
        return result;

    #Return a deep copied version of current matrix
    def copy(self):
        return Matrix3(self.data[0], self.data[1], self.data[2], self.data[3], self.data[4], self.data[5],self.data[6], self.data[7], self.data[8])
        
    def __str__(self):
        i=1
        s = ""
        for data in self.data:
            s += str(data) + " "
            if i%3==0: s+= "\n"
            i+=1
        return s