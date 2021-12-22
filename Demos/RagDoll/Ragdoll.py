from sys import path
path.insert(0, '../../')   

from Typhoon import *
from random import uniform
from vpython import *

class Bone(CollisionBox):
    '''
        Class acts as a collision box for the bones of the ragdoll,
        it renders center of collision box as a sphere
        ---------
        properties:
            body    - RigidBody      
            shape   - vpython.box     
            sphere  - vpython.sphere    
    '''

    def __init__(self):
        '''
            Class constractor
        '''

        super().__init__()
        self.body = RigidBody()
        self.shape = box()
        self.sphere = sphere()

    def display(self):
        '''
            Method used to draw the bone and its collision box
        '''

        #Body position and axis
        pos = self.body.transformMatrix.getAxisVector(3)
        axis = self.body.transformMatrix.getAxisVector(0)
        up = self.body.transformMatrix.getAxisVector(1)

        #Use graphics library
        pos = pos.toVPython()
        axis = axis.toVPython()
        up = up.toVPython()

        self.sphere.opacity = 0.2
        self.sphere.color = color.red
        self.sphere.pos = pos
        radius = self.halfSize.x + self.halfSize.x * 0.2
        if self.halfSize.y < radius: radius = self.halfSize.y + self.halfSize.y * 0.2
        if self.halfSize.z < radius: radius = self.halfSize.z + self.halfSize.z * 0.2
        self.sphere.radius = radius

        self.shape.pos = pos
        self.shape.axis = axis
        self.shape.up = up
        self.shape.size = (self.halfSize*2).toVPython()

    def getCollisionSphere(self):   
        '''
            Method called to get collision sphere of bone
            collision sphere used to collide bone on bone to allow some limited interpenetration
        '''

        sphere = CollisionSphere()
        sphere.body = self.body;
        sphere.radius = self.halfSize.x;
        if self.halfSize.y < sphere.radius: sphere.radius = self.halfSize.y;
        if self.halfSize.z < sphere.radius: sphere.radius = self.halfSize.z;
        sphere.calculateInternals();
        return sphere

    def setState(self, position, extents):
        '''
            Sets the bone to a specific location
            ---------
            args:
                position - Vector - new position of the bone
                extents  - Vector - halfsize of the bone
        '''

        self.body.setPosition(position.x, position.y, position.z)
        self.halfSize = extents

        mass = self.halfSize.x * self.halfSize.y * self.halfSize.z * 8.0
        self.body.setMass(mass)

        tensor = Matrix3()
        tensor.setBlockInertiaTensor(self.halfSize, mass)
        self.body.setInertiaTensor(tensor)

        self.body.setLinearDamping(0.95)
        self.body.setAngularDamping(0.8)
        self.body.clearAccumulators()
        self.body.setAcceleration(0,-2 ,0)

        self.body.setCanSleep(False)
        self.body.setAwake()

        self.body.calculateDerivedData();
        self.calculateInternals();

class RagdollDemo():
    '''
        Class which renders a simulation of a boat moving in the water, this demo demonstrates
        force generators including bouancy, wind, and drag.
        ---------
        properties:
            MAX_CONTACT - int             - constant of max allowed contacts in a time step
            contacts    - list            - all contacts in the simulation
            cData       - CollisionData   - holds all collision data of the simulation
            resolver    - ContactResolver 
            bones       - list            - all bones in the simulation
            joints      - list            - all joints in the simulation

            sailBoat            - SailBoat      - Rigidbody and its graphics
            buoyancyForceFront  - Buoyancy      - Force acting on front of boat
            buoyancyForceBack   - Buoyancy      - Force acting on back of boat
            windSpeed           - Vector        - Wind speed in simulation in world space
            aeroForce           - Aero          - Aero force acting on boat's sail
            forceRegistry       - ForceRegistry - Keeps track of all forces in simulation
    '''

    FREQ = 30       # Frequency of the simulation 
    NUM_BONES = 12  # Number of bones in the simulation
    NUM_JOINTS = 11 # NUmber of joints between the bones
    
    def __init__(self):
        '''
            Class constractor
        '''

        self.MAX_CONTACT = 256
        self.contacts = []
        self.cData = CollisionData()
        self.cData.contactArray = self.contacts
        self.resolver = ContactResolver(self.MAX_CONTACT*8,self.MAX_CONTACT*8)

        #Setup bones and joints
        self.bones = []
        self.joints = []
        for i in range(self.NUM_BONES):
            self.bones.append(Bone())
        for i in range(self.NUM_JOINTS):
            self.joints.append(Joint())

        #Assign joints to self.bones
        #Right Knee
        self.joints[0].set(self.bones[0].body, Vector(0, 1.07, 0), self.bones[1].body, Vector(0, -1.07, 0), 0.15)
        #Left Knee
        self.joints[1].set(self.bones[2].body, Vector(0, 1.07, 0), self.bones[3].body, Vector(0, -1.07, 0), 0.15)
        #Right elbow
        self.joints[2].set(self.bones[9].body, Vector(0, 0.96, 0), self.bones[8].body, Vector(0, -0.96, 0), 0.15)
        #Left elbow
        self.joints[3].set(self.bones[11].body, Vector(0, 0.96, 0), self.bones[10].body, Vector(0, -0.96, 0), 0.15)
        #Stomach to Waist
        self.joints[4].set(self.bones[4].body, Vector(0.054, 0.50, 0), self.bones[5].body, Vector(-0.043, -0.45, 0), 0.15)
        self.joints[5].set(self.bones[5].body, Vector(-0.043, 0.411, 0), self.bones[6].body, Vector(0, -0.411, 0), 0.15)
        self.joints[6].set(self.bones[6].body, Vector(0, 0.521, 0), self.bones[7].body, Vector(0, -0.752, 0), 0.15)
        #Right hip
        self.joints[7].set(self.bones[1].body, Vector(0, 1.066, 0), self.bones[4].body, Vector(0, -0.458, -0.5), 0.15)
        #Left Hip
        self.joints[8].set(self.bones[3].body, Vector(0, 1.066, 0), self.bones[4].body, Vector(0, -0.458, 0.5), 0.105)
        #Right shoulder
        self.joints[9].set(self.bones[6].body, Vector(0, 0.367, -0.8), self.bones[8].body, Vector(0, 0.888, 0.32), 0.15)
        #Left shoulder
        self.joints[10].set(self.bones[6].body, Vector(0, 0.367, 0.8), self.bones[10].body, Vector(0, 0.888, -0.32), 0.15)

        #Reset to initial position
        self.reset();

    def reset(self):
        '''
            resets the simulation into an intial state
        '''

        self.bones[0].setState(Vector(0, 0.993, -0.5), Vector(0.301, 1.0, 0.234))
        self.bones[1].setState(Vector(0, 3.159, -0.56), Vector(0.301, 1.0, 0.234))
        self.bones[2].setState(Vector(0, 0.993, 0.5), Vector(0.301, 1.0, 0.234))
        self.bones[3].setState(Vector(0, 3.15, 0.56), Vector(0.301, 1.0, 0.234))
        self.bones[4].setState(Vector(-0.054, 4.683, 0.013), Vector(0.415, 0.392, 0.690))
        self.bones[5].setState(Vector(0.043, 5.603, 0.013), Vector(0.301, 0.367, 0.693))
        self.bones[6].setState(Vector(0, 6.485, 0.013), Vector(0.435, 0.367, 0.786))
        self.bones[7].setState(Vector(0, 7.759, 0.013), Vector(0.45, 0.598, 0.421))
        self.bones[8].setState(Vector(0, 5.946, -1.066), Vector(0.267, 0.888, 0.207))
        self.bones[9].setState(Vector(0, 4.024, -1.066), Vector(0.267, 0.888, 0.207))
        self.bones[10].setState(Vector(0, 5.946, 1.066), Vector(0.267, 0.888, 0.207))
        self.bones[11].setState(Vector(0, 4.024, 1.066), Vector(0.267, 0.888, 0.207))

        #hit the following bones with a force
        self.bones[6].body.addForceAtBodyPoint(Vector(100, 0, 0), Vector(0, 0, 0))
        self.bones[0].body.addForceAtBodyPoint(Vector(-100, 0, 0), Vector(0, 0, 0))
        self.bones[2].body.addForceAtBodyPoint(Vector(-100, 0, 0), Vector(0, 0, 0))

        #Reset the contacts
        self.cData.contactCount = 0

    def updateObjects(self, duration: float):
        '''
            Method called to update bones called on time step
        '''

        for bone in self.bones:
            bone.body.integrate(duration)
            bone.calculateInternals()

    def generateContacts(self):
        '''
            Method called to detect and generate the contacts 
        '''

        plane = CollisionPlane()
        plane.direction = Vector(0,1,0)
        plane.offset = 0;

        self.cData.reset(self.MAX_CONTACT)
        self.cData.friction = 0.9
        self.cData.restitution = 0.6
        self.cData.tolerance = 0.1

        #Perform exhausive collision detection with the floor
        transform = Matrix4()
        otherTransform = Matrix4()
        position = Vector()
        otherPosition = Vector()

        self.cData.reset(self.MAX_CONTACT)

        for i in range(self.NUM_BONES):
            #Check collision with floor
            if not self.cData.hasMoreContacts(): return

            CollisionDetector.boxAndHalfSpace(self.bones[i], plane, self.cData)
            boneSphere = self.bones[i].getCollisionSphere()

            #Check for collision with each others
            for j in range(i+1, self.NUM_BONES):
                if not self.cData.hasMoreContacts(): return
                otherSphere = self.bones[j].getCollisionSphere()
                CollisionDetector.sphereAndSphere(boneSphere, otherSphere, self.cData)

        #Check joint violation 
        for joint in self.joints:
            if not self.cData.hasMoreContacts(): return
            added = joint.addContact(self.cData.contactArray, self.cData.contactsLeft)
            self.cData.addContacts(added)

    def update(self,duration):
        '''
            Method called to update simulation called on time step
        '''
        self.updateObjects(duration)
        
        self.generateContacts()

        self.resolver.resolveContacts(self.cData.contactArray, self.cData.contactCount,duration)

    def graphicsSetup(self):
        '''
            Called before simulation starts to set up scene
        '''

        scene.width = scene.height = 600
        L = 50
        d = 500
        R= L/100
        scene.center = vec(0,0,0)
        scene.camera.pos = vector(1,4,1)
        scene.range = 0.2*L
        floor = box (pos=vector( 0,0,0), size=vector(d, 0.5, d),  color = color.blue)

    def run(self):
        '''
            open loop of simulation
        '''

        self.graphicsSetup()
        while(True):
            rate(self.FREQ)
            self.update(1/self.FREQ)
            for bone in self.bones:
                bone.display()

x = RagdollDemo()
x.run()
  