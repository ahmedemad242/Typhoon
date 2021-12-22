from Typhoon.Core.Vector import Vector
from sys import float_info

class Particle:
    '''
        Class responsible for simulating particle behaviour
        ---------
        properties:
            position - Vector - represent location of particle in 3D space
            velocity - Vector - represent velocity of particle in 3 axes
            acceleration - Vector - represent acceleration of particle in 3 axes
            damping - double - represent damping applied to velocity of particle each time step
            inverseMass - double - store inverse mass of particle 
            forceAccum - vector - represent force applied to particle in the next time step only
        ---------
        methods:
            setters & getters
            integrate - Update the particle properties each time step
            hasFiniteMass - Return true if object is movable
            clearAccumulator - clears the force applied to the particle in this time step
            addForce - add force to the forceAccum in this time step
    '''

    def __init__(self):
        '''
            Class constractor
        '''

        self.position =  Vector(0,0,0)
        self.velocity = Vector(0,0,0)
        self.acceleration = Vector(0,0,0)
        #Daming is used to make the paricle lose energy
        #damping = 0 -> object stops, damping = 1 -> velocity doesnt change
        self.damping = 1
        #inverse mass = 0 -> infinte mass whichis dealt to immovable objects
        #inverse mass = infinity -> object is super fast (which is not useful in games)
        self.inverseMass = 0
        #the value of the forceAccum is zeroed in each intergration step
        self.forceAccum = Vector(0,0,0)

    def integrate(self, duration):
        '''
            method which updates the particle properties each time step
            ---------
            args:
                duration - double - duration of time step
        '''

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
        '''
            method which set mass particle properties each time step
            ---------
            args:
                mass - double - mass of the object, cannot be zero
        '''

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
        '''
            Returns a new vector which represents the location of the particle
        '''

        return Vector(self.position.x,self.position.y,self.position.z)

    def setVelocity(self, x, y, z):
        self.velocity.x = x
        self.velocity.y = y
        self.velocity.z = z

    def getVelocity(self):
        '''
            Returns a new vector which represents the velocity of the particle
        '''

        return Vector(self.velocity.x,self.velocity.y,self.velocity.z)

    def setAcceleration(self, x,  y,  z):
        self.acceleration.x = x
        self.acceleration.y = y
        self.acceleration.z = z

    def getAcceleration(self):
        '''
            Returns a new vector which represents the acceleration of the particle
        '''

        return Vector(self.acceleration.x,self.acceleration.y,self.acceleration.z)

    def clearAccumulator(self):
        '''
            Clears the accumulated force on the particle
        '''

        self.forceAccum.clear()

    def addForce(self, force):
        '''
            Add force to the accumulated force on the object
            ---------
            args:
                force - Vector - additional force applied to the particle
        '''

        self.forceAccum += force

    def __str__(self):
        return "position: " + str(self.position) + "\n" \
               "velocity: " + str(self.velocity) + "\n" \
               "acceleration: " + str(self.acceleration) + "\n" \
               "force: " + str(self.forceAccum) + "\n" \
               "damping: " + str(self.damping) + "\n" \
               "mass: " + str(self.getMass()) + "n"
