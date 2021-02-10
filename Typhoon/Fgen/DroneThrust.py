from Typhoon.Fgen.Fgen import ForceGenerator
from Typhoon.Core import *    
from vpython import *

class DroneThrust(ForceGenerator):
    
    def __init__(self, kf, w, actPoint):
        #Kf is a constant which depend on several things
        self.kf = kf
        #w or omega is the rotation of drone 
        self.w = w
        #point on which the force acts in local space
        self.actPoint = actPoint

    def updateForce(self, body, duration):
        force = body.getTransform().getAxisVector(1)
        #Force is given by the equation f=kf*w^2
        force *= self.kf * (self.w**2)
        body.addForceAtBodyPoint(force, self.actPoint)


