from Typhoon.Core import *

class RigidBody:
    '''
        Class responsible for simulating rigid bodies
        ---------
        properties:
            inverseMass                 - double     - Holds inverse mass of the rigid body
            inverseInertiaTensor        - Matrix3    - Holds inverse of the body inertia in body space
            damping                     - double     - Holds the amount of damping applied to the linear motion
            angularDamping              - double     - Holds the amount of damping applied to the angular motion
            position                    - Vector     - Holds the position of the center of mass of the rigid body in world space
            orientation                 - Quaternion - Holds the angular orientation of the rigid body in world space
            velocity                    - Vector     - Holds linear velocity of center of mass of the rigid body in world space
            rotation                    - Vector     - Holds angular velocity of the rigid body in world space
            inverseInertiaTensorWorld   - Matrix3    - Holds inverse inertia tensor of the rigid body in world space
            motion                      - double     - Holds amount of motion of the body, act as storage to kinetic energy
            isAwake                     - bool       - determine the body is awake or not
            canSleep                    - bool       - determine if the body can sleep
            transformMatrix             - Matrix4    - Holds a transform matrix to transform body space to world space and visa versa
            forceAccum                  - Vector     - Holds the accumlated forces on the body to be applied in next integration step
            torqueAccum                 - Vector     - Holds the accumlated torques on the body to be applied in next integration step
            acceleration                - Vector     - Holds linear acceleration of the body (used to hold constant accelerations)
            lastFrameAcceleration       - Vector     - Holds linear acceleration of last frame

        ---------
        methods:
            setters & getters
            integrate                - Update the particle properties each time step
            hasFiniteMass            - Return true if object is movable
            clearAccumulator         - clears the force applied to the particle in this time step
            getPointInLocalSpace     - transform a point from world space to local space
            getPointInWorldSpace     - transform a point from local space to world space
            getDirectionInLocalSpace - transform a direction from world space to local space
            getDirectionInWorldSpace - transform a direction from local space to world space
            addForce                 - add force to the forceAccum in this time step (no torque)
            addForceAtBodyPoint      - add force to act on a point in body space (it causes torque)
            addForceAtPoint          - add force to act on a point in world space (it causes torque)
            addTorque                - add torque to the torqueAccum in this time step (no torque


    '''
    def __init__(self):
        '''
            Class constractor
        '''

        #charactaristic properties
        self.inverseMass = 0
        self.inverseInertiaTensor = Matrix3()
        self.damping = 1
        self.angularDamping = 1

        #state properties
        self.position = Vector()
        self.orientation = Quaternion()
        self.velocity = Vector()
        self.rotation = Vector()

        #Derived data (holds data drieved from above data)
        self.inverseInertiaTensorWorld = Matrix3()
        self.motion = 0
        self.isAwake = True
        self.canSleep = False
        self.transformMatrix = Matrix4()
        self.forceAccum = Vector()
        self.torqueAccum = Vector()
        self.acceleration = Vector()
        self.lastFrameAcceleration = Vector()

    def calculateDerivedData(self):
        '''
            calculate derived data as inertia tensor in world space and transform matrix
        '''

        #Note: Since python doesnt support inline functions, we will just put all the calculations here
        #This will cause us a problem in if we want to calculate part of  the drieved values
        #We will choose repeating the code for optimization purposes (imagine saying that and using python for a physics engine LOL!)

        self.orientation.normalize()

        ####Calculate the transform matrix
        self.transformMatrix.data[0] = 1-2*self.orientation.j*self.orientation.j-2*self.orientation.k*self.orientation.k
        self.transformMatrix.data[1] = 2*self.orientation.i*self.orientation.j - 2*self.orientation.r*self.orientation.k
        self.transformMatrix.data[2] = 2*self.orientation.i*self.orientation.k + 2*self.orientation.r*self.orientation.j
        self.transformMatrix.data[3] = self.position.x

        self.transformMatrix.data[4] = 2*self.orientation.i*self.orientation.j + 2*self.orientation.r*self.orientation.k
        self.transformMatrix.data[5] = 1-2*self.orientation.i*self.orientation.i- 2*self.orientation.k*self.orientation.k
        self.transformMatrix.data[6] = 2*self.orientation.j*self.orientation.k - 2*self.orientation.r*self.orientation.i
        self.transformMatrix.data[7] = self.position.y

        self.transformMatrix.data[8] = 2*self.orientation.i*self.orientation.k - 2*self.orientation.r*self.orientation.j
        self.transformMatrix.data[9] = 2*self.orientation.j*self.orientation.k + 2*self.orientation.r*self.orientation.i
        self.transformMatrix.data[10] = 1-2*self.orientation.i*self.orientation.i- 2*self.orientation.j*self.orientation.j
        self.transformMatrix.data[11] = self.position.z

        ####Calculate the inertia tensor in world space
        t4 = self.transformMatrix.data[0]*self.inverseInertiaTensor.data[0]+ self.transformMatrix.data[1]\
            *self.inverseInertiaTensor.data[3]+ self.transformMatrix.data[2]*self.inverseInertiaTensor.data[6]
        t9 = self.transformMatrix.data[0]*self.inverseInertiaTensor.data[1]+ self.transformMatrix.data[1]\
            *self.inverseInertiaTensor.data[4]+ self.transformMatrix.data[2]*self.inverseInertiaTensor.data[7]
        t14 = self.transformMatrix.data[0]*self.inverseInertiaTensor.data[2]+ self.transformMatrix.data[1]\
            *self.inverseInertiaTensor.data[5]+ self.transformMatrix.data[2]*self.inverseInertiaTensor.data[8]
        t28 = self.transformMatrix.data[4]*self.inverseInertiaTensor.data[0]+ self.transformMatrix.data[5]\
            *self.inverseInertiaTensor.data[3]+ self.transformMatrix.data[6]*self.inverseInertiaTensor.data[6]
        t33 = self.transformMatrix.data[4]*self.inverseInertiaTensor.data[1]+ self.transformMatrix.data[5]\
            *self.inverseInertiaTensor.data[4]+ self.transformMatrix.data[6]*self.inverseInertiaTensor.data[7]
        t38 = self.transformMatrix.data[4]*self.inverseInertiaTensor.data[2]+ self.transformMatrix.data[5]\
            *self.inverseInertiaTensor.data[5]+ self.transformMatrix.data[6]*self.inverseInertiaTensor.data[8]
        t52 = self.transformMatrix.data[8]*self.inverseInertiaTensor.data[0]+ self.transformMatrix.data[9]\
            *self.inverseInertiaTensor.data[3]+ self.transformMatrix.data[10]*self.inverseInertiaTensor.data[6]
        t57 = self.transformMatrix.data[8]*self.inverseInertiaTensor.data[1]+ self.transformMatrix.data[9]\
            *self.inverseInertiaTensor.data[4]+ self.transformMatrix.data[10]*self.inverseInertiaTensor.data[7]
        t62 = self.transformMatrix.data[8]*self.inverseInertiaTensor.data[2]+ self.transformMatrix.data[9]\
            *self.inverseInertiaTensor.data[5]+ self.transformMatrix.data[10]*self.inverseInertiaTensor.data[8]

        self.inverseInertiaTensorWorld.data[0] = t4*self.transformMatrix.data[0]+ t9*self.transformMatrix.data[1]\
            + t14*self.transformMatrix.data[2]
        self.inverseInertiaTensorWorld.data[1] = t4*self.transformMatrix.data[4]+ t9*self.transformMatrix.data[5]\
            + t14*self.transformMatrix.data[6]
        self.inverseInertiaTensorWorld.data[2] = t4*self.transformMatrix.data[8]+ t9*self.transformMatrix.data[9]\
            + t14*self.transformMatrix.data[10]
        self.inverseInertiaTensorWorld.data[3] = t28*self.transformMatrix.data[0]+ t33*self.transformMatrix.data[1]\
            + t38*self.transformMatrix.data[2]
        self.inverseInertiaTensorWorld.data[4] = t28*self.transformMatrix.data[4]+ t33*self.transformMatrix.data[5]\
            + t38*self.transformMatrix.data[6]
        self.inverseInertiaTensorWorld.data[5] = t28*self.transformMatrix.data[8]+ t33*self.transformMatrix.data[9]\
            + t38*self.transformMatrix.data[10]
        self.inverseInertiaTensorWorld.data[6] = t52*self.transformMatrix.data[0]+ t57*self.transformMatrix.data[1]\
            + t62*self.transformMatrix.data[2]
        self.inverseInertiaTensorWorld.data[7] = t52*self.transformMatrix.data[4]+ t57*self.transformMatrix.data[5]\
            + t62*self.transformMatrix.data[6]
        self.inverseInertiaTensorWorld.data[8] = t52*self.transformMatrix.data[8]+ t57*self.transformMatrix.data[9]\
            + t62*self.transformMatrix.data[10]

    def integrate(self,duration):
        '''
            method which updates the particle properties each time step
            ---------
            args:
                duration - double - duration of time step
        '''

        if not self.isAwake: return

        #Calculate linear acceleration from forceAccum
        self.lastFrameAcceleration = self.getAcceleration()
        self.lastFrameAcceleration.addScaledVector(self.forceAccum,self.inverseMass)
        
        #Calculate angular acceleration from torqueAccum
        #AngularAcceleration = InertiaInverse * tourque
        angularAcceleration = self.inverseInertiaTensorWorld.transform(self.torqueAccum)

        #Adjust linear velocity
        self.velocity.addScaledVector(self.lastFrameAcceleration,duration)

        #Adjust angular velocity
        self.rotation.addScaledVector(angularAcceleration,duration)

        #Calculate drag
        self.velocity *= self.linearDamping**duration 
        self.rotation *= self.angularDamping**duration

        #Adjust position
        self.position.addScaledVector(self.velocity, duration)

        #Adjust orientation
        self.orientation.addScaledVector(self.rotation, duration)

        #Normalize oriantation, update transform matrix and inertia tensor in world space
        self.calculateDerivedData()

        #Clear all accumulators
        self.clearAccumulators()

        #Update kinetic energy stored as well as put body to sleep
        if(self.canSleep):
            currentMotion = velocity.scalarProduct(velocity) + rotation.scalarProduct(rotation)
            bias = 0.5**duration

            self.motion = bias*self.motion + (1-bias)*currentMotion

            if motion < SLEEP_EPSILON:
                self.setAwake(Fasle)
            elif motion > 10*SLEEP_EPSILON:
                motion = 10*SLEEP_EPSILON

    ####SETTERS AND GETTERS

    def setMass(self, mass):
        assert(mass != 0);
        self.inverseMass = 1/mass

    def getMass(self):
        if self.inverseMass == 0:
            return float_info.max
        else:
            return 1/self.inverseMass
        
    def setInverseMass(self, inverseMass):
        self.inverseMass = inverseMass

    def getInverseMass(self):
        return self.inverseMass

    def hasFiniteMass(self):
        return self.inverseMass >= 0

    
    def setInertiaTensor(self, inertiaTensor):
        '''
            set inertia tensor and save it as inverse  
            ---------
            args:
                inertiaTensor - Matrix3
        '''
        #Repeating the code here for "optimization" Ha ha!
    
        self.inverseInertiaTensor.setInverse(inertiaTensor)

        t4 = self.transformMatrix.data[0]*self.inverseInertiaTensor.data[0]+ self.transformMatrix.data[1]\
            *self.inverseInertiaTensor.data[3]+ self.transformMatrix.data[2]*self.inverseInertiaTensor.data[6]
        t9 = self.transformMatrix.data[0]*self.inverseInertiaTensor.data[1]+ self.transformMatrix.data[1]\
            *self.inverseInertiaTensor.data[4]+ self.transformMatrix.data[2]*self.inverseInertiaTensor.data[7]
        t14 = self.transformMatrix.data[0]*self.inverseInertiaTensor.data[2]+ self.transformMatrix.data[1]\
            *self.inverseInertiaTensor.data[5]+ self.transformMatrix.data[2]*self.inverseInertiaTensor.data[8]
        t28 = self.transformMatrix.data[4]*self.inverseInertiaTensor.data[0]+ self.transformMatrix.data[5]\
            *self.inverseInertiaTensor.data[3]+ self.transformMatrix.data[6]*self.inverseInertiaTensor.data[6]
        t33 = self.transformMatrix.data[4]*self.inverseInertiaTensor.data[1]+ self.transformMatrix.data[5]\
            *self.inverseInertiaTensor.data[4]+ self.transformMatrix.data[6]*self.inverseInertiaTensor.data[7]
        t38 = self.transformMatrix.data[4]*self.inverseInertiaTensor.data[2]+ self.transformMatrix.data[5]\
            *self.inverseInertiaTensor.data[5]+ self.transformMatrix.data[6]*self.inverseInertiaTensor.data[8]
        t52 = self.transformMatrix.data[8]*self.inverseInertiaTensor.data[0]+ self.transformMatrix.data[9]\
            *self.inverseInertiaTensor.data[3]+ self.transformMatrix.data[10]*self.inverseInertiaTensor.data[6]
        t57 = self.transformMatrix.data[8]*self.inverseInertiaTensor.data[1]+ self.transformMatrix.data[9]\
            *self.inverseInertiaTensor.data[4]+ self.transformMatrix.data[10]*self.inverseInertiaTensor.data[7]
        t62 = self.transformMatrix.data[8]*self.inverseInertiaTensor.data[2]+ self.transformMatrix.data[9]\
            *self.inverseInertiaTensor.data[5]+ self.transformMatrix.data[10]*self.inverseInertiaTensor.data[8]

        self.inverseInertiaTensorWorld.data[0] = t4*self.transformMatrix.data[0]+ t9*self.transformMatrix.data[1]\
            + t14*self.transformMatrix.data[2]
        self.inverseInertiaTensorWorld.data[1] = t4*self.transformMatrix.data[4]+ t9*self.transformMatrix.data[5]\
            + t14*self.transformMatrix.data[6]
        self.inverseInertiaTensorWorld.data[2] = t4*self.transformMatrix.data[8]+ t9*self.transformMatrix.data[9]\
            + t14*self.transformMatrix.data[10]
        self.inverseInertiaTensorWorld.data[3] = t28*self.transformMatrix.data[0]+ t33*self.transformMatrix.data[1]\
            + t38*self.transformMatrix.data[2]
        self.inverseInertiaTensorWorld.data[4] = t28*self.transformMatrix.data[4]+ t33*self.transformMatrix.data[5]\
            + t38*self.transformMatrix.data[6]
        self.inverseInertiaTensorWorld.data[5] = t28*self.transformMatrix.data[8]+ t33*self.transformMatrix.data[9]\
            + t38*self.transformMatrix.data[10]
        self.inverseInertiaTensorWorld.data[6] = t52*self.transformMatrix.data[0]+ t57*self.transformMatrix.data[1]\
            + t62*self.transformMatrix.data[2]
        self.inverseInertiaTensorWorld.data[7] = t52*self.transformMatrix.data[4]+ t57*self.transformMatrix.data[5]\
            + t62*self.transformMatrix.data[6]
        self.inverseInertiaTensorWorld.data[8] = t52*self.transformMatrix.data[8]+ t57*self.transformMatrix.data[9]\
            + t62*self.transformMatrix.data[10]

    def getInertiaTensor(self):
        inertiaTensor = Matrix3()
        inertiaTensor.setInverse(self.inverseInertiaTensor)
        return inertiaTensor

    def getInertiaTensorWorld(self):
        inertiaTensorWorld = Matrix3()
        inertiaTensorWorld.setInverse(self.inverseInertiaTensorWorld)
        return inertiaTensorWorld

    def setInverseInertiaTensor(self, inverseInertiaTensor):
        self.inverseInertiaTensor = inverseInertiaTensor


    def getInverseInertiaTensor(self):
        return self.inverseInertiaTensor.copy()


    def getInverseInertiaTensorWorld(self):
        return self.inverseInertiaTensorWorld.copy()

    def getTransform(self):
        return self.transformMatrix.copy() 


    def setDamping(self, linearDamping, angularDamping):
        self.linearDamping = linearDamping
        self.angularDamping = angularDamping

    def setLinearDamping(self, linearDamping):
        self.linearDamping = linearDamping


    def getLinearDamping(self):
        return self.linearDamping


    def setAngularDamping(self, angularDamping):
        angularDamping = angularDamping


    def getAngularDamping(self):
        return self.angularDamping

    def setPosition(self, x, y, z):
        self.position.x = x
        self.position.y = y
        self.position.z = z

    def getPosition(self):
        return Vector(self.position.x,self.position.y,self.position.z)
    
    def setOrientation(self, r, i, j, k):
        self.orientation.r = r;
        self.orientation.i = i;
        self.orientation.j = j;
        self.orientation.k = k;
        self.orientation.normalize();

    def getOrientation(self, o=0): 
        if isinstance(o, Quaternion):
            o.r = self.orientation.r
            o.i = self.orientation.i
            o.j = self.orientation.j
            o.k = self.orientation.k
        elif isinstance(o, Matrix3):
            o.data[0] = self.transformMatrix.data[0]
            o.data[1] = self.transformMatrix.data[1]
            o.data[2] = self.transformMatrix.data[2]

            o.data[3] = self.transformMatrix.data[4]
            o.data[4] = self.transformMatrix.data[5]
            o.data[5] = self.transformMatrix.data[6]

            o.data[6] = self.transformMatrix.data[8]
            o.data[7] = self.transformMatrix.data[9]
            o.data[8] = self.transformMatrix.data[10]
        else:
            return self.orientation.copy()
        
    def setAcceleration(self, x,  y, z):
        self.acceleration.x = x
        self.acceleration.y = y
        self.acceleration.z = z

    def getAcceleration(self):
        return Vector(self.acceleration.x,self.acceleration.y,self.acceleration.z)

    def getLastFrameAcceleration(self):
        return Vector(self.lastFrameAcceleration.x,self.lastFrameAcceleration.y,self.lastFrameAcceleration.z)


    def setVelocity(self, x, y, z):
        self.velocity.x = x
        self.velocity.y = y
        self.velocity.z = z

    def getVelocity(self):
        return Vector(self.velocity.x,self.velocity.y,self.velocity.z)

    def addVelocity(self, deltaVelocity):
        self.velocity += deltaVelocity;

    def setRotation(self, x, y, z):
        self.rotation.x = x
        self.rotation.y = y
        self.rotation.z = z

    def getRotation(self):
        return Vector(self.rotation.x,self.rotation.y,self.rotation.z)


    def addRotation(self, deltaRotation):
        self.rotation += deltaRotation

    def setAwake(self, awake = True):
        if awake:
            self.isAwake= True
            #Add a bit of kinetic energy to avoid it sleeping immediatly
            self.motion = SLEEP_EPSILON*2
        else:
            self.isAwake = False;
            self.velocity.clear()
            self.rotation.clear()

    def setCanSleep(self, canSleep):
        self.canSleep = canSleep;
        if not self.canSleep and not self.isAwake: 
            self.setAwake();

    def clearAccumulators(self):
        self.forceAccum.clear()
        self.torqueAccum.clear()


    #####Transform object space to world space and visa versa
    def getPointInLocalSpace(self, point):
        return self.transformMatrix.transformInverse(point)

    def getPointInWorldSpace(self, point):
        return self.transformMatrix.transform(point)

    def getDirectionInLocalSpace(self, direction):
        return self.transformMatrix.transformInverseDirection(direction)

    def getDirectionInWorldSpace(self, direction):
        return self.transformMatrix.transformDirection(direction)

    ####Adding Force and torque 
    def addForce(self, force):
        self.forceAccum += force;
        self.isAwake = True;

    def addForceAtBodyPoint(self, force, point):
        #Convert to coordinates relative to center of mass
        pt = self.getPointInWorldSpace(point)
        self.addForceAtPoint(force, pt)

    def addForceAtPoint(self, force, point):
        #Convert to coordinates relative to center of mass.
        pt = Vector(point.x,point.y,point.z)
        pt -= self.position

        self.forceAccum += force
        self.torqueAccum += pt % force

        self.isAwaWke = True

    def addTorque(self, torque):
        self.torqueAccum += torque
        self.isAwake = true