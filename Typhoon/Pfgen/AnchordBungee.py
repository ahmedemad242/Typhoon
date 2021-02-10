from Typhoon.Pfgen import AnchordSpring

class ParticleAnchordBungee(AnchordSpring.ParticleAnchordSpring):
	def __init__(self, anchor, k, rl):
		super().__init__(anchor,k,rl)

	def updateForce(self, particle, duration):
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


