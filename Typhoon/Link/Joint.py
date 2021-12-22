from Typhoon.Contact import *

class Joint(ContactGenerator):
    '''
        Class responsible for simulatung a joints between two rigid bodies

        ---------
        properties:
            body     - list   - two bodies to be linked
            position - list - Position of the joint in body coordinate for each body 
            error    - double - Max displacment betweeen the joint
        ---------
        methods:
            addContact - return length between two particles
    '''

    def __init__(self):
        '''
            Class constractor
        '''

        self.body = [None,None]
        self.position = [None, None]
        self.error = 0

    def set(self, a: "RigidBody", aPos: "Vector", b: "RigidBody", bPos: "Vector", error: "double"):
        '''
            Class setter
            ---------
            args:
                a     - RigidBody - first rigid body
                aPos  - Vector    - position of joint in a's space
                b     - RigidBody - second rigid body
                bPos  - Vector    - position of joint in b's space
                error - double    - Max displacment betweeen the joint
        '''

        self.body[0] = a
        self.body[1] = b

        self.position[0] = aPos
        self.position[1] = bPos

        self.error = error


    def addContact(self, contact : list, limit: int):
        '''
            Fills the given contact structure with the generated
            contact and return the number of contacts that have been written.
        ---------
            args:
                contact - list - contacts list 
                limit   - int  - maximum number of contacts in the array that can be written to
        '''

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

        return 0

