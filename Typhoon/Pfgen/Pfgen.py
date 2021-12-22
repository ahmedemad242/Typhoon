from abc import ABC, abstractmethod
from Typhoon.Core import Vector
from Typhoon import Particle

class ParticleForceGenerator(ABC):
    '''
    Abstract class which all the force generators implements
    ---------
    Abstract methods:
        updateForce -   How force is updated each time step
    '''

    @abstractmethod
    def updateForce(self, particle, duration):
        '''
            Abstract class method to be overriden by force generators
        ---------
            args:
                particle - Particle - particle on which the force is applied
                duration - double - time step duration
        '''

        pass
