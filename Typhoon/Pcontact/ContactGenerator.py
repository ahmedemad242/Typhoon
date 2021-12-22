from abc import ABC, abstractmethod

class ParticleContactGenerator(ABC):
    '''
        Abstract class which all the contact generators implements
        ---------
        Abstract methods:
            addContact - add contact and limit to contact object
    '''

    @abstractmethod
    def addContact(self, contact, limit):
        '''
            Abstract class method to Fills the given contact structure with the generated
            contact and return the number of contacts that have been written.
        ---------
            args:
                contact - ParticleContact - particle on which the force is applied
                limit   - int     - maximum number of contacts in the array that can be written to
        '''

        pass
