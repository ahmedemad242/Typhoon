from Typhoon.Pcontact import ContactGenerator


class ParticleConstrain(ContactGenerator.ParticleContactGenerator):
    '''
        Class responsible for simulatung a link between a particle and an anchor
        link is simulated as a contact between the two 
        ---------
        properties:
            particle - Particle - paticle to be linked
            anchor   - Vector   - location of anchor
        ---------
        methods:
            currentLength - return length between two particles
    '''

    def __init__(self):
        '''
            Class constractor
        '''

        self.particle = None
        self.anchor = None

   
    def currentLength(self):
        '''
			return length between two particles
		'''

        relativePos = self.particle.getPosition() - self.anchor
        return relativePos.magnitude()

