from Typhoon.Plink import LinkConstrain


class ParticleCableConstrain(LinkConstrain.ParticleConstrain):
    '''
        Class responsible for simulatung a cable between a particle and an anchor
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

    
    def addContact(self, contact,limit):
        '''
            Fills the given contact structure with the generated
            contact and return the number of contacts that have been written.
        ---------
            args:
                contact - ParticleContact - particle on which the force is applied
                limit   - int     - maximum number of contacts in the array that can be written to
        '''

        length = self.currentLength();

        if length < self.maxLength:  return 0

        contact.particles[0] = self.particle
        contact.particles[1] = None

        normal = self.anchor - self.particle.getPosition()
        normal.normalize()
        contact.contactNormal = normal

        contact.penetration = length-self.maxLength
        contact.restitution = self.restitution

        return 1;


    

