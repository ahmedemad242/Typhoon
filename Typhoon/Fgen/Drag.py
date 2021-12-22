from Typhoon.Fgen.Fgen import ForceGenerator
from Typhoon.Core import *    


class Drag(ForceGenerator):
    '''
        Class responsible for simulatung the Drag force on rigid bodies
        ---------
        properties:
			dragCoff      - double - Volume of the object submerged, it is modeled as a rectangle
			surfaceArea	  - double - Surface area of the body, for a box it will be the hight and width
			liquidDensity - double - liquidDenisty is the denisty of the medium, Defult is the desnity of air at 30 C = 1.1644
        ---------
        methods:
            updateForce - How force is updated each time step
    '''
    
    def __init__(self,  dragCoff, surfaceArea,liquidDenisty = 1.1644):
        '''
            Class constractor
            ---------
            args:
                dragCoff      - double - Volume of the object submerged, it is modeled as a rectangle
			    surfaceArea	  - double - Surface area of the body, for a box it will be the hight and width
			    liquidDensity - double - liquidDenisty is the denisty of the medium, Defult is the desnity of air at 30 C = 1.1644

        '''

        self.dragCoff = dragCoff
        self.surfaceArea = surfaceArea
        self.liquidDenisty = liquidDenisty

    
   
    def updateForce(self, body, duration):
        '''
			Calculate force on a body ina given duration
			---------
			args:
				body	 - Body  
				duration - double 
		'''

        
        #since we already store the velocity in world coordinate
        #we can apply drag into the three axis dx, dy, dz
        #using vx, vy, vz according to the eq.
        #di = 0.5*dragcoff*liquiddenisty*surfacearea*relativevelocity^2
        #we will assume that the speed of air is 0, so relative
        #velocity is the same as velocity
        

        vel = body.getVelocity()
        drag = Vector()
        drag.x = 0.5 * (vel.x**2) * self.surfaceArea * self.dragCoff * self.liquidDenisty
        drag.y = 0.5 * (vel.y**2) * self.surfaceArea * self.dragCoff * self.liquidDenisty
        drag.z = 0.5 * (vel.z**2) * self.surfaceArea * self.dragCoff * self.liquidDenisty
        
        vel.normalize()
        drag.x = -vel.x*drag.x
        drag.y = -vel.y*drag.y
        drag.z = -vel.z*drag.z

        body.addForce(drag)

