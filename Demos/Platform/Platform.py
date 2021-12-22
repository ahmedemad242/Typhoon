from sys import path
path.insert(0, '../../')    

from vpython import *
from Typhoon import *

class PlatformDemo:
    '''
        Class which renders a simulation of a mass moving on a platform, this demo demonstrates
        the links (rods) , force generators, and contact resolution of Typhoon
        ---------
        properties:
            world                   - ParticleWorld  - used to keep track of particles inside simulation 
            particleArray           - list           - list of all particles in simulation   
            rods                    - list           - list of all links in simulation
            massPosition            - Vector         - Extra mass real position
            massDisplayPosition     - Vector         - Extra mass display position
            massDisplayPositionBall - vpython.sphere - used for graphics purposes
        ---------
        we use two vectors for extra mass position to delay calculation of platform slope
    '''

    PARTICLE_COUNT = 6  # number of nodes of the platform
    ROD_COUNT = 15      # number of connections between nodes

    BASE_MASS = 1       # mass of each node
    EXTRA_MASS = 10     # mass of ball

    FREQ = 25           # frequency of simulation

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
        self.rods = []
        self.massPosition = Vector(0,0,0.5)
        self.massDisplayPosition = Vector()
        self.massDisplayPositionBall = sphere (color = color.black, radius = 0.25)

        #setup patricles and their properties
        for i in range(self.PARTICLE_COUNT):
            self.particleArray.append(PlatformDemo.ParticleGraphics())
            self.particleArray[i].particle.setMass(self.BASE_MASS)
            self.particleArray[i].particle.setDamping(0.9)
            self.particleArray[i].particle.setAcceleration(0, -9.81, 0)
            self.particleArray[i].particle.clearAccumulator()
            self.world.getParticles().append(self.particleArray[i].particle)
            
        self.particleArray[0].particle.setInverseMass(0.0001)
        self.particleArray[1].particle.setInverseMass(0.0001)

        self.particleArray[0].particle.setPosition(0,0,1)
        self.particleArray[1].particle.setPosition(0,0,-1)
        self.particleArray[2].particle.setPosition(-3,2,1)
        self.particleArray[3].particle.setPosition(-3,2,-1)
        self.particleArray[4].particle.setPosition(4,2,1)
        self.particleArray[5].particle.setPosition(4,2,-1)

        #setup connection between particles
        for i in range(self.ROD_COUNT):
            self.rods.append(PlatformDemo.RodGraphics())

        self.rods[0].rod.particles[0] = self.particleArray[0].particle
        self.rods[0].rod.particles[1] = self.particleArray[1].particle
        self.rods[0].rod.length = 2
        self.rods[1].rod.particles[0] = self.particleArray[2].particle
        self.rods[1].rod.particles[1] = self.particleArray[3].particle
        self.rods[1].rod.length = 2
        self.rods[2].rod.particles[0] = self.particleArray[4].particle
        self.rods[2].rod.particles[1] = self.particleArray[5].particle
        self.rods[2].rod.length = 2

        self.rods[3].rod.particles[0] = self.particleArray[2].particle
        self.rods[3].rod.particles[1] = self.particleArray[4].particle
        self.rods[3].rod.length = 7
        self.rods[4].rod.particles[0] = self.particleArray[3].particle
        self.rods[4].rod.particles[1] = self.particleArray[5].particle
        self.rods[4].rod.length = 7

        self.rods[5].rod.particles[0] = self.particleArray[0].particle
        self.rods[5].rod.particles[1] = self.particleArray[2].particle
        self.rods[5].rod.length = 3.605551275
        self.rods[6].rod.particles[0] = self.particleArray[1].particle
        self.rods[6].rod.particles[1] = self.particleArray[3].particle
        self.rods[6].rod.length = 3.605551275

        self.rods[7].rod.particles[0] = self.particleArray[0].particle
        self.rods[7].rod.particles[1] = self.particleArray[4].particle
        self.rods[7].rod.length = 4.472135955
        self.rods[8].rod.particles[0] = self.particleArray[1].particle
        self.rods[8].rod.particles[1] = self.particleArray[5].particle
        self.rods[8].rod.length = 4.472135955
        
        self.rods[9].rod.particles[0] = self.particleArray[0].particle
        self.rods[9].rod.particles[1] = self.particleArray[3].particle
        self.rods[9].rod.length = 4.123105626
        self.rods[10].rod.particles[0] = self.particleArray[2].particle
        self.rods[10].rod.particles[1] = self.particleArray[5].particle
        self.rods[10].rod.length = 7.280109889
        self.rods[11].rod.particles[0] = self.particleArray[4].particle
        self.rods[11].rod.particles[1] = self.particleArray[1].particle
        self.rods[11].rod.length = 4.898979486
        self.rods[12].rod.particles[0] = self.particleArray[1].particle
        self.rods[12].rod.particles[1] = self.particleArray[2].particle
        self.rods[12].rod.length = 4.123105626
        self.rods[13].rod.particles[0] = self.particleArray[3].particle
        self.rods[13].rod.particles[1] = self.particleArray[4].particle
        self.rods[13].rod.length = 7.280109889
        self.rods[14].rod.particles[0] = self.particleArray[5].particle
        self.rods[14].rod.particles[1] = self.particleArray[0].particle
        self.rods[14].rod.length = 4.898979486

        for rod in self.rods:
            self.world.getContactGenerators().append(rod.rod)

        self.groundContactGenerator = GroundContacts(self.world.getParticles())
        self.world.getContactGenerators().append(self.groundContactGenerator)

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

        for i in range(2,6):
            self.particleArray[i].particle.setMass(self.BASE_MASS)

        #coordinate of center of mass of platform
        xp = self.massPosition.x
        if xp<0:xp=0
        if xp>1:xp=1

        zp = self.massPosition.z
        if zp<0:zp=0
        if zp>1:zp=1

        self.massDisplayPosition.clear()

        self.particleArray[2].particle.setMass(self.BASE_MASS + self.EXTRA_MASS*(1-xp)*(1-zp));
        self.massDisplayPosition.addScaledVector(self.particleArray[2].particle.getPosition(), (1-xp)*(1-zp))

        if xp > 0:
            self.particleArray[4].particle.setMass(self.BASE_MASS + self.EXTRA_MASS*xp*(1-zp));
            self.massDisplayPosition.addScaledVector(self.particleArray[4].particle.getPosition(), xp*(1-zp))
            if zp > 0:
                self.particleArray[5].particle.setMass(self.BASE_MASS + self.EXTRA_MASS*xp*zp);
                self.massDisplayPosition.addScaledVector(self.particleArray[5].particle.getPosition(), xp*zp)
        if zp > 0:
            self.particleArray[3].particle.setMass(self.BASE_MASS + self.EXTRA_MASS*(1-xp)*zp);
            self.massDisplayPosition.addScaledVector(self.particleArray[3].particle.getPosition(), (1-xp)*zp)

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
            
        self.massDisplayPositionBall.pos = vec(self.massDisplayPosition.x,self.massDisplayPosition.y,self.massDisplayPosition.z)

    def  keyInput(self,evt):
        '''
            maps keys to events
            ---------
            args:
                evt - vpython.event 
        '''

        if evt.key == 'w' or evt.key == 'W':
            self.massPosition.z += 0.05
            if self.massPosition.z > 1.0: self.massPosition.z = 1.0
        elif evt.key == 's' or evt.key == 'S':
            self.massPosition.z -= 0.05
            if self.massPosition.z < 0: self.massPosition.z = 0
        elif evt.key == 'a' or evt.key == 'A':
            self.massPosition.x -= 0.05
            if self.massPosition.x < 0: self.massPosition.x = 0.0
        elif evt.key == 'd' or evt.key == 'D':
            self.massPosition.x += 0.05
            if self.massPosition.x > 1: self.massPosition.x = 1

    def run(self):
        '''
            open loop of simulation
        '''

        self.graphicsSetup()
        while(True):
            rate(self.FREQ)
            self.update()
            self.display()


x = PlatformDemo()
scene.bind('keydown', x.keyInput)
x.run()


