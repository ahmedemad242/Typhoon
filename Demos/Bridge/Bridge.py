from sys import path
path.insert(0, '../../')    

from vpython import *
from Typhoon import *

class PlatformDemo:
    ROD_COUNT = 6
    SUPPORT_COUNT = 12
    CABLE_COUNT = 10
    PARTICLE_COUNT = 12

    BASE_MASS = 1
    EXTRA_MASS = 20

    FREQ = 30

    class ParticleGraphics:
        def __init__(self):
            self.particle = Particle()
            self.ball = sphere (color = color.green, radius = 0.2)

    class CableGraphics:
        def __init__(self):
            self.cable = ParticleCable()
            self.shape = cylinder(radius = 0.1,color=color.cyan)

    class CableConstrainGraphics:
        def __init__(self):
            self.support = ParticleCableConstrain()
            self.shape = cylinder(radius = 0.1,color=color.orange)

    class RodGraphics:
        def __init__(self):
            self.rod = ParticleRod()
            self.shape = cylinder(radius = 0.1,color=color.blue)

    def __init__(self):
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
            self.particleArray.append(PlatformDemo.ParticleGraphics())
            self.particleArray[i].particle.setPosition(i-5,4,(i%2)*2-1)
            self.particleArray[i].particle.setMass(self.BASE_MASS)
            self.particleArray[i].particle.setDamping(0.9)
            self.particleArray[i].particle.setAcceleration(0, -9.81, 0)
            self.particleArray[i].particle.clearAccumulator()
            self.world.getParticles().append(self.particleArray[i].particle)
           
        #setup cable between particles (each two consecutive ones)
        for i in range(self.CABLE_COUNT):
            self.cables.append(PlatformDemo.CableGraphics())
            self.cables[i].cable.particles[0] = self.particleArray[i].particle
            self.cables[i].cable.particles[1] = self.particleArray[i+2].particle
            self.cables[i].cable.maxLength = 1.9
            self.cables[i].cable.restitution =0 
            self.world.getContactGenerators().append(self.cables[i].cable)

        for i in range(self.SUPPORT_COUNT):
            self.supports.append(PlatformDemo.CableConstrainGraphics())
            self.supports[i].support.particle = self.particleArray[i].particle
            self.supports[i].support.anchor = Vector(i/2*2.2-5.5,6,(i%2)*1.6-0.8)
            if i<6: self.supports[i].support.maxLength = i/4 + 3.0
            else: self.supports[i].support.maxLength = i/4
            self.supports[i].support.restitution = 0
            self.world.getContactGenerators().append(self.supports[i].support)

        #setup rods between particles (floor of bridge)
        for i in range(self.ROD_COUNT):
            self.rods.append(PlatformDemo.RodGraphics())
            self.rods[i].rod.particles[0] = self.particleArray[i*2].particle
            self.rods[i].rod.particles[1] = self.particleArray[i*2+1].particle
            self.rods[i].rod.length = 2
            self.world.getContactGenerators().append(self.rods[i].rod)

           
        #Update particle mass to take into account the mass on the platform
        self.updateAdditionalMass()

    def update(self):
        #Clear accumulators
        self.world.startFrame()

        #Run the simulation
        self.world.runPhysics(1/self.FREQ)

        #update mass of platform
        self.updateAdditionalMass()

    def updateAdditionalMass(self):
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
        self.graphicsSetup()
        while(True):
            rate(self.FREQ)
            self.update()
            self.display()


x = PlatformDemo()
scene.bind('keydown', x.keyInput)
x.run()



