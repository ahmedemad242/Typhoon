from Typhoon.Core import *
from Typhoon.Contact.Contact import *

class CollisionPrimitive:
    '''
        Class representes the primitives which surroundes the body for approximate contact resolution
        ---------
        properties:
            body      - RigidBody - Rigidbody which is surrounded by this primitive
            offset    - Matrix4   - Offset of the primitive from rigid body center
            transform - Matrix4   - Resultant tranformation of the primitive
    '''

    def __init__(self):
        '''
            Class constractor
        '''

        self.body = None
        self.offset =  Matrix4()
        self.transform = None

    
    def calculateInternals(self):
        '''
            Calculate transform matrix of primitaive from body transform matrix and offset
        '''

        self.transform = self.body.getTransform() * self.offset

    def getAxis(self, index):
        '''
            Return a specific axis vector of transform of primitive
            ---------
            args:
                index - int 
        '''

        return self.transform.getAxisVector(index)

    def getTransform(self):
        '''
            Return the transform of the primitive
        '''
        return self.transform.copy()

class CollisionSphere(CollisionPrimitive):
    '''
        Class representes a sphere which surroundes the body for approximate contact resolution
        ---------
        properties:
            body      - RigidBody - Rigidbody which is surrounded by this primitive
            offset    - Matrix4   - Offset of the primitive from rigid body center
            transform - Matrix4   - Resultant tranformation of the primitive
            radius    - double    - radius of the sphere
    '''

    def __init__(self):
        '''
            Class constractor
        '''

        super().__init__()
        self.radius = 0

class CollisionBox(CollisionPrimitive):
    '''
        Class representes a box which surroundes the body for approximate contact resolution
        ---------
        properties:
            body      - RigidBody - Rigidbody which is surrounded by this primitive
            offset    - Matrix4   - Offset of the primitive from rigid body center
            transform - Matrix4   - Resultant tranformation of the primitive
            halfSize  - Vector    - represent halfsize vector of the box
    '''

    def __init__(self):
        '''
            Class constractor
        '''

        super().__init__()
        self.halfSize = None

class CollisionPlane: 
    '''
        Class representes an immovable plane in the world
        ---------
        properties:
            offset    - double   - Offset of the primitive from rigid body center
            direction - Vector    - radius of the sphere
    '''

    def __init__(self):
        '''
            Class constractor
        '''

        self.direction = None
        self.offset = None


class IntersectionTests:
    '''
        Wrapper class for intersection tests, used to define early outs in corase collision detection
    '''

    @staticmethod
    def transformToAxis(box: CollisionBox, axis: Vector):
        '''
            class method to transform box halfsizes into an axis
            ---------
            args:
                box  - CollisionBox
                axis - Vector
        '''
        return box.halfSize.x * abs(axis * box.getAxis(0)) +\
               box.halfSize.y * abs(axis * box.getAxis(1)) +\
               box.halfSize.z * abs(axis * box.getAxis(2))


    @staticmethod
    def boxAndHalfSpace(box: CollisionBox, plane: CollisionPlane):
        '''
            class method Return true if the box is intersecting with the given half space
            ---------
            args:
                box   - CollisionBox
                plane - CollisionPlane
        '''

        projectedRadius = IntersectionTests.transformToAxis(box, plane.direction);
        boxDistance = plane.direction * box.getAxis(3) - projectedRadius
        return boxDistance <= plane.offset

class CollisionData:
    '''
        Holds data for detecor to use in building contact data
        ---------
        properties:
            contactArray - list   - Array to write contacts into, defined in the world, and passed here
            contactsLeft - int    - Contacts left
            contactCount - int    - Contacts found until nw
            friction     - double - Frictin to write into any found collision
            restitution  - double - Restitution to write into any found collision
            tolerance    - double - Uncolliding objects this close should have collisions generated.
    '''

    def __init__(self):
        '''
            Class constractor
        '''

        self.contactArray = None
        self.contactsLeft = 0
        self.contactCount = 0
        self.friction = 0
        self.restitution = 0
        self.tolerance = 0

    def hasMoreContacts(self):
        '''
            Return true if we hae contacts left 

        '''

        return self.contactsLeft > 0

    def reset(self, maxContacts):
        '''
            Reset data so it has no contacts used, It clears the countactArray as well
            ---------
            args:
                maxContacts - int
        '''

        self.contactsLeft = maxContacts
        self.contactCount = 0
        self.contactArray.clear()

    def addContacts(self, count):
        '''
            Add number of used contacts
            ---------
            args:
                count - int - number of used contacts
        '''

        self.contactsLeft -= count;
        self.contactCount += count;

#A wrapper class that holds the fine grained collision detection types
class CollisionDetector:
    '''
        Wrapper class holds the fine grained collision detection types
    '''

    @staticmethod
    def sphereAndSphere(one: CollisionSphere, two: CollisionSphere, data: CollisionData):
        '''
            create a contact between two spheres
            return number of contacts used
            ---------
            args:
                one  - CollisionSphere
                two  - CollisionSphere
                data - CollisionData
        '''

        if data.contactsLeft <= 0: return 0
        positionOne = one.getAxis(3)
        positionTwo = two.getAxis(3)

        midline = positionOne - positionTwo 
        size = midline.magnitude()

        if size <= 0.0 or (size >= one.radius+two.radius): return 0

        #Create normal
        normal = (midline * (1.0/size)).copy()
        #Create a contact with normal in planes direction
        data.contactArray.append(Contact())
        data.contactArray[-1].contactNormal = normal
        data.contactArray[-1].contactPoint = positionOne + midline * 0.5
        data.contactArray[-1].penetration = (one.radius+two.radius - size)
        data.contactArray[-1].setBodyData(one.body, two.body,data.friction, data.restitution)
        data.addContacts(1)
        
        return 1

    @staticmethod
    def boxAndHalfSpace(box: CollisionBox, plane: CollisionPlane, data: CollisionData):
        '''
            create a contact between box and plane
            return number of contacts used
            ---------
            args:
                box   - CollisionBox
                plane - CollisionPlane
                data  - CollisionData
        '''

        if data.contactsLeft <= 0: return 0
        #Check for intersection using simple test as early out
        if (not IntersectionTests.boxAndHalfSpace(box, plane)): return 0
             
        #Go through each combination of + and - for each half-size
        #This is used to get vertex position
        mults = [[1,1,1],[-1,1,1],[1,-1,1],[-1,-1,1], [1,1,-1],[-1,1,-1],[1,-1,-1],[-1,-1,-1]]

        contactsUsed = 0
        for i in range(8):
            #Calculate the position of each vertex
            vertexPos = Vector(mults[i][0], mults[i][1], mults[i][2])
            vertexPos.updateComponentProduct(box.halfSize)
            vertexPos = box.transform.transform(vertexPos)

            #Calculate the distance from the plane
            vertexDistance = vertexPos * plane.direction 

            #Compare this to the plane's distance
            if vertexDistance <= plane.offset:
                #Create the contact data
                data.contactArray.append(Contact())
                #The contact point is halfway between the vertex and the
                #plane - we multiply the direction by half the separation
                #distance and add the vertex location.
                data.contactArray[-1].contactPoint = plane.direction.copy()
                data.contactArray[-1].contactPoint *= (vertexDistance-plane.offset)
                data.contactArray[-1].contactPoint += vertexPos
                data.contactArray[-1].contactNormal = plane.direction
                data.contactArray[-1].penetration = plane.offset - vertexDistance
                data.contactArray[-1].setBodyData(box.body, None, data.friction, data.restitution)

                #Check the next vertex
                contactsUsed+=1
                if contactsUsed == data.contactsLeft: return contactsUsed

        data.addContacts(contactsUsed)
        return contactsUsed

    @staticmethod
    def sphereAndHalfSpace(sphere: CollisionPlane, plane: CollisionPlane, data: CollisionData):
        '''
            create a contact with sphere and plane
            return number of contacts used
            ---------
            args:
                sphere - CollisionPlane
                plane  - CollisionPlane
                data   - CollisionData
        '''

        if data.contactsLeft <= 0: return 0
        #Copy sphere position
        position = sphere.getAxis(3)
        #Find distance from plane
        ballDistance = plane.direction * position - sphere.radius - plane.offset
        #Away or touching spheres
        if ballDistance >= 0: return 0
        #Create a contact with normal in plane's direction
        data.contactArray.append(Contact())
        data.contactArray[-1].contactNormal = plane.direction
        data.contactArray[-1].penetration = -ballDistance
        data.contactArray[-1].contactPoint = position - plane.direction * (ballDistance + sphere.radius)
        data.contactArray[-1].setBodyData(sphere.body, None, data.friction, data.restitution)

        data.addContacts(1);
        return 1