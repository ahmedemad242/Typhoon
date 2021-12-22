from Typhoon.Pfgen import Pfgen

class ParticleSpring(Pfgen.ParticleForceGenerator):
	'''
        Class responsible for simulatung the spring force on particles
        ---------
        properties:
            k				- double   - Spring constant
			rl				- double   - Resting length of spring
			otherParticle	- Particle - The other paticle which the spring is attached to (not affected by spring)
        ---------
        methods:
            updateForce    -  How force is updated each time step
    '''

	def __init__(self, k, rl, otherParticle):
		'''
            Class constractor
        ---------
            args:
				k				- double   - Spring constant
				rl				- double   - Resting length of spring
				otherParticle	- Particle - The other paticle which the spring is attached to (not affected by spring)
        '''

		self.k = k
		self.rl = rl
		self.otherParticle = otherParticle

	def updateForce(self, particle, duration):
		'''
			Calculate force on a particle ina given duration
			---------
			args:
				particle	- Particle  
				duration	- double 
		'''
		 
		# Sping force = -k (|d| - rl) ud
		# |d| is the distance between the two particles
		# ud is a unit vector in direction of the particle on which the force is applied to the other particle

		force = particle.getPosition()
		force -= self.otherParticle.getPosition()
		
		magnitude = force.magnitude()
		magnitude = abs(self.rl-magnitude) * self.k
		force.normalize()
		force*= -magnitude

		particle.addForce(force)


