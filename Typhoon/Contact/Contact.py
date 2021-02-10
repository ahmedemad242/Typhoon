from Typhoon.Core import *
from abc import ABC, abstractmethod

#A contact represents two bodies in contact. Resolving a
#contact removes their interpenetration, and applies sufficient
#impulse to keep them apart. Colliding bodies may also rebound.
#Contacts can be used to represent positional joints, by making
#the contact constraint keep the bodies in their correct
#orientation.
class Contact:
    def __init__(self): 
        #Holds the bodies that are involved in the contact. The
        #second of these can be NULL, for contacts with the scenery.
        self.body = [None, None]
        #Holds the lateral friction coefficient at the contact.
        self.friction = 0
        #Holds the normal restitution coefficient at the contact.
        self.restitution = 0
        #Holds the position of the contact in world coordinates.
        self.contactPoint = None
        #Holds the direction of the contact in world coordinates.
        self.contactNormal = None
        #Holds the depth of penetration at the contact point. If both
        #bodies are specified then the contact point should be midway
        #between the inter-penetrating points.
        self.penetration = None
        #Transform matrix which converts contacts coordinate 
        #to world coordinate
        self.contactToWorld = Matrix3()
        #Hold closing velocity of the contact
        self.contactVelocity = None
        #Holds change of velocity for which the contact
        #will be resolved
        self.desiredDeltaVelocity = 0
        #Holds a world coordinate version of the 
        #two contact points relative to center of each
        #body
        self.relativeContactPosition = [None, None]

    #Set data of contact which doesnt depend on the position
    def setBodyData(self, one, two, friction, restitution):
        self.body[0] = one
        self.body[1] = two
        self.friction = friction
        self.restitution = restitution

    #Calculate internal data from state data. 
    #It is called in resolver, sholdnt be called manually.
    def calculateInternals(self, duration):
        #If first object is NULL, swap it
        if not self.body[0]: self.swapBodies()
        assert(self.body[0])

        #Calculate axis of the contact point
        self.calculateContactBasis()

        #Store the relative position of contact relative to each body
        self.relativeContactPosition[0] = self.contactPoint - self.body[0].getPosition()
        if self.body[1]: self.relativeContactPosition[1] = self.contactPoint - self.body[1].getPosition()

        #Store the relative velocity of contact relative to each body
        self.contactVelocity = self.calculateLocalVelocity(0, duration);
        if self.body[1]:
            self.contactVelocity -= self.calculateLocalVelocity(1, duration); 

        self.calculateDesiredDeltaVelocity(duration);

    #Swap bodies of the contact where body[0] is at body[1]
    #and visa versa. The contact normal is also set to the opposite
    #direction.
    def swapBodies(self):
        self.contactNormal *= -1
        temp = self.body[0]
        self.body[0] = self.body[1]
        self.body[1] = temp
    
        #When two bodies collides, if one is awake, the other is awaken
    def matchAwakeState(self):
        if not self.body[1]: return
        body0awake = self.body[0].isAwake
        body1awake = self.body[1].isAwake
        #Only one of the bodies is awake
        if body0awake ^ body1awake:
            if body0awake: body[1].isAwake = True
            else: body[0].isAwake = True

    #Calculate and set value of desiredDeltaVelocity
    def calculateDesiredDeltaVelocity(self, duration):
        velocityLimit = 0.25
        #Calculate velocity due to acceleration in this frame
        velocityFromAcc = 0

        if self.body[0].isAwake: velocityFromAcc+= (self.body[0].getLastFrameAcceleration() * duration) * self.contactNormal
        if self.body[1] and self.body[1].isAwake: velocityFromAcc -= (self.body[1].getLastFrameAcceleration() * duration) * self.contactNormal
        #Limit restitution at low velocities
        thisRestitution = self.restitution
        if abs(self.contactVelocity.x) < velocityLimit: thisRestitution = 0
        #Remove acceleration velocity 
        self.desiredDeltaVelocity = -self.contactVelocity.x -thisRestitution * (self.contactVelocity.x - velocityFromAcc)
    
    #return the velocity of the contact relative to one of the bodiess
    def calculateLocalVelocity(self, bodyIndex, duration):
        thisBody = self.body[bodyIndex]
        #Velocity of the contact point
        velocity = thisBody.getRotation() % self.relativeContactPosition[bodyIndex]
        velocity += thisBody.getVelocity()
        #Convert to contact coordinates
        contactVelocity = self.contactToWorld.transformTranspose(velocity)
        #Amount of velocity due to non reaction forces (acting directly on body as gravity)
        accVelocity = thisBody.getLastFrameAcceleration() * duration
        accVelocity = self.contactToWorld.transformTranspose(accVelocity)
        #Ignore acceleration in direction of contact normal
        accVelocity.x = 0
        contactVelocity += accVelocity
        return contactVelocity

    #Construct an arbitrary matrix which convert contact space to
    #world space. The x-axis is the contactNormal, y and z axes is set
    #arbitrary orthogonal to x-axis and to each others
    def calculateContactBasis(self):
        contactTangent = [Vector(), Vector()]
        #Check if worlds z-axis is nearer to y or x axis
        if abs(self.contactNormal.x) > abs(self.contactNormal.y):
            #For normalization
            s = 1/((self.contactNormal.z**2 + self.contactNormal.x**2)**(1/2))
            #local z-axis is right angled from world's y-axis
            contactTangent[0].x = self.contactNormal.z*s
            contactTangent[0].y = 0
            contactTangent[0].z = - self.contactNormal.x*s
            #local y-axis is at right angle of the local x-axis and z-axis
            contactTangent[1].x = self.contactNormal.y*contactTangent[0].x
            contactTangent[1].y = self.contactNormal.z*contactTangent[0].x - self.contactNormal.x*contactTangent[0].z
            contactTangent[1].z = -self.contactNormal.y*contactTangent[0].x
        else:
            #For normalization
            s = 1/((self.contactNormal.z**2 +self.contactNormal.y**2)**(1/2))
            #local z-axis is right angled from world's y-axis
            contactTangent[0].x = 0
            contactTangent[0].y = -self.contactNormal.z*s
            contactTangent[0].z = self.contactNormal.y*s
            #local y-axis is at right angle of the local x-axis and z-axis
            contactTangent[1].x = self.contactNormal.y*contactTangent[0].z - self.contactNormal.z*contactTangent[0].y
            contactTangent[1].y = -self.contactNormal.x*contactTangent[0].z
            contactTangent[1].z = self.contactNormal.x*contactTangent[0].y

        self.contactToWorld.setComponent(self.contactNormal,contactTangent[0], contactTangent[1])

    #Apply velocity and rotation change then stores their values in given parameters
    def applyVelocityChange(self, velocityChange, rotationChange):
        #Get inverse of inertia tensor of two bodies
        inverseInertiaTensor = [None, None]
        inverseInertiaTensor[0] = self.body[0].getInverseInertiaTensorWorld()
        if self.body[1]: inverseInertiaTensor[1] = self.body[1].getInverseInertiaTensorWorld()
        #Calculate impulse for each axes
        impulseContact = None
        if self.friction == 0:
            impulseContact = self.calculateFrictionlessImpulse(inverseInertiaTensor)
        else:
            impulseContact = self.calculateFrictionImpulse(inverseInertiaTensor)

        #Impulse in world coordinates
        impulse = self.contactToWorld.transform(impulseContact)
        #Split impulse in both linear and rotational components
        impulsiveTorque = self.relativeContactPosition[0] % impulse
        rotationChange[0] = inverseInertiaTensor[0].transform(impulsiveTorque)
        velocityChange[0].clear()
        velocityChange[0].addScaledVector(impulse, self.body[0].getInverseMass())
        #Apply change
        self.body[0].addVelocity(velocityChange[0])
        self.body[0].addRotation(rotationChange[0])

        if self.body[1]:
            #Tourque is in opposite direction
            impulsiveTorque = impulse % self.relativeContactPosition[1]
            rotationChange[1] = inverseInertiaTensor[1].transform(impulsiveTorque)
            velocityChange[1].clear()
            velocityChange[1].addScaledVector(impulse, -self.body[1].getInverseMass())
            #Apply change
            self.body[1].addVelocity(velocityChange[1])
            self.body[1].addRotation(rotationChange[1])

    #Adjust interpenertation of the conatct based on inertia
    def applyPositionChange(self, linearChange, angularChange,  penetration):
        angularLimit = 0.2
        angularMove = [0, 0]
        linearMove = [0, 0]

        totalInertia = 0
        linearInertia = [0,0]
        angularInertia = [0, 0]
        
        #Get inertia of each object in direction of contactNormal
        #due to angular inertia only
        for i in range(2): 
            if (self.body[i]):
                inverseInertiaTensor = self.body[i].getInverseInertiaTensorWorld()
                #Calculate angular inertia.
                angularInertiaWorld = self.relativeContactPosition[i] % self.contactNormal
                angularInertiaWorld = inverseInertiaTensor.transform(angularInertiaWorld)
                angularInertiaWorld = angularInertiaWorld % self.relativeContactPosition[i]
                angularInertia[i] = angularInertiaWorld * self.contactNormal
                #The linear component is simply the inverse mass
                linearInertia[i] = self.body[i].getInverseMass()
                #Keep track of the total inertia from all components
                totalInertia += linearInertia[i] + angularInertia[i]

        #Loop through again calculating and applying the changes
        for i in range(2):
            if (self.body[i]):
                #The linear and angular movements
                sign = 1 if i == 0 else -1
                angularMove[i] = sign * penetration * (angularInertia[i] / totalInertia)
                linearMove[i] = sign * penetration * (linearInertia[i] / totalInertia)
                #To avoid angular projections that are too great (when mass is large
                #but inertia tensor is small) limit the angular move.
                projection = self.relativeContactPosition[i].copy()
                projection.addScaledVector(self.contactNormal,-self.relativeContactPosition[i].scalarProduct(self.contactNormal))
                #Use the small angle approximation for the sine of the angle the
                #magnitude would be sine(angularLimit) * projection.magnitude
                #but we approximate sine(angularLimit) to angularLimit)
                maxMagnitude = angularLimit * projection.magnitude()
                if angularMove[i] < -maxMagnitude:
                    totalMove = angularMove[i] + linearMove[i]
                    angularMove[i] = -maxMagnitude
                    linearMove[i] = totalMove - angularMove[i]
                elif angularMove[i] > maxMagnitude:
                    totalMove = angularMove[i] + linearMove[i]
                    angularMove[i] = maxMagnitude
                    linearMove[i] = totalMove - angularMove[i]
                #Calculate rotation which will do part of the linear motion
                if angularMove[i] == 0:
                    #angular movement means no rotation.
                    angularChange[i].clear()
                else:
                    #Work out the direction we'd like to rotate in.
                    targetAngularDirection = self.relativeContactPosition[i].vectorProduct(self.contactNormal)

                    inverseInertiaTensor = self.body[i].getInverseInertiaTensorWorld()
                    #Work out the direction we'd need to rotate to achieve that
                    angularChange[i] = inverseInertiaTensor.transform(targetAngularDirection) * (angularMove[i] / angularInertia[i])
                
                    #Velocity change is easier - it is just the linear movement
                #along the contact normal.
                linearChange[i] = self.contactNormal * linearMove[i]
                #Now we can start to apply the values we've calculated.
                #Apply the linear movement
                pos = self.body[i].getPosition()
                pos.addScaledVector(self.contactNormal, linearMove[i])
                self.body[i].setPosition(pos.x,pos.y,pos.z)
                #And the change in orientation
                q = Quaternion()
                self.body[i].getOrientation(q)
                q.addScaledVector(angularChange[i], 1)
                self.body[i].setOrientation(q.r,q.i,q.j,q.k)
                #We need to calculate the derived data for any body that is
                #asleep, so that the changes are reflected in the object's
                #data. Otherwise the resolution will not change the position
                #of the object, and the next collision detection round will
                #have the same penetration.
                if not self.body[i].isAwake: self.body[i].calculateDerivedData()

    def calculateFrictionlessImpulse(self, inverseInertiaTensor):
        impulseContact = Vector()
        #Calculate change in velocity for unit impulse in 
        #direction of contactNormal in world space
        deltaVelWorld = self.relativeContactPosition[0] % self.contactNormal
        deltaVelWorld = inverseInertiaTensor[0].transform(deltaVelWorld)
        deltaVelWorld = deltaVelWorld % self.relativeContactPosition[0]
        #Change in velocity in contact coordinates
        deltaVelocity = deltaVelWorld * self.contactNormal
        #Add linear component of change of velocity
        deltaVelocity += self.body[0].getInverseMass()

        if self.body[1]:
            #Calculate change in velocity for unit impulse in 
            #direction of contactNormal in world space
            deltaVelWorld = self.relativeContactPosition[1] % self.contactNormal
            deltaVelWorld = inverseInertiaTensor[1].transform(deltaVelWorld)
            deltaVelWorld = deltaVelWorld % self.relativeContactPosition[1]
            #Change in velocity in contact coordinates
            deltaVelocity += deltaVelWorld * self.contactNormal
            #Add linear component of change of velocity
            deltaVelocity += self.body[1].getInverseMass()
        #Calculate the required size of the impulse
        impulseContact.x = self.desiredDeltaVelocity / deltaVelocity
        impulseContact.y = 0
        impulseContact.z = 0
        return impulseContact

    def calculateFrictionImpulse(self, inverseInertiaTensor):
        impulseContact = None
        inverseMass = self.body[0].getInverseMass()
        #Helper matrix to convert between linear and angular quantities
        impulseToTorque = Matrix3()
        impulseToTorque.setSkewSymmetric(self.relativeContactPosition[0])
        #Convert Impulse into change in velocity 
        deltaVelWorld = impulseToTorque.copy()
        deltaVelWorld *= inverseInertiaTensor[0]
        deltaVelWorld *= impulseToTorque
        deltaVelWorld *= -1

        if self.body[1]:
            impulseToTorque.setSkewSymmetric(self.relativeContactPosition[1]);
            #Convert Impulse into change in velocity 
            deltaVelWorld2 = impulseToTorque.copy()
            deltaVelWorld2 *= inverseInertiaTensor[1]
            deltaVelWorld2 *= impulseToTorque
            deltaVelWorld2 *= -1
            #Add second body's values to total
            deltaVelWorld += deltaVelWorld2
            inverseMass += self.body[1].getInverseMass()
        #Convert into contact coordinates
        deltaVelocity = self.contactToWorld.transpose().copy()
        deltaVelocity *= deltaVelWorld
        deltaVelocity *= self.contactToWorld
        #Add linear change
        deltaVelocity.data[0] += inverseMass
        deltaVelocity.data[4] += inverseMass
        deltaVelocity.data[8] += inverseMass
        #Impulse needed per unit velocity
        impulseMatrix = deltaVelocity.inverse().copy()
        #Kill following velocities by friction
        velKill = Vector(self.desiredDeltaVelocity, -self.contactVelocity.y, -self.contactVelocity.z)
        #Impulse needed to kill velocity
        impulseContact = impulseMatrix.transform(velKill)
        planarImpulse = ( impulseContact.y**2 + impulseContact.z**2)**(1/2)
        #check if friction is exceeding
        if planarImpulse > abs(impulseContact.x * self.friction):
            #Dynamic velocity
            impulseContact.y /= planarImpulse;
            impulseContact.z /= planarImpulse;

            impulseContact.x = deltaVelocity.data[0] + deltaVelocity.data[1]*self.friction*impulseContact.y + deltaVelocity.data[2]*self.friction*impulseContact.z;
            impulseContact.x = self.desiredDeltaVelocity / impulseContact.x;
            impulseContact.y *= self.friction * impulseContact.x;
            impulseContact.z *= self.friction * impulseContact.x;
        
        return impulseContact;
  
#Contact resolver is used to resolve all contacts in simulation
#One instance can be shared across the whole simulation if the
#parameters are roughly the same

#The algorithms iterate through a set of contacts returned by the collision
#detectors, it solves the contact locally without consideration to other
#contacts which means it might make other contacts worse. But with enough 
#iteration limit, it can be proved that the simulation will be true given
#numerical stability

#This algorithm was chosen because it is very fast. It can be given a limit
#More than the contacts and still exist quickly

#Lastly, we must know that this method doesnt act well in high friction simulations
#or where several objects are resting on one another. As the contact is solved locally,
#it will create a chain of inacuracy which wont look good on stacked objects.

#It deals well with impacts, explosions, and resting situations.
class ContactResolver:
    def __init__(self, velocityIterations, positionIterations, velocityEpsilon = 0.01, positionEpsilon = 0.01):
        self.velocityIterations = velocityIterations
        self.positionIterations = positionIterations
        #Velocity smaller than this can be considered 0
        #It is used to deal with instability problems
        #too small, simulation unstable
        #too large, objects will interpentrate
        self.velocityEpsilon = velocityEpsilon
        #Smaller than this value considered to not be interpenteration
        #It is used to deal with instability problems
        #too small, simulation unstable
        #too large, objects will interpentrate
        self.positionEpsilon = positionEpsilon
        self.velocityIterationsUsed = 0
        self.positionIterationsUsed = 0
        #Check validity of algorithm internal settings
        self.validSettings = False
    
    #Return True if setting of the resolver are set correctly
    def isValid(self):
        return (self.velocityIterations > 0) and (self.positionIterations > 0) and (self.positionEpsilon >= 0.0) and (self.positionEpsilon >= 0.0)

    def setIterations(self, velocityIterations, positionIterations):
        self.velocityIterations = velocityIterations
        self.positionIterations = positionIterations

    def setEpsilon(self, velocityEpsilon, positionEpsilon):
        self.velocityEpsilon = velocityEpsilon
        self.positionEpsilon = positionEpsilon

    def resolveContacts(self, contactArray,  numContacts,  duration):
        if numContacts == 0: return
        if not self.isValid(): return
        #Prepare contacts for processing
        self.prepareContacts(contactArray, numContacts, duration)
        #Resolve interpenetration
        self.adjustPositions(contactArray, numContacts, duration)
        #Resolve velocity
        self.adjustVelocities(contactArray, numContacts, duration)

    def prepareContacts(self, contactArray,  numContacts,  duration):
        for contact in contactArray:
            contact.calculateInternals(duration)

    def adjustVelocities(self, contactArray, numContacts, duration):
        velocityChange = [Vector(),Vector()]
        rotationChange = [None, None]
        deltaVel = None

        self.velocityIterationsUsed = 0
        while (self.velocityIterationsUsed < self.velocityIterations):
            #Find contact with max magnitude of velocity change
            max = self.velocityEpsilon
            desiredContact = None
            for contact in contactArray:
                if contact.desiredDeltaVelocity > max:
                    max = contact.desiredDeltaVelocity
                    desiredContact = contact
            if desiredContact == None: break

            #Match awake state of two bodies in contact
            desiredContact.matchAwakeState()
            #Resolve contact velocity
            desiredContact.applyVelocityChange(velocityChange, rotationChange)
            #With the new change in velocity, the closing velocity of the contacts
            #dealing with these two objects needs recalculation
            for contact in contactArray:
                #Check each body in contact
                for b in range(2):
                    if contact.body[b]:
                        #Check match with our two bodies
                        for d in range(2):
                            if contact.body[b] == desiredContact.body[d]:
                                deltaVel = velocityChange[d] + rotationChange[d].vectorProduct(contact.relativeContactPosition[b])
                                #Negative change in second object
                                contact.contactVelocity += contact.contactToWorld.transformTranspose(deltaVel) * (-1 if b else 1)
                                contact.calculateDesiredDeltaVelocity(duration)
            self.velocityIterationsUsed+=1

    def adjustPositions(self, contactArray, numContacts, duration):
        linearChange = [None, None] 
        angularChange = [Vector(), Vector()]
        max = 0
        deltaPosition = None

        self.positionIterationsUsed = 0
        while self.positionIterationsUsed < self.positionIterations:
            #Find contact with max interpenteration
            max = self.positionEpsilon
            desiredContact = None
            for contact in contactArray:
                if contact.penetration > max:
                    max = contact.penetration
                    desiredContact = contact
            if desiredContact == None: break
            #Match awake state of two bodies in contact
            desiredContact.matchAwakeState()
            #Resolve contact velocity
            desiredContact.applyPositionChange(linearChange, angularChange, max)
            
            #With the new change in velocity, the closing velocity of the contacts
            #dealing with these two objects needs recalculation
            for contact in contactArray:
                #Check each body in contact
                for b in range(2):
                   if contact.body[b]:
                       #Check match with our two bodies
                        for d in range(2):
                            if contact.body[b] == desiredContact.body[d]:
                                deltaPosition = linearChange[d] + angularChange[d].vectorProduct(contact.relativeContactPosition[b]);
                                #Sign is positive only for second body as we are subtracting position here
                                contact.penetration += deltaPosition.scalarProduct(contact.contactNormal) * (1 if b else -1)
            self.positionIterationsUsed+=1

class ContactGenerator(ABC):
    # Fills the given contact structure with the generated
    # contact. where limit is the  maximum number of contacts in 
    # the array that can be written to. The method returns
    #  the number of contacts that havebeen written.
    @abstractmethod
    def addContact(self, contact, limit):
        pass

