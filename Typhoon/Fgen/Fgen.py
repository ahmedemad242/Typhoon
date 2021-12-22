from abc import ABC, abstractmethod

class ForceGenerator(ABC):
    '''
        Abstract class which all the force generators implements
        ---------
        Abstract methods:
            updateForce -   How force is updated each time step
    '''

    @abstractmethod
    def updateForce(self, body, duration):
        ''' 
            Abstract class method to be overriden by force generators
        ---------
            args:
                body     - Body   - body on which the force is applied
                duration - double - time step duration
        '''

        pass

