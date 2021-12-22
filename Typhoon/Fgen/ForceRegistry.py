class ForceRegistry:
	'''
        Registery which holds all forces and body they act on
        ---------
        properties:
            registerations - List - all particle-force pairs
        ---------
        methods:
			add				-	Register a force which is applied to a body to the registery 
			updateForces	-	Update all particles by forces acting on it
			clear			-	Clear registery
            remove			-	Remove a pair of certain force applying to a certain body
    '''

	class ForceRegisteration:
		'''
			register a force and a body it applies to
			---------
			properties:
				body - Body
				fgen - ForceGenerator
		'''

		def __init__(self, body, fgen):
			'''
				Class constractor
				---------
				args:
					body - Body
					fgen - ForceGenerator
			'''
			self.body = body
			self.ForceGenerator = fgen

	def __init__(self):
		'''
			Class constractor
			---------
			args:
				registerations - List - all particle-force pairs
		'''

		self.registerations = []

	def add(self, body, fgen):
		'''
			Register a force which is applied to a body to the registery 
			---------
			args:
				body - body  
				fgen - ForceGenerator 
		'''

		self.registerations.append(ForceRegistry.ForceRegisteration(body, fgen))

	def updateForces(self, duration):
		'''
			Update all bodies by forces acting on it
			---------
			args:
				duration - double - duration of time step  
		'''

		for registeration in self.registerations:
			registeration.ForceGenerator.updateForce(registeration.body,duration)
	
	def clear(self):
		'''
			Clears registery
		'''
		self.registerations.clear()

	def remove(self,body,fgen):
		'''
			Remove a pair of certain force applying to a certain body
			nothing happens if the pair is not found
			if more than one exists, only first one registered is removed
			---------
			args:
				body - body
				fgen - ForceGenerator
		'''

		for registeration in self.registerations:
			if registeration.ForceGenerator == fgen and registeration.body == body:
				self.registerations.remove(registeration)
				break

