from Typhoon.Pfgen import Pfgen

class ParticleAnchordSpring(Pfgen.ParticleForceGenerator):
	def __init__(self, anchor, k, rl):
		#Sprinf constant
		self.k = k
		#resting length 
		self.rl = rl
		#Anchor vector to from which the spring force is generated
		self.anchor = anchor

	def getAnchor(self):
		return self.anchor

	def updateForce(self, particle, duration):
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


