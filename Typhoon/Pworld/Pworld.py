from Typhoon.Pfgen import *
from Typhoon.Pcontact import *
from Typhoon.Core.Vector import Vector

class ParticleWorld:
    '''
        Keeps track of particles in system and updates them
        ---------
        properties:
            particleRegistry    - list   - All particle in world
            calculateIteration  - bool   - True if world needs to calculate iterations for contact resolver
            forceRegistery      - list   - All the forces in world
            contactResolver     - ParticleContactResolver - responsible for resolving contacts
            maxContacts         - int    - Max number of contacts allowed
            contacts            - list   - holds contact registers even if empty
            contactGenerators   - list   - holds contact generators

        ---------
        methods:
            runPhysics - run a frame of duration
            startFrame - clear all accumlators from previous frames
    '''

    def __init__(self, maxContacts, iterations=0):
        '''
            Class constractor
            ---------
            args:
                maxContacts  - int - Max number of contacts allowed 
                iterations   - int - Max number of contact resolver iterations
        '''

        self.particleRegistry = [] 
        self.calculateIteration = (iterations == 0)
        self.forceRegistery = ParticleForceRegistery()
        self.contactResolver = ParticleContactResolver(iterations)
        self.maxContacts = maxContacts
        self.contacts = []

        for i in range(self.maxContacts):
            self.contacts.append(ParticleContact())

        self.contactGenerators = []

    def startFrame(self):
        '''
            Clears accumulators to start a new frame
        '''

        for particle in self.particleRegistry:
            particle.clearAccumulator()

    def generateContacts(self):
        '''
            Add contacts due to contact generators
        '''

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

        return self.maxContacts - limit

    def integrate(self, duration):
        '''
            Run an integration on all particles for this time step
            ---------
            args:
                duration  - double - duration of time step 
        '''

        for particle in self.particleRegistry:
            particle.integrate(duration)

    def runPhysics(self,duration):
        '''
            run simulation with a time step of duration
            ---------
            args:
                duration  - double - duration of time step 
        '''

        #apply force generator
        self.forceRegistery.updateForces(duration)
        #integrate particles
        self.integrate(duration)
        #generate contacts
        usedContacts = self.generateContacts()
        #process contacts
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
    '''
        simulate the contacts with the ground
        ---------
        properties:
            particles - list - list of particles which will contact with the ground

        ---------
        methods:
            addContact - resolve contact for velocity and interpenetration
    '''

    def __init__(self, particles):
        '''
            class constractor
        '''

        self.particles = particles

    def addContact(self, contacts,limit,iterator):
        '''
            Fills the given contact structure with the generated
            contact and return the number of contacts that have been written.
        ---------
            args:
                contacts - list - particle on which the force is applied
                limit    - int  - maximum number of contacts in the array that can be written to
                iterator - int  - index to contact to access in the contacts array  
        '''

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