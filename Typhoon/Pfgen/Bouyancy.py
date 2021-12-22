from Typhoon.Pfgen import Pfgen
from Typhoon.Core import Vector

#generate a buoyancy force for a plane of liquid in XZ plane
class ParticleBouyancy(Pfgen.ParticleForceGenerator):
	'''
        Class responsible for simulatung the bouyancy force on particles
        ---------
        properties:
            maxDepth		- double - Depth at which max bouyancy force is applied
			volume			- double - Volume of the object submerged, it is modeled as a rectangle
			LiquidHeight	- double - The height of the water plane above y=0. The plane will be parallel to XZ
			liquidDensity	- double - denisty of the liquid, defult 1000KG/M3 for pure water
        ---------
        methods:
            updateForce    -  How force is updated each time step
    '''

	def __init__(self, maxDepth, volume, LiquidHeight, liquidDensity = 1000):
		'''
            Class constractor
        ---------
            args:
				maxDepth		- double - Depth at which max bouyancy force is applied
				volume			- double - Volume of the object submerged, it is modeled as a rectangle
				LiquidHeight	- double - The height of the water plane above y=0. The plane will be parallel to XZ
				liquidDensity	- double - denisty of the liquid, defult 1000KG/M3 for pure water

        '''
		self.maxDepth = maxDepth
		self.volume = volume
		self.LiquidHeight = LiquidHeight
		self.liquidDensity =liquidDensity

	def updateForce(self, particle, duration):
		'''
			Calculate force on a particle ina given duration
			---------
			args:
				particle	- Particle  
				duration	- double 
		'''

		# f = 0 incase out of water
		# f = denisty * volume incase fully submerged
		# f = denist * volume * d otherwise
		# d =  (depth - maxDepth - Height)/(2*maxDepth)
		
		depth = particle.getPosition().y

		if depth >= self.LiquidHeight + self.maxDepth: return 

		force = Vector.Vector(0,0,0)

		if depth <= self.LiquidHeight - self.maxDepth:
			force.y = self.liquidDensity * self.volume	
			particle.addForce(force)
			return

		force.y = self.liquidDensity * self.volume * (depth - self.maxDepth - self.LiquidHeight)/(2*self.maxDepth)
		particle.addForce(force)


