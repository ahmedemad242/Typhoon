from sys import path
path.insert(0, '../../')    

from enum import Enum
from vpython import *
from datetime import datetime
from datetime import timedelta           
from Typhoon.Particle import Particle
from Typhoon.Core.Vector import Vector
from random import uniform

class Firework(Particle):
    '''
        Child to particle since Firework are particles moving randomly
        ---------
        properties:
            Patricle properties
            type  - FireworkRule   - type of firework
            age   - double         - Time in seconds before the firework die
            ball  - vpython.shpere - used for rendering purposes
    '''

    def __init__(self):
        '''
            Class constractor
        '''

        super().__init__()
        self.type = 0
        self.age = 0
        self.ball = sphere (color = color.green, radius = 2)
        self.ball.visible = False

    def update(self, duration):
        '''
            method used to update and render firework each time step
            ---------
            args:
                duration - double - duration of time step
        '''

        self.integrate(duration)
        self.age -= duration
        pos = self.getPosition()
        self.ball.pos = vector(pos.y,pos.z,pos.x)
        return self.age < 0 or self.position.z < 0

class FireworkRule():
    '''
        controls time of the fireworks and its sub fireworks
        ---------
        properties:
            type         - FireworkRule - type of firework
            minAge       - double       - Min time the firework will be in simulation
            maxAge       - double       - Max time the firework will be in simulation
            minVelocity  - double       - Min velocity of firework
            maxVelocity  - double       - Max velocity of firework
            damping      - double       - Damping applied on firework
            payloadCount - int          - number of sub fireworks
            payloads     - list         - list of sub fireworks
    '''

    class PayLoad():
        '''
            Child to particle since Firework are particles moving randomly
            ---------
            properties:
                Patricle properties
                type  - FireworkRule   - type of firework
                age   - double         - Time in seconds before the firework die
                ball  - vpython.shpere - used for rendering purposes
        '''

        def __init__(self, type, count):
            '''
                Class constractor
                ---------
                args:
                    type  - FireworkRule   - type of firework
                    count - int            - number of payload of this type of firework
            '''

            self.type = type
            self.count = count

    def __init__(self, type, minAge, maxAge, minVelocity, maxVelocity, damping, payloadCount):
        '''
            Class constractor
            ---------
            args:
                type         - FireworkRule - type of firework
                minAge       - double       - Min time the firework will be in simulation
                maxAge       - double       - Max time the firework will be in simulation
                minVelocity  - double       - Min velocity of firework
                maxVelocity  - double       - Max velocity of firework
                damping      - double       - Damping applied on firework
                payloadCount - int          - number of sub fireworks
        '''

        self.type = type
        self.minAge = minAge
        self.maxAge = maxAge
        self.minVelocity = minVelocity
        self.maxVelocity = maxVelocity
        self.damping = damping
        self.payloadCount = payloadCount
        self.payloads = []

    def __del__(self):
        '''
            deletes firework and its children
        '''

        del self.payloads   

    def create(self, firework, parent = None):
        '''
            create a firework and optionally apply a parent to it
            ---------
            args:
                firework - Firework        - Firework to be filled 
                parent   - Firework = None - Parent of firework if it is a child (payload)
        '''

        firework.type = self.type
        firework.age = uniform(self.minAge, self.maxAge);
        velocity = Vector(0,0,0)
        firework.ball.visible = True

        if(parent):
            pos = parent.getPosition()
            firework.setPosition(pos.x,pos.y,pos.z)
            velocity += parent.getVelocity()
        else:
            randposx = uniform(0,50)
            randposy = uniform(0,100)
            firework.setPosition(randposx,randposy,0)
            
        randx = uniform(self.minVelocity.x,self.maxVelocity.x)
        randy = uniform(self.minVelocity.y,self.maxVelocity.y)
        randz = uniform(self.minVelocity.z,self.maxVelocity.z)

        velocity += Vector(randx,randy,randz)
        firework.setVelocity(velocity.x,velocity.y,velocity.z)
        firework.setMass(1);
        firework.setDamping(self.damping);
        firework.setAcceleration(0,0,-20); #Acceleration due to gravity
        firework.clearAccumulator();

class FireWorkDemo:
    '''
        Class which renders a simulation of different types of fireworks being fired in a 3D space
        This demo is supposed to show Typhoon's particle system
        ---------
        properties:
            fireworks    - list - All fireworks in simulation
            nextFirework - int  - Holds number of fireworks in use
            rules        - list - All available rules for fireworks
    '''

    MAXFIREWORKS = 1024
    RULECOUNT = 5

    def __init__(self):
        '''
            Class constractor
        '''

        self.fireworks = []
        self.nextFirework = 0
        self.rules = []

        for i in range(FireWorkDemo.MAXFIREWORKS):
           firework = Firework()
           self.fireworks.append(firework)
           
        self.initiateFireworkRule()

    def initiateFireworkRule(self):
        '''
            Method which stores all rules for simulation
        '''

        rule = FireworkRule(1,0.5,2.1,Vector(-5,-5,25),Vector(5,5,28),0.8,2)
        rule.payloads.append(FireworkRule.PayLoad(3,5))
        rule.payloads.append(FireworkRule.PayLoad(5,1))
        self.rules.append(rule)

        rule = FireworkRule(2,0.5,1,Vector(-5,-5,20),Vector(5,5,30),0.1,1)
        rule.payloads.append(FireworkRule.PayLoad(4,7))
        self.rules.append(rule)

        rule = FireworkRule(3,0.5,3,Vector(-20,10,40),Vector(5,20,80),0.2,0)
        self.rules.append(rule)

        rule = FireworkRule(4,0.2,2.1,Vector(-20, 5, 50),Vector(20, 5, 95),0.2,0)
        self.rules.append(rule)

        rule = FireworkRule(5,0.2,1.7,Vector(-20, 5, 5),Vector(20, 5, 30),0.2,2)
        rule.payloads.append(FireworkRule.PayLoad(2,2))
        rule.payloads.append(FireworkRule.PayLoad(3,3))
        self.rules.append(rule)

    def create(self, type, parent, number = 1):
        '''
            Create a new firework 
            ---------
            args:
                type   - FireworkRule   - type of firework to be fired
                parent - Firework       - parent of the firework
                number - int = 1        - number of created firework
        '''

        for i in range(number):
            rule = self.rules[type-1]
            rule.create(self.fireworks[self.nextFirework],parent)
            self.nextFirework = (self.nextFirework +1) % FireWorkDemo.MAXFIREWORKS

    def update(self):
        '''
            open loop of simulation
        '''

        while True:
            rate(60)
            for firework in self.fireworks:
                if firework.type > 0:
                    if firework.update(1/60):
                        rule = self.rules[firework.type-1]
                        firework.type = 0
                        for i in range(rule.payloadCount):
                            payload = rule.payloads[i]
                            self.create(payload.type,firework,payload.count)
                        firework.ball.visible = False

    def display(self):
        '''
            Called before simulation starts to set up scene
        '''

        scene.width = scene.height = 600
        L = 50
        scene.center = vec(L,0,0)
        scene.range = 3*L
        d = L-2
        R= L/100
        xaxis = cylinder(pos=vec(0,0,0), axis=vec(0,0,d), radius=R, color=color.yellow)
        yaxis = cylinder(pos=vec(0,0,0), axis=vec(d,0,0), radius=R, color=color.yellow)
        zaxis = cylinder(pos=vec(0,0,0), axis=vec(0,d,0), radius=R, color=color.yellow)
        floor = box (pos=vector( 100, -0.5, d/2), size=vector(200, 1, d),  color = color.red)

    def  keyInput(self,evt):
        '''
            maps keys to events
            ---------
            args:
                evt - vpython.event 
        '''

        if evt.key == '1': self.create(1, None)
        elif evt.key == '2': self.create(2, None)
        elif evt.key == '3': self.create(3, None)
        elif evt.key == '4': self.create(4, None)
        elif evt.key == '5': self.create(5, None)


x = FireWorkDemo()
scene.bind('keydown', x.keyInput)
x.display()
x.update()


