from sys import path
path.insert(0, '../../')    

from vpython import *
from Typhoon import *
from random import uniform

class SailBoatDemo:
    '''
        Class which renders a simulation of a boat moving in the water, this demo demonstrates
        force generators including bouancy, wind, and drag.
        ---------
        properties:
            sailBoat            - SailBoat      - Rigidbody and its graphics
            buoyancyForceFront  - Buoyancy      - Force acting on front of boat
            buoyancyForceBack   - Buoyancy      - Force acting on back of boat
            windSpeed           - Vector        - Wind speed in simulation in world space
            aeroForce           - Aero          - Aero force acting on boat's sail
            forceRegistry       - ForceRegistry - Keeps track of all forces in simulation
    '''

    FREQ = 30   # frequency of simulation

    class SailBoat:
        '''
            Class responsible for rendering and keeping the sail boat body
            ---------
            properties:
                boat - RigidBody 
                body - vpython.sphere
                rod  - vpython.cylinder
                sail - vpython.pyramid
        '''

        def __init__(self):
            '''
                Class constractor
            '''

            self.boat = RigidBody()
            self.body = box()
            self.rod = cylinder(radius=0.3)
            self.sail = pyramid(color = color.white)
            

    def __init__(self):
        '''
            Class constractor
        '''

        self.sailBoat = SailBoatDemo.SailBoat()

        #Forces acting in environment
        self.buoyancyForceFront = Buoyancy(self.sailBoat.boat.position+Vector(-0.51,0,0),0.6,2,1.6)
        self.buoyancyForceBack = Buoyancy(self.sailBoat.boat.position+Vector(0.5,0,0),0.6,2,1.6)

        self.windSpeed = Vector()
        self.aeroForce = Aero(Matrix3(0,0,0, 0,0,0, -1,0, -1), Vector(2, 0, 0), self.windSpeed)
        #force registery
        self.forceRegistry = ForceRegistry()

        #Set body properties
        self.sailBoat.boat.setPosition(0, 1.5, 0)
        self.sailBoat.boat.setOrientation(1,0,0,0)
        self.sailBoat.boat.setVelocity(0,0,0)
        self.sailBoat.boat.setRotation(0,0,0)

        self.sailBoat.boat.setMass(200.0)
        it = Matrix3()
        it.setBlockInertiaTensor(Vector(2,1,1), 100)
        self.sailBoat.boat.setInertiaTensor(it)

        self.sailBoat.boat.setDamping(0.8, 0.4)

        self.sailBoat.boat.setAcceleration(0.3,-9.81,0)
        self.sailBoat.boat.calculateDerivedData()

        self.sailBoat.boat.setAwake()
        self.sailBoat.boat.setCanSleep(False)

        #Add forces to force registery
        self.forceRegistry.add(self.sailBoat.boat, self.aeroForce)
        self.forceRegistry.add(self.sailBoat.boat, self.buoyancyForceBack)
        self.forceRegistry.add(self.sailBoat.boat, self.buoyancyForceFront)
    
    def update(self,duration):
        '''
            Method called to update simulation on time step
        '''

        #Clear accumlators so zero forces and torque
        self.sailBoat.boat.clearAccumulators();

        #Add forces to body.
        self.forceRegistry.updateForces(duration);

        #Update the boat's physics.
        self.sailBoat.boat.integrate(duration);

        #Change the wind speed.
        self.windSpeed = self.windSpeed * 0.9 + Vector(uniform(0,100), 0,uniform(0,100))


    def display(self):
        '''
            Method draw the simulation called before each time step
        '''

        pos = self.sailBoat.boat.transformMatrix.getAxisVector(3)
        boatAxis = self.sailBoat.boat.transformMatrix.getAxisVector(0)
        rodAxis = self.sailBoat.boat.transformMatrix.getAxisVector(1)

        offsetSailRod = vector(-4,1.5,0)
        offsetSail = vector(-4,6.5,0)

        offsetSailRod = self.sailBoat.boat.getTransform().transformDirection(offsetSailRod);
        offsetSail = self.sailBoat.boat.getTransform().transformDirection(offsetSail);
        
        pos = vector(pos.x,pos.y,pos.z)
        boatAxis = vector(boatAxis.x,boatAxis.y,boatAxis.z)
        rodAxis = vector(rodAxis.x,rodAxis.y,rodAxis.z)
        offsetSailRod = vector(offsetSailRod.x,offsetSailRod.y,offsetSailRod.z)
        offsetSail = vector(offsetSail.x,offsetSail.y,offsetSail.z)

        self.sailBoat.body.pos = pos
        self.sailBoat.body.axis = boatAxis
        self.sailBoat.body.up = rodAxis
        self.sailBoat.body.size = vector(10,3,4)

        self.sailBoat.rod.pos = pos + offsetSailRod
        self.sailBoat.rod.axis = 6.5 * rodAxis

        self.sailBoat.sail.pos = pos + offsetSail
        self.sailBoat.sail.up = boatAxis
        self.sailBoat.sail.axis = rodAxis
        self.sailBoat.sail.size = vector(10,0.3,5)

    def graphicsSetup(self):
        '''
            Called before simulation starts to set up scene
        '''

        scene.width = scene.height = 600
        L = 50
        d = L-2
        R= L/100
        scene.center = vec(d/2,0,d/2)
        scene.range = L

        xaxis = cylinder(pos=vec(0,0,0), axis=vec(0,0,d), radius=R, color=color.yellow)
        yaxis = cylinder(pos=vec(0,0,0), axis=vec(d,0,0), radius=R, color=color.yellow)
        zaxis = cylinder(pos=vec(0,0,0), axis=vec(0,d,0), radius=R, color=color.yellow)
        floor = box (pos=vector( d/2, -0.5, d/2), size=vector(d, 0.5, d),  color = color.blue)

    def run(self):
        '''
            open loop of simulation
        '''

        self.graphicsSetup()
        while(True):
            rate(self.FREQ)
            self.update(1/self.FREQ)
            self.display()

x = SailBoatDemo()
x.run()