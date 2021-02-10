from Typhoon.Fgen.Fgen import ForceGenerator


class Aero(ForceGenerator):
    def __init__(self, tensor, postion, windSpeed):

        #Holds the aerodynamic tensor for the surface in body
        #space. 
        self.tensor = tensor

        #Holds the relative position of the aerodynamic surface in
        #body space.
        self.position = postion

        #Holds the speed of the wind in the world
        self.windSpeed = windSpeed

    #Uses an explicit tensor matrix to update the force on
    # the given rigid body.
    def updateForceFromTensor(self, body, duration, tensor):
        #Calculate total velocity (windspeed and body's velocity).
        velocity = body.getVelocity()
        velocity += self.windSpeed

        #Calculate the velocity in body coordinates
        bodyVel = body.getDirectionInLocalSpace(velocity)

        #Calculate the force in body coordinates
        bodyForce = tensor.transform(bodyVel)
        force = body.getDirectionInWorldSpace(bodyForce)

        #Apply the force
        body.addForceAtBodyPoint(force, self.position)


    def updateForce(self, body, duration):
        self.updateForceFromTensor(body,duration,self.tensor)




