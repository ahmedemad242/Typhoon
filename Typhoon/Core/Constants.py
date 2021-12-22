from sys import float_info, maxsize
from math import pi
import sys

#Any value under which will be rendered zero
REAL_EPSILON = 10**-9

#Holds energy under which the object will be sleeping and wont react 
SLEEP_EPSILON = 0.3

PI = pi

#Max float in pyhton
MAX_FLOAT = float_info.max

#Max int value in python
MAX_INT = maxsize
