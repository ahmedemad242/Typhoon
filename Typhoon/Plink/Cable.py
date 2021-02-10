from Typhoon.Plink import Link


class ParticleCable(Link.ParticleLink):
    def __init__(self):
        super().__init__()
        #max lenght of cable
        self.maxLength = 0
        #restitution of cable
        self.restitution = 0

    
    #return length between two particles
    def addContact(self, contact,limit):
        #Find the length of the cable
        length = self.currentLength()

        #Check if we're under-extended
        if length < self.maxLength:  return 0

        #Otherwise return the contact
        contact.particles[0] = self.particles[0]
        contact.particles[1] = self.particles[1]

        #Calculate the normal
        normal = self.particles[1].getPosition() - self.particles[0].getPosition()
        normal.normalize()
        contact.contactNormal = normal

        contact.penetration = length-self.maxLength
        contact.restitution = self.restitution

        return 1;


    

