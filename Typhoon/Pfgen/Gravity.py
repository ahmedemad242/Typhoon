from Typhoon.Pfgen import Pfgen

class ParticleGravity(Pfgen.ParticleForceGenerator):
    '''
        Class responsible for simulatung the spring force on particles
        ---------
        properties:
            gravity	- Vector - acceleration due to gravity
        ---------
        methods:
            updateForce -  How force is updated each time step
    '''
    
    def __init__(self, gravity):
        '''
            Class constractor
            ---------
            args:
            gravity - Vector 
        '''

        self.gravity = gravity

    def updateForce(self, particle, duration):
        '''
	        Calculate force on a particle ina given duration
	        ---------
	        args:
		        particle - Particle  
		        duration - double 
        '''

        #check for infinite masses (immovable)
        if not (particle.hasFiniteMass()): return
        #Add force to particle scaled by its mass
        particle.addForce(self.gravity * particle.getMass());


