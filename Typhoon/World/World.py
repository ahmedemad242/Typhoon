from Typhoon.Fgen import *
from Typhoon.Core import *
from Typhoon.Contact import *

class World:
    '''
        Keeps track of particles in system and updates them
        ---------
        properties:
            bodyRegistry        - list   - All rigid bodies in world
            calculateIteration  - bool   - True if world needs to calculate iterations for contact resolver
            forceRegistery      - list   - All the forces in world
            contactResolver     - ParticleContactResolver - responsible for resolving contacts
            maxContacts         - int    - Max number of contacts allowed
            contactRegistry     - list   - holds contact registers 
            contactGenRegistry  - list   - holds contact generators

        ---------
        methods:
            runPhysics - run a frame of duration
            startFrame - clear all accumlators from previous frames
    '''

    def __init__(self, maxContact, iterations=0):
        '''
            Class constractor
            ---------
            args:
                maxContacts  - int - Max number of contacts allowed 
                iterations   - int - Max number of contact resolver iterations
        '''

        self.bodyRegistry = [] 
        self.contactGenRegistry = []
        self.contactRegistry = []
        self.maxContact = maxContact
        self.forceRegistry = ForceRegistry()
        self.calculateIteration = (iterations == 0)
        self.resolver = ContactResolver(iterations,iterations)


    def startFrame(self):
        '''
            Clears accumulators to start a new frame
        '''

        for body in self.bodyRegistry:
            body.clearAccumulators()
            body.calculateDerivedData()


    def integrate(self, duration):
        '''
            Run an integration on all particles for this time step
            ---------
            args:
                duration  - double - duration of time step 
        '''

        for body in self.bodyRegistry:
            body.integrate(duration)

    def runPhysics(self,duration):
        '''
            run simulation with a time step of duration
            ---------
            args:
                duration  - double - duration of time step 
        '''

        #apply force generator
        self.forceRegistery.updateForces(duration)

        #integrate bodies
        for reg in self.bodyRegistry:
            reg.integrate(duration)

        usedContacts = self.generateContacts()

        if self.calculateIteration: self.resolver.setIterations(usedContacts * 4, usedContacts * 4)
        resolver.resolveContacts(contacts, usedContacts, duration)


    def generateContacts(self):
        '''
            Add contacts due to contact generators
        '''

        limit = self.maxContact
        for reg in self.contactGenRegistry:
            used  = reg.addContact(self.contactRegistry, limit)
            limit -= used

            if limit <= 0: break

        return self.maxContact - limit
        

    def getBodyRegistry(self):
        return self.bodyRegistry

    def getForces(self):
        return self.forceRegistery