from Typhoon.Pfgen import Pfgen
from Typhoon.Core import Vector

#generate a buoyancy force for a plane of liquid in XZ plane
class ParticleBouyancy(Pfgen.ParticleForceGenerator):
	def __init__(self, maxDepth, volume, LiquidHeight,liquidDensity = 1000):
		#Depth at which max bouyancy force is applied
		self.maxDepth = maxDepth
		#Volume of the object submerged, it is modeled as a rectangle 
		self.volume = volume
		#The height of the water plane above y=0. The plane will be
        #parrallel to the XZ plane.
		self.LiquidHeight = LiquidHeight
		#denisty of the liquid, defult 1000KG/M3 for pure water
		self.liquidDensity =liquidDensity

	def updateForce(self, particle, duration):
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


