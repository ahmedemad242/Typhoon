from Typhoon.Pfgen import Pfgen

class ParticleForceRegistery:
	'''
        Registery which holds all forces and particle they act on
        ---------
        properties:
            registerations - List - all particle-force pairs
        ---------
        methods:
			add				-	Register a force which is applied to a particle to the registery 
			updateForces	-	Update all particles by forces acting on it
			clear			-	Clear registery
            remove			-	Remove a pair of certain force applying to a certain particle
    '''

	class ParticleForceRegisteration:
		'''
			register a force and a particle it applies to
			---------
			properties:
				particle - Particle
				fgen	 - particleForceGenerator
		'''

		def __init__(self, particle, fgen):
			'''
				Class constractor
				---------
				args:
					particle - Particle
					fgen	 - ParticleForceGenerator
			'''

			self.particle = particle
			self.particleForceGenerator = fgen

	def __init__(self):
		'''
			Class constractor
			---------
			args:
				registerations - List - all particle-force pairs
		'''
		self.registerations = []

	def add(self, particle, fgen):
		'''
			Register a force which is applied to a particle to the registery 
			---------
			args:
				particle - Particle  
				fgen	 - ParticleForceGenerator 
		'''

		self.registerations.append(ParticleForceRegistery.ParticleForceRegisteration(particle, fgen))

	def updateForces(self, duration):
		'''
			Update all particles by forces acting on it
			---------
			args:
				duration - double - duration of time step  
		'''

		for registeration in self.registerations:
			registeration.particleForceGenerator.updateForce(registeration.particle,duration)
	
	def clear(self):
		'''
			Clears registery
		'''

		self.registerations.clear()


	def remove(self,particle,fgen):
		'''
			Remove a pair of certain force applying to a certain particle
			nothing happens if the pair is not found
			if more than one exists, only first one registered is removed
			---------
			args:
				particle - Particle
				fgen	 - ParticleForceGenerator
		'''

		for registeration in self.registerations:
			if registeration.particleForceGenerator == fgen and registeration.particle == particle:
				self.registerations.remove(registeration)
				break

