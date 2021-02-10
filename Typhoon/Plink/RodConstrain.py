from Typhoon.Plink import LinkConstrain

class ParticleRodConstrain(LinkConstrain.ParticleConstrain):
    def __init__(self):
        super().__init__()
        #max lenght of cable
        self.length = 0

    
    #return length between two particles
    def addContact(self, contact,limit):
        #Find the length of the rod
        currentLen = self.currentLength()

        #Check if we're over or under extended
        if (currentLen == self.length): return 0
        

        #Otherwise return the contact
        contact.particles[0] = self.particles[0]
        contact.particles[1] = None

        #Calculate the normal
        normal = anchor - self.particles[0].getPosition()
        normal.normalize()

        #The contact normal depends on whether we're extending or compressing
        if (currentLen > self.length):
            contact.contactNormal = normal
            contact.penetration = currentLen - self.length
        else:
            contact.contactNormal = normal * -1
            contact.penetration = self.length - currentLen
        

        #Always use zero restitution so no bounciness
        contact.restitution = 0

        return 1


    

