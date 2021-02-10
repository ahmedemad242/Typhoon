from Typhoon.Pcontact import ContactGenerator


class ParticleConstrain(ContactGenerator.ParticleContactGenerator):
    def __init__(self):
        #hold particles connectected by the link
        self.particle = None
        self.anchor = None

    #return length between two particles
    def currentLength(self):
        relativePos = self.particle.getPosition() - self.anchor
        return relativePos.magnitude()

