from Typhoon.Pcontact import ContactGenerator


class ParticleLink(ContactGenerator.ParticleContactGenerator):
    def __init__(self):
        #hold particles connectected by the link
        self.particles = [None]*2

    #return length between two particles
    def currentLength(self):
        relativePos = self.particles[0].getPosition() - self.particles[1].getPosition()
        return relativePos.magnitude()

    
