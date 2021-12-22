from sys import path
path.insert(0, '../../')   
from Typhoon import *
from random import uniform
from vpython import *

drawGraphics = True # if we want to render the simulation

class Drone(CollisionBox):
    '''
        Class renders the drone and keep track of its collision box        
        ---------
        properties:
            body    - RigidBody      
            box     - vpython.box     
            motors  - list of vpython.cylinder    
    '''

    def __init__(self):
        '''
            Class constractor
        '''

        super().__init__()
        self.body = RigidBody()
        if drawGraphics:
            self.box = box()
            self.motors = [cylinder(),cylinder(),cylinder(),cylinder()]

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
        #Draw drone
        self.box.pos = pos
        self.box.axis = axis
        self.box.up = up
        self.box.size = (self.halfSize*2).toVPython()
        self.box.color = color.red
        #Draw 4 motors
        self.motors[0].axis = up
        self.motors[0].pos = self.body.getPointInWorldSpace(Vector(self.halfSize.x,2*self.halfSize.y/3,self.halfSize.z)).toVPython()
        self.motors[0].radius = (self.halfSize.x+self.halfSize.z)/4
        self.motors[0].color = color.white
        self.motors[1].axis = up
        self.motors[1].pos = self.body.getPointInWorldSpace(Vector(self.halfSize.x,2*self.halfSize.y/3,-self.halfSize.z)).toVPython()
        self.motors[1].radius = (self.halfSize.x+self.halfSize.z)/4
        self.motors[1].color = color.white
        self.motors[2].axis = up
        self.motors[2].pos = self.body.getPointInWorldSpace(Vector(-self.halfSize.x,2*self.halfSize.y/3,self.halfSize.z)).toVPython()
        self.motors[2].radius = (self.halfSize.x+self.halfSize.z)/4
        self.motors[2].color = color.white
        self.motors[3].axis = up
        self.motors[3].pos = self.body.getPointInWorldSpace(Vector(-self.halfSize.x,2*self.halfSize.y/3,-self.halfSize.z)).toVPython()
        self.motors[3].radius = (self.halfSize.x+self.halfSize.z)/4
        self.motors[3].color = color.white

    def setState(self, position: "Vector", extents: "Vector"):
        '''
            Sets the Drone to a specific location, with specific parameters
            ---------
            args:
                position - Vector - new position of the bone
                extents  - Vector - halfsize of the bone
        '''

        #Set position and size
        self.body.setPosition(position.x, position.y, position.z)
        self.halfSize = extents.copy()

        #Mass and inertia
        mass = self.halfSize.x * self.halfSize.y * self.halfSize.z * 8.0
        self.body.setMass(mass)
        tensor = Matrix3()
        tensor.setBlockInertiaTensor(self.halfSize, mass)
        self.body.setInertiaTensor(tensor)

        #Damping 
        self.body.setLinearDamping(0.95)
        self.body.setAngularDamping(0.8)
        self.body.clearAccumulators()

        #Acceleration
        self.body.setAcceleration(0,-9.81 ,0)

        #Body cant go to sleep 
        self.body.setCanSleep(False)
        self.body.setAwake()

        #Calculate derieved data of both Drone and it's collision box
        self.body.calculateDerivedData();
        self.calculateInternals();

        

class DroneDemo():
    '''
        Class creates a simulation of a drone and a goal that the drone should get to
        This simulation is build to be used by a deep learning algorithm to learn how the four
        motors' prameters should be set so the drone could get to the foal
    '''

    FREQ = 30
    W = [8.1,8.1,8.1,8.1]
    KF = [0.7,0.7,0.7,0.7]
    DRAG_COFF = 0 
    WIND_SPEED = Vector(0, 0, 0)
    

    def __init__(self):
        '''
            Class constractor
        '''

        self.MAX_CONTACT = 32
        self.contacts = []
        self.cData = CollisionData()
        self.cData.contactArray = self.contacts
        self.cData.friction = 1
        self.cData.restitution = 0.2
        self.cData.tolerance = 0.1
        self.resolver = ContactResolver(self.MAX_CONTACT*6,self.MAX_CONTACT*6)
        self.drone = Drone()
        self.forceRegistry = ForceRegistry()
        self.reset(Vector(0,5,0), Vector(3,0.4,2))
        
        self.goalSphere = sphere()
        self.goalSphere.pos = vector(0,10,0)
        self.goalSphere.color = color.red
        self.goalSphere.opacity = 0.3


    

    def addForces(self, kf, w, dragCoff, windSpeed):
        '''
            Add forces to simulation on drone
            ---------
            args:
                kf          - list   - four doubles which represent drone constant
                w           - list   - four double which represent motors angulr velocity
                dragCoff    - double - drag coff applied to the drone while flying
                windSpeed   - Vector - wind speed in worlds space
        '''

        aeroForce = Aero(Matrix3(0,0,0, -1,-0.5,0, 0,0,-0.1), Vector(0, self.drone.halfSize.y, 0), windSpeed)
        rightForwardMotorThrust = DroneThrust(kf[0],w[0],Vector(self.drone.halfSize.x,self.drone.halfSize.y,self.drone.halfSize.z))
        leftForwardMotorThrust = DroneThrust(kf[1],w[1],Vector(self.drone.halfSize.x,self.drone.halfSize.y,-self.drone.halfSize.z))
        rightBackwardMotorThrust = DroneThrust(kf[2],w[2],Vector(-self.drone.halfSize.x,self.drone.halfSize.y,self.drone.halfSize.z))
        leftBackwardMotorThrust = DroneThrust(kf[3],w[3],Vector(-self.drone.halfSize.x,self.drone.halfSize.y,-self.drone.halfSize.z))
        dragzy = Drag(dragCoff, self.drone.halfSize.z*self.drone.halfSize.y)
        dragxz = Drag(dragCoff, self.drone.halfSize.z*self.drone.halfSize.x)
        dragxy = Drag(dragCoff, self.drone.halfSize.x*self.drone.halfSize.y)
        self.forceRegistry.add(self.drone.body, aeroForce)
        self.forceRegistry.add(self.drone.body, rightForwardMotorThrust)
        self.forceRegistry.add(self.drone.body, leftForwardMotorThrust)
        self.forceRegistry.add(self.drone.body, rightBackwardMotorThrust)
        self.forceRegistry.add(self.drone.body, leftBackwardMotorThrust)
        self.forceRegistry.add(self.drone.body, dragzy)
        self.forceRegistry.add(self.drone.body, dragxz)
        self.forceRegistry.add(self.drone.body, dragxy)

    def reset(self, position, extent):
        '''
            resets the simulation into an intial state
        '''

        self.drone.setState(position, extent)
        self.cData.reset(self.MAX_CONTACT)

    def updateObjects(self, duration: float):
        '''
            Method called to update drone called on time step
        '''

        self.drone.body.integrate(duration)
        self.drone.calculateInternals()

    def generateContacts(self):
        '''
            Method called to detect and generate the contacts 
        '''

        #Ground
        plane = CollisionPlane()
        plane.direction = Vector(0,1,0)
        plane.offset = 0;
        #Contact data reset
        self.cData.reset(self.MAX_CONTACT)
        #Drone collision with ground
        CollisionDetector.boxAndHalfSpace(self.drone, plane, self.cData)

    def update(self,duration):
        '''
            Method called to update simulation called on time step
        '''

        self.forceRegistry.clear()
        self.addForces(self.KF,self.W, self.DRAG_COFF, self.WIND_SPEED)
        self.forceRegistry.updateForces(duration)
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
        scene.camera.follow(self.drone.box)
        scene.range = 0.2*L
        scene.bind('keydown', self.keyInput)
        floor = box (pos=vector( 0, -0.25, 0), size=vector(d, 0.5, d),  color = color.blue)

    def display(self):
        '''
            Called on each time step to display simulation objects
        '''

        self.drone.display()

    def run(self):
        '''
            open loop of simulation
        '''

        if drawGraphics:
            self.graphicsSetup()
        while(True):
            rate(self.FREQ)
            self.update(1/self.FREQ)
            if drawGraphics:
                self.display()
    
    def keyInput(self, evt):
        if evt.key == 'w' or evt.key == 'W':
            self.goalSphere.pos.z -= 1
            #w[0] += 0.1
        elif evt.key == 's' or evt.key == 'S':
            self.goalSphere.pos.z += 1
            #w[0] -= 0.1
        elif evt.key == 'a' or evt.key == 'A':
            self.goalSphere.pos.x -= 1
            #w[1] -= 0.1
        elif evt.key == 'd' or evt.key == 'D':
            self.goalSphere.pos.x += 1
            #w[2] -= 0.1
        elif evt.key == 'q' or evt.key == 'Q':
            #w[1] += 0.1
            self.goalSphere.pos.y -= 1
        elif evt.key == 'e' or evt.key == 'E':
            #w[2] += 0.1
            self.goalSphere.pos.y += 1
        elif evt.key == 'r' or evt.key == 'R':
            pass
            #w[3] += 0.1
        elif evt.key == 'f' or evt.key == 'F':
            pass
            #w[3] -= 0.1
        elif evt.key == 'z' or evt.key == 'Z':
            pass
            #w[0] = w[1] = w[2] = w[3] = 0

x = DroneDemo()
x.run()


