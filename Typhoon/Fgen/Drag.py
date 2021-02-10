from Typhoon.Fgen.Fgen import ForceGenerator
from Typhoon.Core import *    


class Drag(ForceGenerator):
    
    def __init__(self,  dragCoff, surfaceArea,liquidDenisty = 1.1644):
        #liquidDenisty is the denisty of the medium
        #Defult is the desnity of air at 30 C
        self.liquidDenisty = liquidDenisty
        #Surface area of the body, for a box
        #it will be the hight and width
        self.surfaceArea = surfaceArea
        #Drag coffecient
        self.dragCoff = dragCoff

    
    #Since we already store the velocity in world coordinate
    #We can apply drag into the three axis Dx, Dy, Dz
    #using Vx, Vy, Vz according to the eq.
    #Di = 0.5*dragCoff*liquidDenisty*surfaceArea*RelativeVelocity^2
    #We will assume that the speed of air is 0, so relative
    #velocity is the same as velocity
    def updateForce(self, body, duration):
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

