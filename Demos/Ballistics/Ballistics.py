from sys import path
path.insert(0, '../../')    


from enum import Enum
from vpython import *
from datetime import datetime
from datetime import timedelta           
from Typhoon.Particle import Particle


class BallisticsDemo:

    class ShotType(Enum):
        UNUSED = 0
        PISTOL = 1
        ARTILLERY = 2
        FIREBALL = 3
        LASER = 4

    class AmmoRound:
        def __init__(self):
            self.particle = Particle()
            self.type = BallisticsDemo.ShotType.UNUSED
            self.startTime = None
            self.ball = sphere (color = color.green, radius = 4)
            self.ball.visible = False
            self.particle.setPosition(0,1,0)

        def render(self):
            position = self.particle.getPosition()
            self.ball.pos = vector(position.z,position.y,position.x)
   
    def __init__(self):
        self.ammoRounds = 16
        self.ammo = []
        self.currentShotType = self.ShotType.LASER 
        for x in range(self.ammoRounds):
            self.ammo.append(self.AmmoRound())

    def fire(self):
        #find first shot available
        currentShot = None
        counter = 0
        for shot in self.ammo:
            currentShot = shot
            counter += 1
            if shot.type == self.ShotType.UNUSED:
                break

        #couldnt find any available shots
        if counter >= self.ammoRounds:
            return

        #set properties of particle
        if self.currentShotType == self.ShotType.LASER:
            currentShot.particle.setMass(0.1)
            currentShot.particle.setVelocity(0,0,100)
            currentShot.particle.setAcceleration(0,0,0)
            currentShot.particle.setDamping(0.99)
        elif self.currentShotType == self.ShotType.PISTOL:
            currentShot.particle.setMass(1)
            currentShot.particle.setVelocity(0,0,35)
            currentShot.particle.setAcceleration(0,-1,0)
            currentShot.particle.setDamping(0.99)
        elif self.currentShotType == self.ShotType.ARTILLERY:
            currentShot.particle.setMass(200)
            currentShot.particle.setVelocity(0,30,40)
            currentShot.particle.setAcceleration(0,-20,0)
            currentShot.particle.setDamping(0.99)
        elif self.currentShotType == self.ShotType.FIREBALL:
            currentShot.particle.setMass(1)
            currentShot.particle.setVelocity(0,0,10)
            currentShot.particle.setAcceleration(0,0.6,0)
            currentShot.particle.setDamping(0.9)

        currentShot.startTime = datetime.now()
        shot.ball.visible = True
        currentShot.type = self.currentShotType
        currentShot.particle.clearAccumulator()

    def update(self):
        while True:
            rate(60)
            for shot in self.ammo:
                if shot.type != self.ShotType.UNUSED:
                    shot.render()
                    shot.particle.integrate(1/60)
                    if shot.particle.getPosition().y < 0 or shot.particle.getPosition().z > 500 or shot.startTime+timedelta(seconds=5) < datetime.now():
                        shot.ball.visible = False
                        shot.particle.setPosition(0,1,0)
                        shot.type = self.ShotType.UNUSED

            k = keysdown()
            if '1' in k: self.currentShotType = self.ShotType.FIREBALL
            elif '2' in k: self.currentShotType = self.ShotType.ARTILLERY
            elif '3' in k: self.currentShotType = self.ShotType.PISTOL
            elif '4' in k: self.currentShotType = self.ShotType.LASER


    def display(self):
        scene.width = scene.height = 600
        L = 50
        scene.center = vec(L,0,0)
        scene.range = 1.3*L
        d = L-2
        R= L/100
        xaxis = cylinder(pos=vec(0,0,0), axis=vec(0,0,d), radius=R, color=color.yellow)
        yaxis = cylinder(pos=vec(0,0,0), axis=vec(d,0,0), radius=R, color=color.yellow)
        zaxis = cylinder(pos=vec(0,0,0), axis=vec(0,d,0), radius=R, color=color.yellow)
        for i in range(20):
            cylinder(pos=vec(i*10,0,0), axis=vec(0,0,d), radius=0.2, color=color.yellow)
        floor = box (pos=vector( 100, -0.5, d/2), size=vector(200, 1, d),  color = color.red)
                

x = BallisticsDemo()
scene.bind('click', x.fire)
x.display()
x.update()