from abc import ABC, abstractmethod

class ParticleContactGenerator(ABC):
    # Fills the given contact structure with the generated
    # contact. where limit is the  maximum number of contacts in 
    # the array that can be written to. The method returns
    #  the number of contacts that havebeen written.
    @abstractmethod
    def addContact(self, contact, limit):
        pass
