# Typhoon
3D physics engine capable of simulating particles, rigid bodies, and their interactions. Based on the book "Game Physics Engine Development" by ian millington

### Quickstart

Add Typhoon into your work directory

Import module and start working:

``` python
from Typhoon.Particle import Particle

FREQ = 1
particle = Particle()
particle.setPosition(0,0,0)
particle.setAcceleration(1,0,0)
particle.setMass(1)

particle.integrate(1/FREQ)
particle.integrate(1/FREQ)

print(particle)
```
```
$ python app.py
position: 1.0 0.0 0.0
velocity: 2.0 0.0 0.0
acceleration: 1 0 0
force: 0 0 0
damping: 1
mass: 1.0
```

## Typhoon structure
    .
    ├── Core
    │   ├── Vector          
    │   ├── Matrix3        
    │   ├── Matrix4        
    │   └── Quaternion    
    ├── Particle system
    │   ├── Force generators
    │   └── contacts    
    ├── Mass aggregate system
    │   └── Links    
    ├── Rigid body system
    │   ├── Force & toeque generators
    │   ├── contacts
    │   └── contact resolver    
    └── ...

## Demos (used vpython for rendering)
``` 
pip install vpython==7.6.1
```
The demos folder include several demos of what typhoon is capable of.

### ballistics

``` python
class BallisticsDemo:

    def __init__(self):
        self.particle = Particle()
        self.type = BallisticsDemo.ShotType.UNUSED
        self.startTime = None
        self.particle.setPosition(0,1,0)

    def update(self):
        while True:
            rate(FREQ)
            for shot in self.ammo:
                if shot.type != self.ShotType.UNUSED:
                    shot.render()
                    shot.particle.integrate(1/FREQ)
```

### Sailboat

This demo shows how to setup the rigid body simulation

``` python
class SailBoatDemo:
    def __init__(self):
        self.sailBoat = RigidBody()

        #Set body properties
        self.sailBoat.setPosition(0, 1.5, 0)
        self.sailBoat.setOrientation(1,0,0,0)
        self.sailBoat.setVelocity(0,0,0)
        self.sailBoat.setRotation(0,0,0)

        self.sailBoat.setMass(200.0)
        it = Matrix3()
        it.setBlockInertiaTensor(Vector(2,1,1), 100)
        self.sailBoat.setInertiaTensor(it)
        self.sailBoat.setDamping(0.8, 0.4)
        self.sailBoat.setAcceleration(0.3,-9.81,0)

        self.sailBoat.calculateDerivedData()

        self.sailBoat.setAwake()
        self.sailBoat.setCanSleep(False)

        #Forces acting in environment
        self.buoyancyForceFront = Buoyancy(self.sailBoat.boat.position+Vector(-0.51,0,0),0.6,2,1.6)
        self.buoyancyForceBack = Buoyancy(self.sailBoat.boat.position+Vector(0.5,0,0),0.6,2,1.6)
        self.windSpeed = Vector()
        self.aeroForce = Aero(Matrix3(0,0,0, 0,0,0, -1,0, -1), Vector(2, 0, 0), self.windSpeed)
        
        #Add forces to force registery
        self.forceRegistry = ForceRegistry()
        self.forceRegistry.add(self.sailBoat.boat, self.aeroForce)
        self.forceRegistry.add(self.sailBoat.boat, self.buoyancyForceBack)
        self.forceRegistry.add(self.sailBoat.boat, self.buoyancyForceFront)
```

and what is being updated every timestep

```python
def update(self,duration):
        #Clear accumlators so zero forces and torque
        self.sailBoat.boat.clearAccumulators();

        #Add forces to body.
        self.forceRegistry.updateForces(duration);

        #Update the boat's physics.
        self.sailBoat.boat.integrate(duration);

        #Change the wind speed.
        self.windSpeed = self.windSpeed * 0.9 + Vector(uniform(0,100), 0,uniform(0,100))


    def run(self):
        while(True):
            rate(self.FREQ)
            self.display()
            self.update(1/self.FREQ)
```
