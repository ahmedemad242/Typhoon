#Keep track of particles in system and updates them
from Typhoon.Fgen import *
from Typhoon.Core import *
from Typhoon.Contact import *

class World:
    def __init__(self, maxContact, iterations=0):
        #holds bodies in world
        self.bodyRegistry = [] 

        #holds contacts generators in world
        self.contactGenRegistry = []

        #holds contacts in world
        self.contactRegistry = []

        #Maxiumum number of contacts allowed
        self.maxContact = maxContact

        #Contains all the forces in world
        self.forceRegistry = ForceRegistry()

        #True if world needs to calculate iterations for contact resolver
        self.calculateIteration = (iterations == 0)

        #Contact resolver object
        self.resolver = ContactResolver(iterations,iterations)


    def startFrame(self):
        for body in self.bodyRegistry:
            body.clearAccumulators()
            body.calculateDerivedData()


    def integrate(self, duration):
        for body in self.bodyRegistry:
            body.integrate(duration)

    def runPhysics(self,duration):
        #apply force generator
        self.forceRegistery.updateForces(duration)
        #integrate bodies
        for reg in self.bodyRegistry:
            reg.integrate(duration)

        usedContacts = self.generateContacts()

        if self.calculateIteration: self.resolver.setIterations(usedContacts * 4, usedContacts * 4)
        resolver.resolveContacts(contacts, usedContacts, duration)


    def generateContacts(self):
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