from Typhoon.Pfgen import Pfgen

class ParticleDrag(Pfgen.ParticleForceGenerator):
	'''
        Class responsible for simulatung the drag force on particles
        ---------
        properties:
            k1	- double - drag constants  
			k2	- double - drag constants  
        ---------
        methods:
            updateForce    -  How force is updated each time step
    '''

	def __init__(self, k1, k2):
		'''
            Class constractor
        ---------
            args:
				k1	- double - drag constants
				k2	- double - drag constants
        '''
		self.k1 = k1
		self.k2 = k2

	def updateForce(self, particle, duration):
		'''
			Calculate force on a particle ina given duration
			---------
			args:
				particle	- Particle  
				duration	- double 
		'''

		#drag force = -(k1 * |V| + k2 * |V|^2)Uv
		#k1, k2 drag coff
		# |V| magnitude of velocity
		# Uv unit vector in V direction
		force = particle.getVelocity()
		
		dragCoff = force.magnitude()
		dragCoff = self.k1 * dragCoff + self.k2 * dragCoff**2
		force.normalize()
		force*=-dragCoff

		particle.addForce(force)


