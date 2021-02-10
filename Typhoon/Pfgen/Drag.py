from Typhoon.Pfgen import Pfgen

class ParticleDrag(Pfgen.ParticleForceGenerator):
	def __init__(self, k1, k2):
		#Drag constants
		self.k1 = k1
		self.k2 = k2

	def updateForce(self, particle, duration):
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


