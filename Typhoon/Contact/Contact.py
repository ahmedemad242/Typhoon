from Typhoon.Core import *
from abc import ABC, abstractmethod

class Contact:
    '''
        A Contact represents two bodies touching. This class stores information
        about the contact, and how to calculate its derived data as interpentration,
        impulse, etc...
        ---------
        properties:
            body                    - list    - Holds two bodeis that are involved in the contact
            friction                - double  - Holds the lateral friction coefficient
            restitution             - double  - Holds the normal restitution coefficient
            contactPoint            - Vector  - Holds the position of the contact in world coordinates
            contactNormal           - Vector  - Holds the direction of the contact in world coordinates
            penetration             - double  - Holds the depth of penetration at the contact point
            contactToWorld          - Matrix3 - Transform matrix which converts contacts coordinate to world
            contactVelocity         - Vector  - Hold closing velocity of the contact
            desiredDeltaVelocity    - double  - Holds change of velocity for which the contact will be resolved
            relativeContactPosition - list    - Holds a world coordinate of two contact points relative to center of each body
        ---------
        setBodyData:
            setters                         - Set data of contact which doesnt depend on the position
            calculateInternals              - Calculate internal data from state data, not called manually (only in resolver)
            swapBodies                      - Swap body[0] with body[1] and inverse the contact normal
            matchAwakeState                 - When two bodies collides, if one is awake, the other is awaken
            calculateDesiredDeltaVelocity   - Calculate and set value of desiredDeltaVelocity from acceleration
            calculateLocalVelocity          - Return the velocity of the contact relative to one of the bodies
            calculateContactBasis           - Construct and sets contactToWorld to an arbitrary matrix to convert contact space to world  
            applyVelocityChange             - Apply velocity and rotation change then stores their values in given parameters
            applyPositionChange             - Adjust interpenertation of the conatct based on inertia
            calculateFrictionlessImpulse    - calculate impulse of a frictionless contact
            calculateFrictionImpulse        - calculate impulse of a contact with friction
    '''

    def __init__(self): 
        '''
            Class constractor
        '''

        self.body = [None, None]
        self.friction = 0
        self.restitution = 0
        self.contactPoint = None
        self.contactNormal = None
        self.penetration = None
        self.contactToWorld = Matrix3()
        self.contactVelocity = None
        self.desiredDeltaVelocity = 0
        self.relativeContactPosition = [None, None]

    def setBodyData(self, one, two, friction, restitution):
        '''
            Set data of contact which doesnt depend on the position
            ---------
            args:
                one          - RigidBody - first body involved in contact
                two          - RigidBody - second body involved in contact
                friction     - double    - lateral friction coefficient
                restitution  - double    - normal restitution coefficient
        '''

        self.body[0] = one
        self.body[1] = two
        self.friction = friction
        self.restitution = restitution

    def calculateInternals(self, duration):
        '''
            Calculate internal data from state data, not called manually
            ---------
            args:
                duration - double - duration of time step
        '''

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

    def swapBodies(self):
        '''
            Swap bodies of the contact where body[0] is at body[1]
            The contact normal is also set to the opposite direction.
        '''

        self.contactNormal *= -1
        temp = self.body[0]
        self.body[0] = self.body[1]
        self.body[1] = temp
    
    def matchAwakeState(self):
        '''
            When two bodies collides, if one is awake, the other is awaken
        '''

        if not self.body[1]: return
        body0awake = self.body[0].isAwake
        body1awake = self.body[1].isAwake

        if body0awake ^ body1awake:
            if body0awake: body[1].isAwake = True
            else: body[0].isAwake = True

    def calculateDesiredDeltaVelocity(self, duration):
        '''
            Calculate and set value of desiredDeltaVelocity from acceleration
            ---------
            args:
                duration - double - duration of time step
        '''

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
    
    def calculateLocalVelocity(self, bodyIndex, duration):
        '''
            Return the velocity of the contact relative to one of the bodies
            ---------
            args:
                bodyIndex - int    - index of body 0 or 1
                duration  - double - duration of time step
        '''

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


    def calculateContactBasis(self):
        '''
            Construct an arbitrary matrix which convert contact space to world space
        '''

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

    def applyVelocityChange(self, velocityChange, rotationChange):
        '''
            Apply velocity and rotation change then stores their values in given parameters
            ---------
            args:
                velocityChange - list - list of 2 empty vectors to store velocity
                rotationChange - list - list of 2 empty vectors to store rotation
        '''

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

    def applyPositionChange(self, linearChange, angularChange,  penetration):
        '''
            Adjust interpenertation of the conatct based on inertia
            ---------
            args:
                linearChange  - list - list of 2 empty vectors to store linearChange
                angularChange - list - list of 2 empty vectors to store angularChange
        '''

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
                
                #Velocity change is just the linear movement along the contact normal.
                linearChange[i] = self.contactNormal * linearMove[i]

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
        '''
            calculate impulse of a frictionless contact
            ---------
            args:
                inverseInertiaTensor - Matrix3 
        '''

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
        '''
            calculate impulse of a contact with friction
            ---------
            args:
                inverseInertiaTensor - Matrix3 
        '''

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

class ContactResolver:
    '''
        Contact resolver is used to resolve all contacts in simulation, one instance is shared across simulation
        Resolver solves each contact locally which means it can worsen other contacts. This can be avoided by having more iterations
        Not to be used when applying high friction or several object resting on each other
        It deals well with impacts, explosions, and resting situations
        ---------
        properties:
            velocityIterations      - int    - Max number of iterations for velocity resolving
            positionIterations      - int    - Max number of iterations for position resolving
            velocityEpsilon         - double - Velocity smaller than this can be considered 0
            positionEpsilon         - double - Values smaller than this value considered to not be interpenteration
            velocityIterationsUsed  - int    - number of iterations used for velocity resolving
            positionIterationsUsed  - int    - number of iterations used for position resolving
            validSettings           - bool   - Check validity of algorithm internal settings
        ---------
        setBodyData:
            isValid         - Return True if setting of the resolver are set correctly
            setIterations   - set max number of iterations for velocity and position
            setEpsilon      - set epsilon of velocity and position
            resolveContacts - resolve all contacts in simulation
    '''

    def __init__(self, velocityIterations, positionIterations, velocityEpsilon = 0.01, positionEpsilon = 0.01):
        '''
            Class constractor
            ---------
            args:
                velocityIterations  - int           - Max number of iterations for velocity resolving
                positionIterations  - int           - Max number of iterations for position resolving
                velocityEpsilon     - double = 0.01 - Velocity smaller than this can be considered 0
                positionEpsilon     - double = 0.01 - Values smaller than this value considered to not be interpenteration
        '''

        self.velocityIterations = velocityIterations
        self.positionIterations = positionIterations
        self.velocityEpsilon = velocityEpsilon
        self.positionEpsilon = positionEpsilon
        self.velocityIterationsUsed = 0
        self.positionIterationsUsed = 0
        self.validSettings = False
    
    def isValid(self):
        '''
            Return True if setting of the resolver are set correctly
        '''

        return (self.velocityIterations > 0) and (self.positionIterations > 0) and (self.positionEpsilon >= 0.0) and (self.positionEpsilon >= 0.0)

    def setIterations(self, velocityIterations, positionIterations):
        '''
            set max number of iterations for velocity and position
            ---------
            args:
                velocityIterations  - int - Max number of iterations for velocity resolving
                positionIterations  - int - Max number of iterations for position resolving
        '''

        self.velocityIterations = velocityIterations
        self.positionIterations = positionIterations

    def setEpsilon(self, velocityEpsilon, positionEpsilon):
        '''
            set epsilon of velocity and position
            ---------
            args:
                velocityEpsilon     - double - Velocity smaller than this can be considered 0
                positionEpsilon     - double - Values smaller than this value considered to not be interpenteration
        '''

        self.velocityEpsilon = velocityEpsilon
        self.positionEpsilon = positionEpsilon

    def resolveContacts(self, contactArray,  numContacts,  duration):
        '''
            resolve all contacts in simulation
            ---------
            args:
                contactArray - double - Array of all contacts in simulation
                numContacts  - int    - Number of contacts in the array
                duration     - double - duration of time step
        '''

        if numContacts == 0: return
        if not self.isValid(): return

        #Prepare contacts for processing
        self.prepareContacts(contactArray, numContacts, duration)

        #Resolve interpenetration
        self.adjustPositions(contactArray, numContacts, duration)

        #Resolve velocity
        self.adjustVelocities(contactArray, numContacts, duration)

    def prepareContacts(self, contactArray,  numContacts,  duration):
        '''
            Prepare contacts for processing by calculating internal data
            ---------
            args:
                contactArray - double - Array of all contacts in simulation
                numContacts  - int    - Number of contacts in the array
                duration     - double - duration of time step
        '''

        for contact in contactArray:
            contact.calculateInternals(duration)

    def adjustVelocities(self, contactArray, numContacts, duration):
        '''
            Adjust velocity of bodies in contact
            It is important to note that contact with max magnitude of velocity change is solved first
            ---------
            args:
                contactArray - double - Array of all contacts in simulation
                numContacts  - int    - Number of contacts in the array
                duration     - double - duration of time step
        '''

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
                for b in range(2):
                    if contact.body[b]:
                        for d in range(2):
                            if contact.body[b] == desiredContact.body[d]:
                                deltaVel = velocityChange[d] + rotationChange[d].vectorProduct(contact.relativeContactPosition[b])

                                #Negative change in second object
                                contact.contactVelocity += contact.contactToWorld.transformTranspose(deltaVel) * (-1 if b else 1)
                                contact.calculateDesiredDeltaVelocity(duration)
            self.velocityIterationsUsed+=1

    def adjustPositions(self, contactArray, numContacts, duration):
        '''
            Adjust velocity of bodies in contact
            It is important to note that contact with max interpenteration is solved first
            ---------
            args:
                contactArray - double - Array of all contacts in simulation
                numContacts  - int    - Number of contacts in the array
                duration     - double - duration of time step
        '''

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
                for b in range(2):
                   if contact.body[b]:
                        for d in range(2):
                            if contact.body[b] == desiredContact.body[d]:
                                deltaPosition = linearChange[d] + angularChange[d].vectorProduct(contact.relativeContactPosition[b]);
                                
                                #Sign is positive only for second body as we are subtracting position here
                                contact.penetration += deltaPosition.scalarProduct(contact.contactNormal) * (1 if b else -1)

            self.positionIterationsUsed+=1

class ContactGenerator(ABC):
    @abstractmethod
    def addContact(self, contact, limit):
        pass

