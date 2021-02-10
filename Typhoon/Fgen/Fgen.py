from abc import ABC, abstractmethod

class ForceGenerator(ABC):
	#Calculate and update force to a given particle 
	@abstractmethod
	def updateForce(self, body, duration):
		pass

