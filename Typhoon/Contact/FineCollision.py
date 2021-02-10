from Typhoon.Core import *
from Typhoon.Contact.Contact import *

class CollisionPrimitive:
    def __init__(self):
        #Rigidbody which is surrounded by this primitive
        self.body = None
        #Offset of the primitive from rigid body center
        self.offset =  Matrix4()
        #Resultant tranformation of the primitive
        #Calculated from offset of the primitive 
        #and the transform of the rigid body
        self.transform = None

    #Calculates the internals for the primitive
    def calculateInternals(self):
        self.transform = self.body.getTransform() * self.offset

    #Return a specific axis vector of transform of primitive
    def getAxis(self, index):
        return self.transform.getAxisVector(index)

    #Return the transform of the primitive
    def getTransform(self):
        return self.transform.copy()

#Represent a sphere surrounding a rigidbody for collision detection
class CollisionSphere(CollisionPrimitive):
    def __init__(self):
        super().__init__()
        self.radius = 0

#Represent a box surrounding a rigidbody for collision detection
class CollisionPlane: 
    def __init__(self):
        self.direction = None
        self.offset = None

#Represnet an immovable plane in the world
class CollisionBox(CollisionPrimitive):
    def __init__(self):
        super().__init__()
        self.halfSize = None

#Wrapper class for intersection tests which
#can be used in coarase collision detection ot
#early outs in fine collision detection
class IntersectionTests:
    #Transform box halfsizes into an axis
    @staticmethod
    def transformToAxis(box: CollisionBox, axis: Vector):
        return box.halfSize.x * abs(axis * box.getAxis(0)) +\
               box.halfSize.y * abs(axis * box.getAxis(1)) +\
               box.halfSize.z * abs(axis * box.getAxis(2))

    #Return true if the box is intersecting with
    #the given half space
    @staticmethod
    def boxAndHalfSpace(box: CollisionBox, plane: CollisionPlane):
        projectedRadius = IntersectionTests.transformToAxis(box, plane.direction);
        #How far the box is from origin on y axis
        boxDistance = plane.direction * box.getAxis(3) - projectedRadius
        return boxDistance <= plane.offset

#Holds data for detecor to use in building contact data
class CollisionData:
    def __init__(self):
        #Array to write contacts into
        #It is defined in the main world
        #and passed into here as a pointer
        self.contactArray = None
        #Contacts left
        self.contactsLeft = 0
        #Contacts found until nw
        self.contactCount = 0
        #Frictin to write into any found collision
        self.friction = 0
        #Restitution to write into any found collision
        self.restitution = 0
        #Holds the collision tolerance, even uncolliding objects this close should have collisions generated.
        self.tolerance = 0

    #Return true if we hae contacts left 
    def hasMoreContacts(self):
        return self.contactsLeft > 0

    #Reset data so it has no contacts used,
    #It clears the countactArray as well
    def reset(self, maxContacts):
        self.contactsLeft = maxContacts
        self.contactCount = 0
        self.contactArray.clear()

    #Add number of used contacts
    def addContacts(self, count):
        self.contactsLeft -= count;
        self.contactCount += count;

#A wrapper class that holds the fine grained collision detection types
class CollisionDetector:
    @staticmethod
    def sphereAndSphere(one: CollisionSphere, two: CollisionSphere, data: CollisionData):
        if data.contactsLeft <= 0: return 0
        #Copy sphere position
        positionOne = one.getAxis(3)
        positionTwo = two.getAxis(3)
        #Find the vector between the objects
        midline = positionOne - positionTwo 
        size = midline.magnitude()
        #See if it is large enough.
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
        if data.contactsLeft <= 0: return 0
        #Check for intersection using simple test as early out
        if (not IntersectionTests.boxAndHalfSpace(box, plane)): return 0
        #We have an intersection, so find the intersection points. We can 
        #do this with only checking vertices. If the box is resting on a 
        #face or on an edge, it will be reported as four or two contact 
        #points respectivly

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
    def sphereAndHalfSpace(sphere: CollisionSphere, plane: CollisionPlane, data: CollisionData):
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