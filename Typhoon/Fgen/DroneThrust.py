from Typhoon.Fgen.Fgen import ForceGenerator
from Typhoon.Core import *    
from vpython import *

class DroneThrust(ForceGenerator):
    '''
        Class responsible for simulatung the thrust force on a drone
        ---------
        properties:
            kf		 - double - Kf is constant of the drone which takes many factors
			w	     - double - omega is the rotation of drone 
			actPoint - Vector - point on which the force acts in local space
        ---------
        methods:
            updateForce - How force is updated each time step
    ''' 

    def __init__(self, kf, w, actPoint):
        '''
            Class constractor
            ---------
            args:
                kf		 - double - Kf is constant of the drone which takes many factors
			    w	     - double - omega is the rotation of drone 
			    actPoint - Vector - point on which the force acts in local space
        '''

        self.kf = kf
        self.w = w
        self.actPoint = actPoint

    def updateForce(self, body, duration):
        '''
			Calculate force on a body ina given duration
			---------
			args:
				body	 - Body  
				duration - double 
		'''

        #Force is given by the equation f=kf*w^2

        force = body.getTransform().getAxisVector(1)
        force *= self.kf * (self.w**2)
        body.addForceAtBodyPoint(force, self.actPoint)


