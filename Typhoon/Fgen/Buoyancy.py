from Typhoon.Fgen.Fgen import ForceGenerator
from Typhoon.Core import *    


class Buoyancy(ForceGenerator):
    
    def __init__(self, centerOfBouancy, maxDepth, volume, LiquidHeight,liquidDensity = 1000):
        #Depth at which max bouyancy force is applied
        self.maxDepth = maxDepth
        #Volume of the object submerged, it is modeled as a rectangle 
        self.volume = volume
        #The height of the water plane above y=0. The plane will be
        #parrallel to the XZ plane.
        self.LiquidHeight = LiquidHeight
        #denisty of the liquid, defult 1000KG/M3 for pure water
        self.liquidDensity =liquidDensity
        #Center of the rigid body in objects space
        self.centerOfBuoyancy = centerOfBouancy


    #Uses an explicit tensor matrix to update the force on
    #the given rigid body. This is exactly the same as for updateForce
    #only it takes an explicit tensor.
    def updateForce(self, body, duration):
        
        #Get center of bouancy in world space
        pointInWorld = body.getPointInWorldSpace(self.centerOfBuoyancy)
        depth = pointInWorld.y;

        #Check if we're out of the water
        if depth >= self.LiquidHeight + self.maxDepth: return;
        force = Vector()

        #Check if we're at maximum depth
        if (depth <= self.LiquidHeight - self.maxDepth):
            force.y = self.liquidDensity * self.volume
            body.addForceAtBodyPoint(force, self.centerOfBuoyancy)
            return

        #Otherwise we are partly submerged
        force.y = self.liquidDensity * self.volume * (depth - self.maxDepth - self.LiquidHeight) / 2 * self.maxDepth
        body.addForceAtBodyPoint(force, self.centerOfBuoyancy)
