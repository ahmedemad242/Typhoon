from Typhoon.Pfgen import AnchordSpring

class ParticleAnchordBungee(AnchordSpring.ParticleAnchordSpring):
	'''
        Class responsible for simulatung the bungee force on particles from an anchor 
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

		super().__init__(anchor,k,rl)

	def updateForce(self, particle, duration):
		'''
			Calculate force on a particle ina given duration
			---------
			args:
				particle	- Particle  
				duration	- double 
		'''

		# Bungee force = -k (|d| - rl) Ud
		# |d| is the distance between the two particles
		# Ud is a unit vector in direction of the particle on which the force is applied to the other particle
		# Bungee rope only acts when it is extended
		force = particle.getPosition()
		force -= self.anchor
		magnitude = force.magnitude()
		if magnitude <= self.rl: return

		magnitude = (magnitude - self.rl) * self.k
		force.normalize()
		force*= -magnitude

		particle.addForce(force)


