#Registery which holds all forces and particle they act on
class ForceRegistry:
	#register a force and a particle it applies to
	class ForceRegisteration:
		def __init__(self, body, fgen):
			self.body = body
			self.ForceGenerator = fgen

	#List of all particle-force pairs
	def __init__(self):
		self.registerations = []

	#Register a force which is applied to a particle to the registery
	def add(self, body, fgen):
		self.registerations.append(ForceRegistry.ForceRegisteration(body, fgen))

	#Update all particles by forces acting on it
	def updateForces(self, duration):
		for registeration in self.registerations:
			registeration.ForceGenerator.updateForce(registeration.body,duration)
	
	#Remove all particle-force pair in the registery
	def clear(self):
		self.registerations.clear()

	#Remove a pair of certain force applying to a certain particle
	#nothing happens if the pair is not found
	def remove(self,body,fgen):
		for registeration in self.registerations:
			if registeration.ForceGenerator == fgen and registeration.body == body:
				self.registerations.remove(registeration)
				break

