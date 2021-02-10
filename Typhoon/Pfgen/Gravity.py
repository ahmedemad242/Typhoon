from Typhoon.Pfgen import Pfgen

class ParticleGravity(Pfgen.ParticleForceGenerator):
	def __init__(self, gravity):
		#hold the acceleration due to gravity as a vector
		self.gravity = gravity

	def updateForce(self, particle, duration):
		#check for infinite masses (immovable)
		if not (particle.hasFiniteMass()): return
		#Add force to particle scaled by its mass
		particle.addForce(self.gravity * particle.getMass());


