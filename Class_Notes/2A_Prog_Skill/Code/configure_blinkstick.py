"""This program sets the student name and matriculation number on a blinkstick

It was written by David Ingram from The University of Edinburgh in 2020
and is released unde creative commons by attribution licence.

It uses three variables:
NAME is the name of the student
MATRIC is the matriculation number of the student
bstick is the object used to talk to the blinkstick.
"""
from blinkstick import blinkstick

# set student name and Matric number
NAME = "Jasper Day"
MATRIC = "s2265891"

# find the first available blinkstick
bstick = blinkstick.find_first()

# Check we have found a blinkstick and if not print an error
if bstick is None:
    print("The Blinkstick is not connected, either plug it in " \
    +" or check your USB cable supports data and power!")
else:
    # a blinkstick has been found so we can continue to save 
    # data in the info blocks.
    bstick.set_info_block1(NAME)
    bstick.set_info_block2(MATRIC)

    # now check it worked
    print("Blinkstick #"+bstick.get_serial() \
          +" is issued to "+ bstick.get_info_block1() \
          +" ("+bstick.get_info_block2()+")")
