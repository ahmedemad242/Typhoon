from vpython import vector

#class which hold 3D vector in space
class Vector:

    #intialize a vector with its position x, y, and z
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    #treat vector as 1D array where we can use Vector[0] to return first element hence X
    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            return self.z
    
    #Invert vector to opposite direction
    def invert(self):
        self.x = - self.x
        self.y = - self.y
        self.z = - self.z

    
    #overloading *= operator in multiplication of vector with a scalar
    def __imul__(self, value):
        self.x *= value
        self.y *= value
        self.z *= value
        return self

    #overload * operation to return a vector multiplication of vector with scalar
    def __mul__(self,value):
        if isinstance(value, Vector):
            return self.x*value.x + self.y*value.y + self.z*value.z
        else:
            return Vector(self.x*value,self.y*value,self.z*value)

    #overload += operation to add two vectors 
    def __iadd__(self, vector):
        self.x += vector.x
        self.y += vector.y
        self.z += vector.z
        return self
    
    #overload + operation and return a vector of addition of two original vectors
    def __add__(self, vector):
        return Vector(self.x + vector.x,self.y + vector.y,self.z + vector.z)

    #overload -= operation to sub two vectors 
    def __isub__(self, vector):
        self.x -= vector.x
        self.y -= vector.y
        self.z -= vector.z
        return self
    
    #overload - operation and return a vector of sub of two original vectors
    def __sub__(self, vector):
        return Vector(self.x - vector.x,self.y - vector.y,self.z - vector.z)

    #Add scaled vector to current vector
    def addScaledVector(self, vector, value):
        self.x += vector.x * value
        self.y += vector.y * value
        self.z += vector.z * value

    #evaluate the component wise product and store it in the vector
    def updateComponentProduct(self, vector):
        self.x *= vector.x;
        self.y *= vector.y;
        self.z *= vector.z;	

    #return a copy vector of the component wise product
    def componentProduct(self, vector):
        return Vector(self.x * vector.x,self.y * vector.y,self.z * vector.z)

    #return scaler product 
    def scalarProduct(self, vector):
        return self.x * vector.x + self.y * vector.y + self.z * vector.z

    #evaluate the vector  product and store it in the vector
    def updateVectorProduct(self, vector):
        self.x = y * vector.z - vector.y * z;
        self.y = z * vector.x - vector.z * x;
        self.z = x * vector.y - vector.x * y;
        
    #return a copy vector of the vector product
    def vectorProduct(self,vector):
        return Vector(self.y * vector.z - vector.y * self.z, self.z * vector.x - vector.z * self.x, self.x * vector.y - vector.x * self.y);

    #overload % opertation to return a copy vector of vector product
    def __mod__(self, vector):
        return self.vectorProduct(vector)

    #return magnitude of vector
    def magnitude(self):
        return (self.x**2+self.y**2+self.z**2)**(1/2)

    #return square of magnitude of vector 
    def squareMagnitude(self):
        return self.x**2+self.y**2+self.z**2

    #change non zero vector to unit vectors
    def normalize(self):
        l = self.magnitude()
        if l > 0:
            self *= (1/l)


    #return a normalized version of vector
    def unit(self):
        x = Vector(self.x,self.y,self.z)
        x.normalize()
        return x

    #limit vector to a certain value
    def trim(self, size):
        if self.squareMagnitude > size*size:
            self.normalize()
            self.x *= size
            self.y *= size
            self.z *= size
    
    #clears vector to 0,0,0
    def clear(self ):
        self.x = 0
        self.y = 0
        self.z = 0

    #return a copy of the vector
    def copy(self):
        return Vector(self.x,self.y,self.z)


    #return true if two vectors are equal (element by element comparison)
    def __eq__(self,vector):
        return self.x == vector.x and self.y == vector.y and self.z == vector.z


	#Return true if two vectors are not equal
	#element by element comparison 
    def __ne__(self,vector):
        return x != vector.x or self.y != vector.y or self.z != vector.z

	#Return true if the first vector is smaller than the second vector
	#This is not a single value comparison meaning that !(a <= b) doesnt imply a > b
    def __lt__(self,vector):
        return self.x < vector.x  and self.y < vector.y  and self.z < vector.z

	#Return true if the first vector is smaller than or equal than the second vector
	#This is not a single value comparison
    def __le__(self,vector):
        return self.x <= vector.x and self.y <= vector.y and self.z <= vector.z

	#Return true if the first vector is larger than the second vector
	#This is not a single value comparison
    def __gt__(self,vector):
        return self.x > vector.x and self.y > vector.y and self.z > vector.z

	#Return true if the first vector is larger than or equal than the second vector
	#This is not a single value comparison
    def __ge__(self,vector):
        return self.x >= vector.x  and self.y >= vector.y  and self.z >= vector.z

    def set(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

    def toVPython(self):
        return vector(self.x, self.y, self.z)

    def __str__(self):
        return str(self.x) + " " + str(self.y) + " " + str(self.z)