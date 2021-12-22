from sys import path
path.insert(0, '../../')    

from vpython import *
from Typhoon import *

class BridgeDemo:
    '''
        Class which renders a simulation of a mass moving on a bridge, this demo demonstrates
        the links (rods, cables), force generators, and contact resolution of Typhoon
        ---------
        properties:
            world                   - ParticleWorld  - used to keep track of particles inside simulation 
            particleArray           - list           - list of all particles in simulation   
            rods                    - list           - list of all rods in simulation
            cables                  - list           - list of all cables in simulation
            supports                - list           - list of all anchored cables in simulation
            massPosition            - Vector         - Extra mass real position
            massDisplayPosition     - Vector         - Extra mass display position
            massDisplayPositionBall - vpython.sphere - used for graphics purposes
        ---------
        we use two vectors for extra mass position to delay calculation of platform slope
    '''

    ROD_COUNT = 6       # Number of rods in simmulation
    SUPPORT_COUNT = 12  # Number of anchored cables in simulation
    CABLE_COUNT = 10    # Number of cables between bridge steps
    PARTICLE_COUNT = 12 # Number of nodes of bridge

    BASE_MASS = 1       # Mass of each particle in bridge
    EXTRA_MASS = 20     # Mass of extra mass moving on the platform

    FREQ = 30           # frequency of simulation

    class ParticleGraphics:
        '''
            Class responsible for rendering particles
            ---------
            properties:
                particle - Particle 
                ball     - vpython.sphere
        '''

        def __init__(self):
            '''
                Class constractor
            '''

            self.particle = Particle()
            self.ball = sphere (color = color.green, radius = 0.2)

    class CableGraphics:
        '''
            Class responsible for rendering cable links
            ---------
            properties:
                rod     - ParticleRod 
                shape   - vpython.cylinder
        '''

        def __init__(self):
            '''
                Class constractor
            '''
            self.cable = ParticleCable()
            self.shape = cylinder(radius = 0.1,color=color.cyan)

    class CableConstrainGraphics:
        '''
            Class responsible for rendering anchored cable links
            ---------
            properties:
                rod     - ParticleRod 
                shape   - vpython.cylinder
        '''

        def __init__(self):
            '''
                Class constractor
            '''

            self.support = ParticleCableConstrain()
            self.shape = cylinder(radius = 0.1,color=color.orange)

    class RodGraphics:
        '''
            Class responsible for rendering rod links
            ---------
            properties:
                rod     - ParticleRod 
                shape   - vpython.cylinder
        '''

        def __init__(self):
            '''
                Class constractor
            '''

            self.rod = ParticleRod()
            self.shape = cylinder(radius = 0.1,color=color.blue)

    def __init__(self):
        '''
            Class constractor
        '''

        self.world = ParticleWorld(self.PARTICLE_COUNT*10)
        self.particleArray = []
        self.cables = []
        self.rods = []
        self.supports = []
        self.massPosition = Vector(0,0,0.5)
        self.massDisplayPosition = Vector()
        self.massDisplayPositionBall = sphere (color = color.black, radius = 0.25)

        #setup patricles and their properties
        for i in range(self.PARTICLE_COUNT):
            self.particleArray.append(BridgeDemo.ParticleGraphics())
            self.particleArray[i].particle.setPosition(i-5,4,(i%2)*2-1)
            self.particleArray[i].particle.setMass(self.BASE_MASS)
            self.particleArray[i].particle.setDamping(0.9)
            self.particleArray[i].particle.setAcceleration(0, -9.81, 0)
            self.particleArray[i].particle.clearAccumulator()
            self.world.getParticles().append(self.particleArray[i].particle)
           
        #setup cable between particles (each two consecutive ones)
        for i in range(self.CABLE_COUNT):
            self.cables.append(BridgeDemo.CableGraphics())
            self.cables[i].cable.particles[0] = self.particleArray[i].particle
            self.cables[i].cable.particles[1] = self.particleArray[i+2].particle
            self.cables[i].cable.maxLength = 1.9
            self.cables[i].cable.restitution =0 
            self.world.getContactGenerators().append(self.cables[i].cable)

        for i in range(self.SUPPORT_COUNT):
            self.supports.append(BridgeDemo.CableConstrainGraphics())
            self.supports[i].support.particle = self.particleArray[i].particle
            self.supports[i].support.anchor = Vector(i/2*2.2-5.5,6,(i%2)*1.6-0.8)
            if i<6: self.supports[i].support.maxLength = i/4 + 3.0
            else: self.supports[i].support.maxLength = i/4
            self.supports[i].support.restitution = 0
            self.world.getContactGenerators().append(self.supports[i].support)

        #setup rods between particles (floor of bridge)
        for i in range(self.ROD_COUNT):
            self.rods.append(BridgeDemo.RodGraphics())
            self.rods[i].rod.particles[0] = self.particleArray[i*2].particle
            self.rods[i].rod.particles[1] = self.particleArray[i*2+1].particle
            self.rods[i].rod.length = 2
            self.world.getContactGenerators().append(self.rods[i].rod)

           
        #Update particle mass to take into account the mass on the platform
        self.updateAdditionalMass()

    def update(self):
        '''
            Method called to update simulation on time step
        '''

        #Clear accumulators
        self.world.startFrame()

        #Run the simulation
        self.world.runPhysics(1/self.FREQ)

        #update mass of platform
        self.updateAdditionalMass()

    def updateAdditionalMass(self):
        '''
            Method called to calculate the center of mass of the platform
            according to position of the extra mass
        '''

        for i in range(self.PARTICLE_COUNT):
            self.particleArray[i].particle.setMass(self.BASE_MASS)

        x = int(self.massPosition.x)
        xp = self.massPosition.x%1

        if x<0:
            x=0
            xp=0 
        if x>=5:
            x=5
            xp=0

        z = int(self.massPosition.z)
        zp = self.massPosition.z%1

        if z<0:
            z= 0
            zp= 0 
        if z>=1:
            z=1
            zp=0

        self.massDisplayPosition.clear()

        self.particleArray[x*2+z].particle.setMass(self.BASE_MASS + self.EXTRA_MASS*(1-xp)*(1-zp))
        self.massDisplayPosition.addScaledVector(self.particleArray[x*2+z].particle.getPosition(), (1-xp)*(1-zp))

        if xp > 0:
            self.particleArray[x*2+z+2].particle.setMass(self.BASE_MASS + self.EXTRA_MASS*xp*(1-zp));
            self.massDisplayPosition.addScaledVector(self.particleArray[x*2+z+2].particle.getPosition(), xp*(1-zp))
            if zp > 0:
                self.particleArray[x*2+z+3].particle.setMass(self.BASE_MASS + self.EXTRA_MASS*xp*zp);
                self.massDisplayPosition.addScaledVector(self.particleArray[x*2+z+3].particle.getPosition(), xp*zp)
        if zp > 0:
            self.particleArray[x*2+z+1].particle.setMass(self.BASE_MASS + self.EXTRA_MASS*(1-xp)*zp);
            self.massDisplayPosition.addScaledVector(self.particleArray[x*2+z+1].particle.getPosition(), (1-xp)*zp)


    def graphicsSetup(self):
        '''
            Called before simulation starts to set up scene
        '''

        scene.width = scene.height = 600
        L = 100
        scene.camera.pos = vec(-10,10,10)
        scene.camera.axis = vec(0,0,0) - scene.camera.pos
        scene.range = 0.1*L
        
        d = L-2
        R= L/400
        #xaxis = cylinder(pos=vec(0,0,0), axis=vec(0,0,d), radius=R, color=color.yellow)
        #yaxis = cylinder(pos=vec(0,0,0), axis=vec(d,0,0), radius=R, color=color.yellow)
        #zaxis = cylinder(pos=vec(0,0,0), axis=vec(0,d,0), radius=R, color=color.yellow)
        floor = box (pos=vector( 0, 0, 0), size=vector(200, 0.01, d),  color = color.red)


    def display(self):
        '''
            Called each time step to update simulation graphics
        '''

        for particle in self.particleArray:
            position = particle.particle.getPosition()
            particle.ball.pos = vec(position.x,position.y,position.z)
            particle.ball.visible = True

        for rod in self.rods:
            p0 = rod.rod.particles[0].getPosition()
            p1 = rod.rod.particles[1].getPosition()
            rod.shape.pos = vec(p0.x,p0.y,p0.z)
            rod.shape.axis =vec(p1.x-p0.x,p1.y-p0.y,p1.z-p0.z)

        for cable in self.cables:
            p0 = cable.cable.particles[0].getPosition()
            p1 = cable.cable.particles[1].getPosition()
            cable.shape.pos = vec(p0.x,p0.y,p0.z)
            cable.shape.axis =vec(p1.x-p0.x,p1.y-p0.y,p1.z-p0.z)

        for support in self.supports:
            p0 = support.support.particle.getPosition()
            p1 = support.support.anchor
            support.shape.pos = vec(p0.x,p0.y,p0.z)
            support.shape.axis =vec(p1.x-p0.x,p1.y-p0.y,p1.z-p0.z)
            
        self.massDisplayPositionBall.pos = vec(self.massDisplayPosition.x,self.massDisplayPosition.y,self.massDisplayPosition.z)

    def  keyInput(self,evt):
        '''
            maps keys to events
            ---------
            args:
                evt - vpython.event 
        '''

        if evt.key == 'w' or evt.key == 'W':
            self.massPosition.z += 0.1
            if self.massPosition.z > 1.0: self.massPosition.z = 1
        elif evt.key == 's' or evt.key == 'S':
            self.massPosition.z -= 0.1
            if self.massPosition.z < 0: self.massPosition.z = 0
        elif evt.key == 'a' or evt.key == 'A':
            self.massPosition.x -= 0.1
            if self.massPosition.x < 0: self.massPosition.x = 0
        elif evt.key == 'd' or evt.key == 'D':
            self.massPosition.x += 0.1
            if self.massPosition.x > 5: self.massPosition.x = 5

    def run(self):
        '''
            open loop of simulation
        '''

        self.graphicsSetup()
        while(True):
            rate(self.FREQ)
            self.update()
            self.display()


x = BridgeDemo()
scene.bind('keydown', x.keyInput)
x.run()



