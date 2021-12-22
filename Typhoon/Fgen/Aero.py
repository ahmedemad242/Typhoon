from Typhoon.Fgen.Fgen import ForceGenerator


class Aero(ForceGenerator):
    '''
        Class responsible for simulatung the aero force on rigid bodies
        ---------
        properties:
            tensor      - Matrix3 - Holds the aerodynamic tensor for the surface in body space
			position	- Vector  - Holds the relative position of the aerodynamic surface in body space
			windSpeed	- Vector  - Holds the speed of the wind in the world
        ---------
        methods:
            updateForceFromTensor - Uses an explicit tensor matrix to update the force on the given rigid body
            updateForce           - How force is updated each time step
    '''

    def __init__(self, tensor, postion, windSpeed):
        '''
            Class constractor
        ---------
            args:
                tensor      - Matrix3 - Holds the aerodynamic tensor for the surface in body space
			    position	- Vector  - Holds the relative position of the aerodynamic surface in body space
			    windSpeed	- Vector  - Holds the speed of the wind in the world
        '''

        self.tensor = tensor
        self.position = postion
        self.windSpeed = windSpeed


    def updateForceFromTensor(self, body, duration, tensor):
        '''
			Uses an explicit tensor matrix to update the force on the given rigid body
			---------
			args:
				body	 - Body  
				duration - double 
                tensor   - Matrix3
		'''
        
        velocity = body.getVelocity()
        velocity += self.windSpeed

        #Calculate the velocity in body coordinates
        bodyVel = body.getDirectionInLocalSpace(velocity)
        print('velocity', bodyVel)

        #Calculate the force in body coordinates
        bodyForce = tensor.transform(bodyVel)
        print('bodyForce', bodyForce)
        force = body.getDirectionInWorldSpace(bodyForce)

        
        body.addForceAtBodyPoint(force, self.position)


    def updateForce(self, body, duration):
        '''
			Calculate force on a particle in a given duration
			---------
			args:
				body	 - Body  
				duration - double 
		'''

        self.updateForceFromTensor(body, duration, self.tensor)




