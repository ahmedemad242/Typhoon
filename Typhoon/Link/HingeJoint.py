from Typhoon.Contact import *


#Joints are used to put to bodies together,
#This is a common position joint which will
#Keep its location in body coordinates between
#two bodies
class HingeJoint(ContactGenerator):
    def __init__(self):
        self.body = [None,None]
        #Position of the joint in body coordinate
        self.position = [None, None]
        #Max displacment betweeen the joint
        #start to act
        self.error = 0
        #Normal to the plane where the joint can freely move in body space
        self.normal = Vector(-1,0,0)

    def set(self, a: "RigidBody", aPos: "Vector", b: "RigidBody", bPos: "Vector", error: float):
        self.body[0] = a
        self.body[1] = b

        self.position[0] = aPos
        self.position[1] = bPos

        self.error = error


    def addContact(self, contact : list, limit: int):
        a_pos_world = self.body[0].getPointInWorldSpace(self.position[0])
        b_pos_world = self.body[1].getPointInWorldSpace(self.position[1])

        a_to_b = b_pos_world - a_pos_world
        normal = a_to_b.copy()
        normal.normalize()
        length = a_to_b.magnitude()

        if abs(length) > self.error:
            contact.append(Contact())
            contact[-1].body[0] = self.body[0]
            contact[-1].body[1] = self.body[1]
            contact[-1].contactNormal = normal 
            contact[-1].contactPoint = (a_pos_world + b_pos_world) * 0.5
            contact[-1].penetration = length-self.error
            contact[-1].friction = 1
            contact[-1].restitution = 0
            return 1

        if self.outOfPlane():
            pass


        return 0

    def outOfPlane(self):
        transform = self.body[0].getDirectionInWorldSpace(self.normal)
        return transform == self.normal

    def outOfAngle(self):
        pass
