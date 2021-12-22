from vpython import vector

class Vector:
    '''
        Class responsible for representing 3D vectors
        ---------
        properties:
            x - double - represent magnitude of vector along x-axis
            y - double - represent magnitude of vector along y-axis
            z - double - represent magnitude of vector along z-axis
        ---------
        methods:
            setters & getters
            invert                  -   Invert vector to opposite direction
            clear                   -   set vector to 0,0,0
            trim                    -   limit vector magnitude to a certain value
            unit                    -   Return a new normalized vector
            normalize               -   normalize currrent vector if non zero
            addScaledVector         -   Add scaled vector to current vector
            updateComponentProduct  -   Evaluate the component wise product and store it in the vector
            updateVectorProduct     -   evaluate the vector  product and store it in the vector
            toVPython               -   Return a vector which is used by the graphics library
            copy                    -   Return a copy of current vector
            squareMagnitude         -   Return square magnitude of current vector
            magnitude               -   Return magnitude of current vector
            vectorProduct           -   Return a copy vector of the vector product
            componentProduct        -   Return a copy vector of the component wise product
            scalarProduct           -   Return scaler product
        ---------
        opertaion overload:
            []  -   treats vector as 1D array
            *=  -   Multiplication of vector with a scalar 
            *   -   Returns a scalar multiplication or a new scaled vector depending on input
            +=  -   add a vector to current one
            +   -   Return a vector of addition of two original vectors
            -=  -   subtract a vector from current 
            -   -   Return a vector of sub of two original vectors
            %   -   Return a new vector vector product
            =   -   Return true if two vectors are equal
            =   -   Return true if two vectors are not equal
            <   -   Return true if vector is smaller than the second vector (Not single value comparison) 
            <=  -   Return true if vector is smaller than or equal the second vector (Not single value comparison)  
            >   -   Return true if vector is larger than the second vector (Not single value comparison) 
            >=  -   Return true if vector is larger than or equal the second vector (Not single value comparison) 
    '''

    def __init__(self, x=0, y=0, z=0):
        '''
            Class constractor
            ---------
            args:
                x - double - magnitude of vector along x-axis
                y - double - magnitude of vector along y-axis
                z - double - magnitude of vector along z-axis
        '''

        self.x = x
        self.y = y
        self.z = z

    def __getitem__(self, key):
        '''
            operation overload for [] operator which treats vector as 1D array
            ---------
            args:
                key - int - index of 0, 1, 2 for x, y, z component of vector
        '''

        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            return self.z
    
    def __imul__(self, value):
        '''
            operation overload for *= operator for multiplication of vector with a scalar
            ---------
            args:
                value - double - value by which vector should be scaled 
        '''

        self.x *= value
        self.y *= value
        self.z *= value
        return self

    def __mul__(self, value):
        '''
            operation overload for * operator 
                - returns a scaler multiplication if value is vector
                - return a vector scaled by value if value is scalar
            ---------
            args:
                value - double - value by which vector should be scaled 
                value - Vector - another vector 
        '''

        if isinstance(value, Vector):
            return self.x*value.x + self.y*value.y + self.z*value.z
        else:
            return Vector(self.x*value,self.y*value,self.z*value)

    def __iadd__(self, vector):
        '''
            operation overload for += operator add two vectors 
            ---------
            args:
                vector - Vector 
        '''

        self.x += vector.x
        self.y += vector.y
        self.z += vector.z
        return self
    
    def __add__(self, vector):
        '''
            operation overload for + operator return a vector of addition of two original vectors
            ---------
            args:
                vector - Vecotr        '''

        return Vector(self.x + vector.x,self.y + vector.y,self.z + vector.z)

    def __isub__(self, vector):
        '''
            operation overload for -= operator to subtract second vector from first
            ---------
            args:
                vector - Vector 
        '''

        self.x -= vector.x
        self.y -= vector.y
        self.z -= vector.z
        return self
    
    def __sub__(self, vector):
        '''
            operation overload for - operator return a vector of sub of two original vectors
            ---------
            args:
                vector - Vector
        '''

        return Vector(self.x - vector.x,self.y - vector.y,self.z - vector.z)
 
    def __mod__(self, vector):
        '''
            operation overload for %  operator return a new vector vector product
            ---------
            args:
                vector - Vector
        '''

        return self.vectorProduct(vector)

    def __eq__(self,vector):
        '''
            operation overload for = operator return true if two vectors are equal (element by element comparison)
            ---------
            args:
                vector - Vector 
        '''

        return self.x == vector.x and self.y == vector.y and self.z == vector.z

    def __ne__(self,vector):
        '''
            operation overload for = operator return true if two vectors are not equal (element by element comparison)
            ---------
            args:
                vector - Vector 
        '''

        return x != vector.x or self.y != vector.y or self.z != vector.z

    def __lt__(self,vector):
        '''
            operation overload for < operator 
                Return true if the first vector is smaller than the second vector
	            This is not a single value comparison meaning that !(a <= b) doesnt imply a > b
            ---------
            args:
                vector - Vector
        '''

        return self.x < vector.x  and self.y < vector.y  and self.z < vector.z


    def __le__(self,vector):
        '''
            operation overload for <= operator 
                Return true if the first vector is smaller than or equal the second vector
                Not a single value comparison
            ---------
            args:
                vector - Vector
        '''

        return self.x <= vector.x and self.y <= vector.y and self.z <= vector.z

    def __gt__(self,vector):
        '''
            operation overload for > operator
                Return true if the first vector is bigger than the second vector
                Not a single value comparison
            ---------
            args:
                vector - Vector
        '''

        return self.x > vector.x and self.y > vector.y and self.z > vector.z


    def __ge__(self,vector):
        '''
            operation overload for >= operator for
                Return true if the first vector is bigger than or equal the second vector
                Not a single value comparison
            ---------
            args:
                vector - Vector 
        '''

        return self.x >= vector.x  and self.y >= vector.y  and self.z >= vector.z
    
    def invert(self):
        '''
            Invert current vector to opposite direction
        '''
        self.x = - self.x
        self.y = - self.y
        self.z = - self.z

    def addScaledVector(self, vector, value):
        '''
            Add scaled vector to current vector
            ---------
            args:
                vector - Vector 
                value - double - magnitude of scale to other vector
        '''

        self.x += vector.x * value
        self.y += vector.y * value
        self.z += vector.z * value

    def updateComponentProduct(self, vector):
        '''
            evaluate the component wise product and store it in the vector
            ---------
            args:
                vector - Vector 
        '''

        self.x *= vector.x;
        self.y *= vector.y;
        self.z *= vector.z;	

    def componentProduct(self, vector):
        '''
            return a copy vector of the component wise product
            ---------
            args:
                vector - Vector 
        '''

        return Vector(self.x * vector.x,self.y * vector.y,self.z * vector.z)

    def scalarProduct(self, vector):
        '''
            return scaler product
            ---------
            args:
                vector - Vector 
        '''

        return self.x * vector.x + self.y * vector.y + self.z * vector.z

    def updateVectorProduct(self, vector):
        '''
            evaluate the vector  product and store it in the vector
            ---------
            args:
                vector - Vector 
        '''

        self.x = y * vector.z - vector.y * z;
        self.y = z * vector.x - vector.z * x;
        self.z = x * vector.y - vector.x * y;
        
    def vectorProduct(self,vector):
        '''
            return a copy vector of the vector product
            ---------
            args:
                vector - Vector 
        '''

        return Vector(self.y * vector.z - vector.y * self.z, self.z * vector.x - vector.z * self.x, self.x * vector.y - vector.x * self.y);

    def magnitude(self):
        '''
            return magnitude of vector
        '''

        return (self.x**2+self.y**2+self.z**2)**(1/2)

    
    def squareMagnitude(self):
        '''
            return square of magnitude of vector
        '''

        return self.x**2+self.y**2+self.z**2

    
    def normalize(self):
        '''
            change non zero vector to unit vectors
        '''

        l = self.magnitude()
        if l > 0:
            self *= (1/l)

    def unit(self):
        '''
            return a normalized version of vector
        '''

        x = Vector(self.x,self.y,self.z)
        x.normalize()
        return x

    def trim(self, size):
        '''
            limit vector to a certain value
            ---------
            args:
                size - double - max magnitude of the vector 
        '''

        if self.squareMagnitude > size*size:
            self.normalize()
            self.x *= size
            self.y *= size
            self.z *= size
    
    def clear(self):
        '''
            set vector to 0,0,0
        '''

        self.x = 0
        self.y = 0
        self.z = 0

    def copy(self):
        '''
            return a copy of the vector
        '''

        return Vector(self.x,self.y,self.z)

    def set(self,x,y,z):
        '''
            setter of class
            ---------
            args:
                x - double - magnitude of vector along x-axis
                y - double - magnitude of vector along y-axis
                z - double - magnitude of vector along z-axis
        '''

        self.x = x
        self.y = y
        self.z = z

    def toVPython(self):
        '''
            Return a vector which is used by the graphics library
        '''

        return vector(self.x, self.y, self.z)

    def __str__(self):
        return str(self.x) + " " + str(self.y) + " " + str(self.z)