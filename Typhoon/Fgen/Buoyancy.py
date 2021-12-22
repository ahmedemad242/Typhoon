from Typhoon.Fgen.Fgen import ForceGenerator
from Typhoon.Core import *    


class Buoyancy(ForceGenerator):
    '''
        Class responsible for simulatung the Buoyancy force on rigid bodies
        ---------
        properties:
            maxDepth		 - double - Depth at which max bouyancy force is applied
			volume			 - double - Volume of the object submerged, it is modeled as a rectangle
			LiquidHeight	 - double - The height of the water plane above y=0. The plane will be parallel to XZ
			liquidDensity	 - double - denisty of the liquid, defult 1000KG/M3 for pure water
            centerOfBuoyancy - Vector - Center of the rigid body in objects space
        ---------
        methods:
            updateForce - How force is updated each time step
    '''

    def __init__(self, centerOfBouancy, maxDepth, volume, LiquidHeight,liquidDensity = 1000):
        '''
            Class constractor
            ---------
            args:
                centerOfBuoyancy - Vector - Center of the rigid body in objects space
				maxDepth		- double - Depth at which max bouyancy force is applied
				volume			- double - Volume of the object submerged, it is modeled as a rectangle
				LiquidHeight	- double - The height of the water plane above y=0. The plane will be parallel to XZ
				liquidDensity	- double - denisty of the liquid, defult 1000KG/M3 for pure water
        '''

        self.maxDepth = maxDepth
        self.volume = volume
        self.LiquidHeight = LiquidHeight
        self.liquidDensity =liquidDensity
        self.centerOfBuoyancy = centerOfBouancy



    def updateForce(self, body, duration):
        '''
			Calculate force on a particle ina given duration
			---------
			args:
				body	- Body  
				duration	- double 
		'''

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

        #partly submerged
        force.y = self.liquidDensity * self.volume * (depth - self.maxDepth - self.LiquidHeight) / 2 * self.maxDepth
        body.addForceAtBodyPoint(force, self.centerOfBuoyancy)
