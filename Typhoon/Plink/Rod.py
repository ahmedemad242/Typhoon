from Typhoon.Plink import Link


class ParticleRod(Link.ParticleLink):
    '''
        Class responsible for simulatung a rod between two particles
        ---------
        properties:
            particles   - list   - paticles to be linked
            length      - double - lenght of rod
        ---------
        methods:
            addContact - return length between two particles
    '''

    def __init__(self):
        '''
            Class constractor
        '''

        super().__init__()
        self.length = 0

    def addContact(self, contact,limit):
        '''
            Fills the given contact structure with the generated
            contact and return the number of contacts that have been written.
        ---------
            args:
                contact - ParticleContact - particle on which the force is applied
                limit   - int     - maximum number of contacts in the array that can be written to
        '''

        currentLen = self.currentLength()

        #Check if we're over or under extended
        if (currentLen == self.length): return 0
        
        contact.particles[0] = self.particles[0]
        contact.particles[1] = self.particles[1]

        normal = self.particles[1].getPosition() - self.particles[0].getPosition()
        normal.normalize()

        #The contact normal direction 
        if (currentLen > self.length):
            contact.contactNormal = normal
            contact.penetration = currentLen - self.length
        else:
            contact.contactNormal = normal * -1
            contact.penetration = self.length - currentLen
        

        #restitution is zero to avoid bounciness
        contact.restitution = 0

        return 1


    

