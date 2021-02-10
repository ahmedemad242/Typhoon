
#Keep track of particles in system and updates them
from Typhoon.Pfgen import *
from Typhoon.Pcontact import *
from Typhoon.Core.Vector import Vector

class ParticleWorld:
    def __init__(self, maxContacts, iterations=0):
        #holds particles in world
        self.particleRegistry = [] 

        #True if world needs to calculate iterations for contact resolver
        self.calculateIteration = (iterations == 0)

        #Contains all the forces in world
        self.forceRegistery = ParticleForceRegistery()

        #Resolves contatcs (way to go on description)
        self.contactResolver = ParticleContactResolver(iterations)

        #Max number of contacts allowed
        self.maxContacts = maxContacts

        #contacts in world
        self.contacts = []

        for i in range(self.maxContacts):
            self.contacts.append(ParticleContact())

        self.contactGenerators = []

    def startFrame(self):
        for particle in self.particleRegistry:
            particle.clearAccumulator()

    def generateContacts(self):
        limit = self.maxContacts
        iterator = 0

        for contactGen in self.contactGenerators:
            if isinstance(contactGen, GroundContacts):
                used = contactGen.addContact(self.contacts,limit,iterator)
            else:
                used = contactGen.addContact(self.contacts[iterator],limit)

            limit -= used
            iterator += used

            if limit <= 0: break

        #return contacts used
        return self.maxContacts - limit

    def integrate(self, duration):
        for particle in self.particleRegistry:
            particle.integrate(duration)

    def runPhysics(self,duration):
        #apply force generator
        self.forceRegistery.updateForces(duration)
        #integrate particles
        self.integrate(duration)
        #generate contacts
        usedContacts = self.generateContacts()
        #process contacts
        #if usedContacts:
        if(self.calculateIteration): 
            self.contactResolver.setIterations(2*usedContacts)
        self.contactResolver.resolveContacts(self.contacts,duration)

    def getParticles(self):
        return self.particleRegistry

    def getContactGenerators(self):
        return self.contactGenerators

    def getForces(self):
        return self.forceRegistery



        
class GroundContacts():
    def __init__(self, particles):
        self.particles = particles

    def addContact(self, contacts,limit,iterator):
        count = 0
        for particle in self.particles:
            y = particle.getPosition().y
            if y < 0:
                contacts[iterator].contactNormal = Vector(0,1,0)
                contacts[iterator].particles[0] = particle
                contacts[iterator].particles[1] = None
                contacts[iterator].penetration = -y
                contacts[iterator].restitution = 0
                count+=1
                iterator+=1
                if (count >= limit): return count;
        return count