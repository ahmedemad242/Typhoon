from Typhoon.Core.Vector import Vector
from sys import float_info

class Particle:

    #constructor of particle
    def __init__(self):
        #position of the particle
        self.position =  Vector(0,0,0)

        #velocity of the particle
        self.velocity = Vector(0,0,0)

        #acceleration of the particle
        self.acceleration = Vector(0,0,0)

        #damping is applied to the velocity of the paticle
        #it is used to me the paricle lose energy
        #damping = 0 -> object stops, damping = 1 -> velocity doesnt change
        self.damping = 1

        #We store the inverse mass not mass because it's more logical
        #inverse mass = 0 -> infinte mass whichis dealt to immovable objects
        #inverse mass = infinity -> object is super fast (which is not useful in games)
        self.inverseMass = 0

        #Stores accumlated forces on the particle for the next iteration only
        #the value is zeroed in each intergration step
        self.forceAccum = Vector(0,0,0)

    def integrate(self, duration):
        assert(duration > 0);

        #update position by velocity 
        # Pn = Pn-1 + v*t
        self.position.addScaledVector(self.velocity, duration);

        #Calculate acceleration from force
        resultAcceleration = Vector(self.acceleration.x,self.acceleration.y,self.acceleration.z)
        resultAcceleration.addScaledVector(self.forceAccum, self.inverseMass);

        #update velocity using acceleration
        self.velocity.addScaledVector(resultAcceleration, duration);

        #Calculate drag
        self.velocity *= self.damping ** duration

        #clear all forces
        self.clearAccumulator();

    def setMass(self, mass):
        assert(mass != 0)
        self.inverseMass = 1/ mass

    def getMass(self):
        if self.inverseMass == 0:
            return float_info.max
        else:
            return 1 / self.inverseMass

    def setInverseMass(self, inverseMass):
        self.inverseMass = inverseMass

    def getInverseMass(self):
        return self.inverseMass

    def hasFiniteMass(self):
        if self.inverseMass >= 0:
            return True
        return False

    def setDamping(self,damping):
        self.damping = damping

    def getDamping(self):
        return self.damping

    def setPosition(self, x, y, z):
        self.position.x = x
        self.position.y = y
        self.position.z = z

    def getPosition(self):
        return Vector(self.position.x,self.position.y,self.position.z)

    def setVelocity(self, x, y, z):
        self.velocity.x = x
        self.velocity.y = y
        self.velocity.z = z

    def getVelocity(self):
        return Vector(self.velocity.x,self.velocity.y,self.velocity.z)

    def setAcceleration(self, x,  y,  z):
        self.acceleration.x = x
        self.acceleration.y = y
        self.acceleration.z = z

    def getAcceleration(self):
        return Vector(self.acceleration.x,self.acceleration.y,self.acceleration.z)

    def clearAccumulator(self):
        self.forceAccum.clear()

    def addForce(self, force):
        self.forceAccum += force

    def __str__(self):
        return "position: " + str(self.position) + "\n" \
               "velocity: " + str(self.velocity) + "\n" \
               "acceleration: " + str(self.acceleration) + "\n" \
               "force: " + str(self.forceAccum) + "\n" \
               "damping: " + str(self.damping) + "\n" \
               "mass: " + str(self.getMass()) + "n"
