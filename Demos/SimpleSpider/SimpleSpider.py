from sys import path
path.insert(0, '../../')   

from Typhoon import *
from random import uniform
from vpython import *


drawGraphics = True 


class Legs(CollisionBox):
    def __init__(self):
        super().__init__()
        self.body = RigidBody()
        if drawGraphics:
            self.shape = box()
            self.sphere = sphere()

    def display(self):
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
    
     #We use a sphere to collide bone on bone to allow some limited
     #interpenetration.
    def getCollisionSphere(self):   
        sphere = CollisionSphere()
        sphere.body = self.body;
        sphere.radius = self.halfSize.x;
        if self.halfSize.y < sphere.radius: sphere.radius = self.halfSize.y;
        if self.halfSize.z < sphere.radius: sphere.radius = self.halfSize.z;
        sphere.calculateInternals();
        return sphere

    #Sets the bone to a specific location.
    def setState(self, position: "Vector", extents: "Vector"):
        self.body.setPosition(position.x, position.y, position.z)
        self.halfSize = extents.copy()

        mass = self.halfSize.x * self.halfSize.y * self.halfSize.z * 8.0
        self.body.setMass(mass)
        tensor = Matrix3()
        tensor.setBlockInertiaTensor(self.halfSize, mass)
        self.body.setInertiaTensor(tensor)

        self.body.setLinearDamping(0.95)
        self.body.setAngularDamping(0.8)
        self.body.clearAccumulators()
        self.body.setAcceleration(0,-9.81 ,0)

        self.body.setCanSleep(False)
        self.body.setAwake()

        self.body.calculateDerivedData();
        self.calculateInternals();

class Head(CollisionSphere):
    def __init__(self):
        super().__init__()
        self.body = RigidBody()
        if drawGraphics:
            self.sphere = sphere()

    def display(self):
        #Body position and axis
        pos = self.body.transformMatrix.getAxisVector(3)
        #Use graphics library
        pos = pos.toVPython()
        self.sphere.color = color.red
        self.sphere.pos = pos
        self.sphere.radius = self.radius

     #We use a sphere to collide bone on bone to allow some limited
     #interpenetration.
    def getCollisionSphere(self): 
        self.calculateInternals();
        return self

    #Sets the bone to a specific location.
    def setState(self, position: Vector, radius: float):
        self.body.setPosition(position.x, position.y, position.z)
        self.radius = radius
        mass = self.radius * self.radius * self.radius * 8.0
        self.body.setMass(mass)
        tensor = Matrix3()
        tensor.setBlockInertiaTensor(Vector(self.radius,self.radius,self.radius), mass)
        self.body.setInertiaTensor(tensor)
        self.body.setLinearDamping(0.95)
        self.body.setAngularDamping(0.8)
        self.body.clearAccumulators()
        self.body.setAcceleration(0,-9.81 ,0)
        self.body.setCanSleep(False)
        self.body.setAwake()
        self.body.calculateDerivedData();
        self.calculateInternals();


class jointgraphics:
    def __init__(self):
        self.joint = Joint()
        if drawGraphics:
            self.cylinder = cylinder()
        
    def display(self):
        a_pos_world = self.joint.body[0].getPointInWorldSpace(self.joint.position[0])
        b_pos_world = self.joint.body[1].getPointInWorldSpace(self.joint.position[1])
        a_to_b = b_pos_world - a_pos_world
        self.cylinder.pos = b_pos_world.toVPython()
        self.cylinder.axis = a_to_b.toVPython()
        self.cylinder.radius = 0.2
        self.cylinder.color = color.green

class SimpleSpider():
    FREQ = 60
    NUM_LEGS = 4
    NUM_JOINTS = 4
    NUM_HEAD = 1
    
    def __init__(self):
        self.MAX_CONTACT = 32
        #Array of contacts
        self.contacts = []
        #Data of collision detector
        self.cData = CollisionData()
        self.cData.contactArray = self.contacts
        self.resolver = ContactResolver(self.MAX_CONTACT*6,self.MAX_CONTACT*6)
        self.Registry = []
        self.forceRegistry = ForceRegistry()
        self.aeroForce = Aero(Matrix3(0,0,0, -1,-0.5,0, 0,0,-0.1), Vector(0, 0, 0), Vector(0,0,0))
        

        #True if the contacts should be rendered.
        self.renderDebugInfo = False
        #True if the simulation is paused. 
        self.pauseSimulation = False
        #Pauses the simulation after the next frame automatically 
        self.autoPauseSimulation = False

        #Setup bones and joints
        self.legs = []
        self.joints = []
        self.head = Head()
        for i in range(self.NUM_LEGS):
            self.legs.append(Legs())
        for i in range(self.NUM_JOINTS):
            self.joints.append(jointgraphics())

        self.forceRegistry.add(self.head.body, self.aeroForce)

        self.legExtend = Vector(0.301, 2.0, 0.234)
        self.radius = 1.5
       
        #Assign joints to self.bones
        #Right front Leg
        self.joints[0].joint.set(self.legs[0].body, Vector(0, self.legExtend.y, 0), self.head.body, Vector(self.radius/2, -self.radius/2, self.radius/(2**(1/2))), 0.15)
        #Left front Leg
        self.joints[1].joint.set(self.legs[1].body, Vector(0, self.legExtend.y, 0), self.head.body, Vector(self.radius/2, -self.radius/2, -self.radius/(2**(1/2))), 0.15)
        #Right back leg
        self.joints[2].joint.set(self.legs[2].body, Vector(0, self.legExtend.y, 0), self.head.body, Vector(-self.radius/2, -self.radius/2, self.radius/(2**(1/2))), 0.15)
        #Left back leg
        self.joints[3].joint.set(self.legs[3].body, Vector(0, self.legExtend.y, 0), self.head.body, Vector(-self.radius/2, -self.radius/2, -self.radius/(2**(1/2))), 0.15)
        #Reset to initial position
        self.reset();

    def reset(self):
        self.legs[0].setState(Vector(0, 0.993, -0.5), self.legExtend)
        self.legs[1].setState(Vector(0, 3.159, -0.56), self.legExtend)
        self.legs[2].setState(Vector(0, 0.993, 0.5), self.legExtend)
        self.legs[3].setState(Vector(0, 3.15, 0.56), self.legExtend)

        self.legs[0].body.setOrientation(-0.0465445, -0.5998767, 0.3156456, -0.733723)
        self.legs[1].body.setOrientation(-0.0465445, -0.5998767, 0.3156456, -0.733723)
        self.legs[2].body.setOrientation(-0.5998767, -0.0465445, -0.6762527, -0.4250457)
        self.legs[3].body.setOrientation(-0.5998767, -0.0465445, -0.6762527, -0.4250457)


        self.head.setState(Vector(0,4,0),self.radius)


        #Reset the contacts
        self.cData.contactCount = 0

    def updateObjects(self, duration: float):
        for leg in self.legs:
            leg.body.integrate(duration)
            leg.body.clearAccumulators()
            leg.calculateInternals()
            
        
        self.head.body.integrate(duration)
        self.head.calculateInternals()

    def generateContacts(self):
        plane = CollisionPlane()
        plane.direction = Vector(0,1,0)
        plane.offset = 0;

        self.cData.reset(self.MAX_CONTACT)
        self.cData.friction = 1
        self.cData.restitution = 0.2
        self.cData.tolerance = 0.1

        #Perform exhausive collision detection with the floor
        transform = Matrix4()
        otherTransform = Matrix4()
        position = Vector()
        otherPosition = Vector()

        self.cData.reset(self.MAX_CONTACT)

        if not self.cData.hasMoreContacts(): return
        CollisionDetector.sphereAndHalfSpace(self.head, plane, self.cData)

        for i in range(self.NUM_LEGS):
            #Check collision with floor
            if not self.cData.hasMoreContacts(): return

            CollisionDetector.boxAndHalfSpace(self.legs[i], plane, self.cData)
            boneSphere = self.legs[i].getCollisionSphere()
            otherSphere = self.head.getCollisionSphere()
            CollisionDetector.sphereAndSphere(boneSphere, otherSphere, self.cData)

            #Check for collision with each others
            for j in range(i+1, self.NUM_LEGS):
                if not self.cData.hasMoreContacts(): return
                otherSphere = self.legs[j].getCollisionSphere()
                CollisionDetector.sphereAndSphere(boneSphere, otherSphere, self.cData)

        #Check joint violation 
        for joint in self.joints:
            if not self.cData.hasMoreContacts(): return
            added = joint.joint.addContact(self.cData.contactArray, self.cData.contactsLeft)
            self.cData.addContacts(added)

    def update(self,duration):
        if self.pauseSimulation:
            return
        elif self.autoPauseSimulation:
            self.pauseSimulation = True
            self.autoPauseSimulation = False

        self.updateObjects(duration)
        

        self.forceRegistry.updateForces(duration)

        self.generateContacts()

        self.resolver.resolveContacts(self.cData.contactArray, self.cData.contactCount,duration)

    def graphicsSetup(self):
        scene.width = scene.height = 600
        L = 50
        d = L-2
        R= L/100
        scene.center = vec(0,0,0)
        scene.range = 0.2*L
        scene.bind('keydown', self.keyInput)
        #zaxis = cylinder(pos=vec(0,0,0), axis=vec(0,0,d), radius=R, color=color.yellow)
        #xaxis = cylinder(pos=vec(0,0,0), axis=vec(d,0,0), radius=R, color=color.yellow)
        #yaxis = cylinder(pos=vec(0,0,0), axis=vec(0,d,0), radius=R, color=color.yellow)
        floor = box (pos=vector( 0, -0.25, 0), size=vector(d, 0.5, d),  color = color.blue)

    def display(self):
        self.head.display()
        for leg in self.legs:
            leg.display()
        for joint in self.joints:
            joint.display()

    def run(self):
        if drawGraphics:
            self.graphicsSetup()
        while(True):
            rate(self.FREQ)
            self.update(1/self.FREQ)
            if drawGraphics:
                self.display()
    
    def addForceOnALeg(self, index):
        self.legs[index].body.addForceAtBodyPoint(Vector(0,-200, 0),Vector(0, -2.0, 0))

    def keyInput(self, evt):
        s = evt.key
        if 'w' in s:
            self.addForceOnALeg(0)
        if 's' in s:
            self.addForceOnALeg(1)
        if 'a' in s:
            self.addForceOnALeg(2)
        if 'd' in s:
            self.addForceOnALeg(3)

    

x = SimpleSpider()
x.run()

