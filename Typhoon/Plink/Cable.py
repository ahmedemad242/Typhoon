from Typhoon.Plink import Link


class ParticleCable(Link.ParticleLink):
    '''
        Class responsible for simulatung a cable between two particles
        ---------
        properties:
            particles   - list   - paticles to be linked
            maxLength   - double - max lenght of cable
            restitution - double - restitution of cable
        ---------
        methods:
            addContact - return length between two particles
    '''

    def __init__(self):
        '''
            Class constractor
        '''

        super().__init__()
        self.maxLength = 0
        self.restitution = 0


    def addContact(self, contact, limit):
        '''
            Fills the given contact structure with the generated
            contact and return the number of contacts that have been written.
        ---------
            args:
                contact - ParticleContact - particle on which the force is applied
                limit   - int     - maximum number of contacts in the array that can be written to
        '''
        
        length = self.currentLength()

        #Check if we're under-extended
        if length < self.maxLength:  return 0

        contact.particles[0] = self.particles[0]
        contact.particles[1] = self.particles[1]

        normal = self.particles[1].getPosition() - self.particles[0].getPosition()
        normal.normalize()
        contact.contactNormal = normal

        contact.penetration = length-self.maxLength
        contact.restitution = self.restitution

        return 1;


    

