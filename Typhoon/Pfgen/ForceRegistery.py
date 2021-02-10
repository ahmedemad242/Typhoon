from Typhoon.Pfgen import Pfgen

#Registery which holds all forces and particle they act on
class ParticleForceRegistery:
	#register a force and a particle it applies to
	class ParticleForceRegisteration:
		def __init__(self, particle, fgen):
			self.particle = particle
			self.particleForceGenerator = fgen

	#List of all particle-force pairs
	def __init__(self):
		self.registerations = []

	#Register a force which is applied to a particle to the registery
	def add(self, particle, fgen):
		self.registerations.append(ParticleForceRegistery.ParticleForceRegisteration(particle, fgen))

	#Update all particles by forces acting on it
	def updateForces(self, duration):
		for registeration in self.registerations:
			registeration.particleForceGenerator.updateForce(registeration.particle,duration)
	
	#Remove all particle-force pair in the registery
	def clear(self):
		self.registerations.clear()

	#Remove a pair of certain force applying to a certain particle
	#nothing happens if the pair is not found
	def remove(self,particle,fgen):
		for registeration in self.registerations:
			if registeration.particleForceGenerator == fgen and registeration.particle == particle:
				self.registerations.remove(registeration)
				break

