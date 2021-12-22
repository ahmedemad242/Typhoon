from Typhoon.Pfgen import Pfgen

class ParticleAnchordSpring(Pfgen.ParticleForceGenerator):
	'''
        Class responsible for simulatung the spring force on particles from an anchor
        ---------
        properties:
            k		- double - Spring constant
			rl		- double - Resting length of spring
			anchor	- Vector - Anchor to which the spring is attached
        ---------
        methods:
            updateForce    -  How force is updated each time step
    '''

	def __init__(self, anchor, k, rl):
		'''
            Class constractor
        ---------
            args:
				k		- double   - Spring constant
				rl		- double   - Resting length of spring
				anchor	- Vector   - Anchor to which the spring is attached
        '''

		self.k = k
		self.rl = rl
		self.anchor = anchor

	def getAnchor(self):
		return self.anchor

	def updateForce(self, particle, duration):
		'''
			Calculate force on a particle ina given duration
			---------
			args:
				particle	- Particle  
				duration	- double 
		'''

		# Sping force = -k (|d| - rl) Ud
		# |d| is the distance between the two particles
		# Ud is a unit vector in direction of the particle on which the force is applied to the other particle
		
		force = particle.getPosition()
		force -= self.anchor
		magnitude = force.magnitude()
		if magnitude < self.rl: return

		magnitude = self.rl - magnitude * self.k
		force.normalize()
		force*= magnitude

		particle.addForce(force)


