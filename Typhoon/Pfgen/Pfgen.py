from abc import ABC, abstractmethod
from Typhoon.Core import Vector
from Typhoon import Particle

class ParticleForceGenerator(ABC):
	#Calculate and update force to a given particle 
	@abstractmethod
	def updateForce(self, particle, duration):
		pass
