from Typhoon.Pcontact import ContactGenerator


class ParticleLink(ContactGenerator.ParticleContactGenerator):
    '''
        Class responsible for simulatung a link between two particles
        link is simulated as a contact between two paticles 
        ---------
        properties:
            particles - list - paticles to be linked
        ---------
        methods:
            currentLength - return length between two particles
    '''

    def __init__(self):
        '''
            Class constractor
        '''

        self.particles = [None]*2

    def currentLength(self):
        '''
			return length between two particles
		'''

        relativePos = self.particles[0].getPosition() - self.particles[1].getPosition()
        return relativePos.magnitude()

    
