from Typhoon.Pfgen import Pfgen

class ParticleBungee(Pfgen.ParticleForceGenerator):
	def __init__(self, otherParticle, k, rl):
		#Sprinf constant
		self.k = k
		#resting length 
		self.rl = rl
		#other particle to which the bungee rope is attached
		#this particle is not affected by the spring force
		self.otherParticle = otherParticle

	def updateForce(self, particle, duration):
		# Bungee force = -k (|d| - rl) Ud
		# |d| is the distance between the two particles
		# Ud is a unit vector in direction of the particle on which the force is applied to the other particle
		# Bungee rope only acts when it is extended
		
		force = particle.getPosition()
		force -= self.otherParticle.getPosition()
		magnitude = force.magnitude()
		if magnitude <= self.rl: return

		magnitude = (self.rl - magnitude) * self.k
		force.normalize()
		force*= magnitude

		particle.addForce(force)


