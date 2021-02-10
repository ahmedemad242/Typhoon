from Typhoon.Pfgen import Pfgen

class ParticleSpring(Pfgen.ParticleForceGenerator):
	def __init__(self, otherParticle, k, rl):
		#Sprinf constant
		self.k = k
		#resting length 
		self.rl = rl
		#other particle to which the spring is attached
		#this particle is not affected by the spring force
		self.otherParticle = otherParticle

	def updateForce(self, particle, duration):
		# Sping force = -k (|d| - rl) Ud
		# |d| is the distance between the two particles
		# Ud is a unit vector in direction of the particle on which the force is applied to the other particle
		
		force = particle.getPosition()
		force -= self.otherParticle.getPosition()
		
		magnitude = force.magnitude()
		magnitude = abs(self.rl-magnitude) * self.k
		force.normalize()
		force*= -magnitude

		particle.addForce(force)


