from Typhoon import Particle
from Typhoon.Core import Vector
from Typhoon.Pcontact import ParticleContact
from sys import float_info

class ParticleContactResolver:
    def __init__(self,iterations):
        #max number of allowed iteration for contact resolver
        self.iterations = iterations

        self.usedIterations = 0

    def setIterations(self,iterations):
        self.iterations = iterations

    def resolveContacts(self, contactArray, duration):
        self.usedIterations = 0
        while self.usedIterations < self.iterations:
            max = float_info.max

            #Find contact with the most seprating velocity (most impact)
            currentContact = None
            for contact in contactArray:
                if contact.particles[0] == None: continue
                separatingVelocity = contact.calculateSeparatingVelocity()
                if separatingVelocity<max and (separatingVelocity<0 or contact.penetration >0):
                    currentContact = contact
                    max = separatingVelocity

            #Nothing to resolve
            if currentContact is None: return

            #resolve contact
            currentContact.resolve(duration)

            #update interposition for all particles
            move = currentContact.particleMovement

            for contact in contactArray:
                if contact.particles[0] == currentContact.particles[0]:
                    contact.penetration -=  contact.contactNormal.scalarProduct(move[0]) 
                elif contact.particles[0] == currentContact.particles[1]:
                    contact.penetration -= move[1].scalarProduct(contact.contactNormal) 
                if contact.particles[1]:
                    if contact.particles[1] == currentContact.particles[0]:
                        contact.penetration += move[0].scalarProduct(contact.contactNormal)
                    elif contact.particles[1] == currentContact.particles[1]:
                        contact.penetration += move[1].scalarProduct(contact.contactNormal)

            self.usedIterations+=1