from Typhoon import Particle
from Typhoon.Core.Vector import Vector

class ParticleContact:
    '''
        Class responsible for representing a contact between two particles
        ---------
        properties:
            particles           - list   - two particles involved in contact
            restitution         - double - Restitution cofficient of collision
            contactNormal       - Vector - direction of contact
            penetration         - double - depth of contact
            particleMovement    - list   - two vectors representing Amount of movement for particles in resolution

        ---------
        methods:
            resolve - resolve contact for velocity and interpenetration
    '''

    def __init__(self):
        '''
            Class constractor
        '''
        self.particles = [None]*2
        self.restitution = 0
        self.contactNormal = Vector(0,0,0)
        self.penetration = 0
        self.particleMovement = [Vector(0,0,0),Vector(0,0,0)]

    def resolve(self,duration):
        '''
            resolve contact for velocity and interpenetration
        '''
        self.resolveVelocity(duration)
        self.resolveInterpenetration(duration)

    def calculateSeparatingVelocity(self):
        '''
            return seperating velocity at contact point
        '''
        relativeVelocity = self.particles[0].getVelocity()
        if self.particles[1]: relativeVelocity-=self.particles[1].getVelocity()
        return relativeVelocity.scalarProduct(self.contactNormal)

    def resolveVelocity(self, duration):
        '''
            impulse calculations for contact using law of conservasion of momentum
            ---------
            args:
                duration - double - duration of time step 
        '''

        #Calculate separating velocity due to collision
        separatingVelocity = self.calculateSeparatingVelocity()

        if separatingVelocity>0:return

        newSeparatingVelocity = -separatingVelocity*self.restitution

        #Calculate velocity due to acceleration only
        accCausedVelocity = self.particles[0].getAcceleration()
        if self.particles[1]: accCausedVelocity-=self.particles[1].getAcceleration()
        accCausedSeparatingVelocity = accCausedVelocity.scalarProduct(self.contactNormal)*duration

        #Remove acceleration caused velocity from seprating velocity
        if accCausedSeparatingVelocity < 0:
            newSeparatingVelocity += self.restitution*accCausedSeparatingVelocity
            if newSeparatingVelocity<0: newSeparatingVelocity=0

        deltaVelocity = newSeparatingVelocity - separatingVelocity

        totalInverseMass = self.particles[0].getInverseMass()
        if self.particles[1]: totalInverseMass+=self.particles[1].getInverseMass()

        if totalInverseMass<=0: return

        #Find impulse per inverse mass
        impulse = deltaVelocity/totalInverseMass
        impulsePerIMass = self.contactNormal*impulse
        
        #Apply impulse to velocity
        vel = self.particles[0].getVelocity()+impulsePerIMass*self.particles[0].getInverseMass()
        self.particles[0].setVelocity(vel.x,vel.y,vel.z)
        if self.particles[1]: 
            vel = self.particles[1].getVelocity()+impulsePerIMass*-self.particles[1].getInverseMass()
            self.particles[1].setVelocity(vel.x,vel.y,vel.z)

    def resolveInterpenetration(self,duration):
        '''
            interpenetration calculation for contact
            ---------
            args:
                duration - double - duration of time step 

        '''

        if self.penetration <=0: return
        
        totalInverseMass = self.particles[0].getInverseMass()
        if self.particles[1]: totalInverseMass+=self.particles[1].getInverseMass()

        #infinite mass check
        if totalInverseMass<=0: return

        #amount of penetration resolution per inverse mass
        movePerIMass = self.contactNormal * (self.penetration/totalInverseMass)

        #Calculate movment
        self.particleMovement[0] = movePerIMass * self.particles[0].getInverseMass();
        if self.particles[1]:
            self.particleMovement[1] = movePerIMass * - self.particles[1].getInverseMass();
        else:
            self.particleMovement[1].clear();
       
        #Apply movement
        pos0 =self.particles[0].getPosition()+self.particleMovement[0]
        self.particles[0].setPosition(pos0.x,pos0.y,pos0.z)
        if self.particles[1]:
            pos1 =self.particles[1].getPosition()+self.particleMovement[1]
            self.particles[1].setPosition(pos1.x,pos1.y,pos1.z)