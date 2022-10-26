# ++============================================++
# || Programming for Engineers: Toucan Crossing ||
# ||-------------+------------+-----------------||
# || Jasper Day  |  S2265891  |  2022/10/20     ||
# ++============================================++

# Description:
# ============
# `Period` tracks the state of the traffic light as the simulation advances. 
# The `window` object contains a grid on which `SceneObjects` are located.
# 
# As the simulation advances, every object (the traffic light and the scene 
# objects) is updated. The `window` object mutates as these objects are updated.
# 
# All of the logic (for traffic light state changes and `SceneObject` updates) 
# is contained in the `update` implied functions for their respective members.

from blinkstick import blinkstick
import matplotlib as mpt
import numpy as np
from enum import Enum
import time


class Period(Enum):
    # Enum type allows state comparison of our traffic light variable.
    # `int` enum lets us augment state by addition operator +=
    I = 1
    II = 2
    III = 3
    # I, II, and III are for Mayfield Roads
    # IA, IIA, and IIIA are for Westfield Mains
    IA = 4
    IIA = 5
    IIIA = 6
    # Pedestrian Cycle
    IV = 7
    V = 8
    VI = 9
    VII = 10
    VIII = 11
    IX = 12
    # red / amber for westfield mains
    IXA = 13

class TrafficLightAssignments(dict, Enum):
    # Traffic Light assignments. 
    # Traffic lights can be set with the splat operator **
    MAYFIELD_ROADS_RED = {
        "index": 0,
        "name": "red"
    }
    MAYFIELD_ROADS_YELLOW = {
        "index": 1,
        "name": "yellow"
    }
    MAYFIELD_ROADS_GREEN = {
        "index": 2,
        "name": "green"
    }
    WESTFIELD_MAINS_RED = {
        "index": 5,
        "name": "red"
    }
    WESTFIELD_MAINS_YELLOW = {
        "index": 4,
        "name": "yellow"
    }
    WESTFIELD_MAINS_GREEN = {
        "index": 3,
        "name": "green"
    }
    PEDESTRIAN_LIGHT_GREEN = {
        "index": 6,
        "name": "green"
    }
    PEDESTRIAN_LIGHT_RED = {
        "index": 7,
        "name": "red"
    }

class Scene():
    def __init__(self, rows, columns):
        scene = np.zeros([rows, columns])
    time_since_car = 0
    time_since_ped = 0
    time_since_button = 0
    # time since period updated
    time_since_update = 0
    def simulation_step(self, traffic_light):  # advance simulation
        global TIME
        traffic_light.update(self)
        print(f"State: {traffic_light.state}, Time: {self.time_since_update}")
        # broadcast call for all objects to update themselves (position, state, etc)
        
        TIME += 1
        self.time_since_button += 1
        self.time_since_car += 1
        self.time_since_ped += 1
        self.time_since_update += 1
        time.sleep(0.5)

class BlinkstickAPI():
    # interface to easily change traffic lights
    def __init__(self):
        self.bstick = blinkstick.find_first()
        if self.bstick == None: 
            raise Exception("No blinkstick found")
    
    def clear_colors(self):
        for i in range(0,8):
            self.bstick.set_color(index=i, name="black")
    
    def set_light(self, color_dict):
        self.bstick.set_color(**color_dict)
    

class TrafficLight():
    def __init__(self, state: Period):
        self.state = state
        self.blinkstick = BlinkstickAPI()

    def update(self, window: Scene):
        # Clear traffic light
        self.blinkstick.clear_colors()

        if self.state == Period.I:
            # Vehicle Running (Mayfield Roads)
            self.blinkstick.set_light(TrafficLightAssignments.MAYFIELD_ROADS_GREEN)
            self.blinkstick.set_light(TrafficLightAssignments.WESTFIELD_MAINS_RED)
            self.blinkstick.set_light(TrafficLightAssignments.PEDESTRIAN_LIGHT_RED)
            
            if (window.time_since_car >= 6 and 
                window.time_since_update >= 10 and 
                window.time_since_update >= window.time_since_button):
                # Gap condition with pedestrian demand
                self.state = Period.II
                window.time_since_update = 0

            elif window.time_since_update >= 20:
                # Max vehicle running duration
                self.state = Period.II
                window.time_since_update = 0
        
        elif self.state == Period.II:
            # Amber to Vehicles (Mayfield Roads)
            self.blinkstick.set_light(TrafficLightAssignments.MAYFIELD_ROADS_YELLOW)
            self.blinkstick.set_light(TrafficLightAssignments.WESTFIELD_MAINS_RED)
            self.blinkstick.set_light(TrafficLightAssignments.PEDESTRIAN_LIGHT_RED)
            
            if window.time_since_update >= 3:
                self.state = Period.III
                window.time_since_update = 0

        elif self.state == Period.III:
            # Vehicle Clearance
            self.blinkstick.set_light(TrafficLightAssignments.MAYFIELD_ROADS_RED)
            self.blinkstick.set_light(TrafficLightAssignments.WESTFIELD_MAINS_RED)
            self.blinkstick.set_light(TrafficLightAssignments.PEDESTRIAN_LIGHT_RED)

            if window.time_since_car >= 6 and window.time_since_update >= 1:
                # Gap condition
                self.state = Period.IXA
                window.time_since_update = 0
            
            elif window.time_since_update >= 3:
                self.state = Period.IXA
                window.time_since_update = 0

        if self.state == Period.IXA:
            # Amber / Yellow (Westfield Mains)
            self.blinkstick.set_light(TrafficLightAssignments.MAYFIELD_ROADS_RED)
            self.blinkstick.set_light(TrafficLightAssignments.WESTFIELD_MAINS_RED)
            self.blinkstick.set_light(TrafficLightAssignments.WESTFIELD_MAINS_YELLOW)
            self.blinkstick.set_light(TrafficLightAssignments.PEDESTRIAN_LIGHT_RED)

            if window.time_since_update >= 2:
                self.state = Period.IA
                window.time_since_update = 0
            

        if self.state == Period.IA:
            # Vehicle Running (Westfield Mains)
            self.blinkstick.set_light(TrafficLightAssignments.MAYFIELD_ROADS_RED)
            self.blinkstick.set_light(TrafficLightAssignments.WESTFIELD_MAINS_GREEN)
            self.blinkstick.set_light(TrafficLightAssignments.PEDESTRIAN_LIGHT_RED)
            
            if (window.time_since_car >= 6 and 
                window.time_since_update >= 10 and 
                window.time_since_update <= window.time_since_button):
                # Gap condition with pedestrian demand
                self.state = Period.IIA
                window.time_since_update = 0

            elif window.time_since_update >= 20:
                # Max vehicle running duration
                self.state = Period.IIA
                window.time_since_update = 0
        
        elif self.state == Period.IIA:
            # Amber to Vehicles (Westfield Mains)
            self.blinkstick.set_light(TrafficLightAssignments.MAYFIELD_ROADS_RED)
            self.blinkstick.set_light(TrafficLightAssignments.WESTFIELD_MAINS_YELLOW)
            self.blinkstick.set_light(TrafficLightAssignments.PEDESTRIAN_LIGHT_RED)
            
            if window.time_since_update >= 3:
                self.state = Period.IIIA
                window.time_since_update = 0

        elif self.state == Period.IIIA:
            # Vehicle Clearance
            self.blinkstick.set_light(TrafficLightAssignments.MAYFIELD_ROADS_RED)
            self.blinkstick.set_light(TrafficLightAssignments.WESTFIELD_MAINS_RED)
            self.blinkstick.set_light(TrafficLightAssignments.PEDESTRIAN_LIGHT_RED)
            
            if window.time_since_car >= 6 and window.time_since_update >= 1:
                # Gap condition
                self.state = Period.IV
                window.time_since_update = 0
            
            elif window.time_since_update >= 3:
                self.state = Period.IV
                window.time_since_update = 0

        elif self.state == Period.IV:
            # Pedestrian Crossing
            self.blinkstick.set_light(TrafficLightAssignments.MAYFIELD_ROADS_RED)
            self.blinkstick.set_light(TrafficLightAssignments.WESTFIELD_MAINS_RED)
            self.blinkstick.set_light(TrafficLightAssignments.PEDESTRIAN_LIGHT_GREEN)
            
            if window.time_since_update >= 6:
                # Appropriate time for 10+ m road
                self.state = Period.V
                window.time_since_update = 0
        
        elif self.state == Period.V:
            # Fixed black-out
            self.blinkstick.set_light(TrafficLightAssignments.MAYFIELD_ROADS_RED)
            self.blinkstick.set_light(TrafficLightAssignments.WESTFIELD_MAINS_RED)
            
            if window.time_since_update >= 3:
                self.state = Period.VI
                window.time_since_update = 0
        
        elif self.state == Period.VI:
            # Pedestrian Clearance
            self.blinkstick.set_light(TrafficLightAssignments.MAYFIELD_ROADS_RED)
            self.blinkstick.set_light(TrafficLightAssignments.WESTFIELD_MAINS_RED)
            if window.time_since_ped >= 2 or window.time_since_update >= 22:
                # Pedestrians extend clearance by 2s
                self.state = Period.VII
                window.time_since_update = 0

        elif self.state == Period.VII:
            # Additional Pedestrian Clearance
            self.blinkstick.set_light(TrafficLightAssignments.MAYFIELD_ROADS_RED)
            self.blinkstick.set_light(TrafficLightAssignments.WESTFIELD_MAINS_RED)
                    
            if window.time_since_ped >= 2 or window.time_since_update >= 3:
                self.state = Period.VIII
                window.time_since_update = 0


        elif self.state == Period.VIII:
            # All-Red for 2s
            self.blinkstick.set_light(TrafficLightAssignments.MAYFIELD_ROADS_RED)
            self.blinkstick.set_light(TrafficLightAssignments.WESTFIELD_MAINS_RED)
            self.blinkstick.set_light(TrafficLightAssignments.PEDESTRIAN_LIGHT_RED)
            
            if window.time_since_update >= 2:
                self.state = Period.IX
                window.time_since_update = 0

        elif self.state == Period.IX:
            # Red/Amber Period
            self.blinkstick.set_light(TrafficLightAssignments.MAYFIELD_ROADS_RED)
            self.blinkstick.set_light(TrafficLightAssignments.MAYFIELD_ROADS_YELLOW)
            self.blinkstick.set_light(TrafficLightAssignments.WESTFIELD_MAINS_RED)
            self.blinkstick.set_light(TrafficLightAssignments.PEDESTRIAN_LIGHT_RED)

            if window.time_since_update >= 2:
                self.state = Period.I
                window.time_since_update = 0

class SceneObject():
    def __init__(self, window:Scene, row_start:int, row_end:int, col_start:int, col_end:int, letter):
        
        # Check if bounds are valid
        if not (row_start <= row_end < window.scene.shape[0] and col_start <= col_end < window.scene.shape[1]):
            raise Exception("Incorrect bounds for object") 
        
        self.row_start = row_start
        self.row_end = row_end
        self.col_start = col_start
        self.col_end = col_end
        self.letter = letter

    def contains(self, scene_object):
        return (self.row_start <= scene_object.row_start and 
                self.row_end >= scene_object.row_end and 
                self.col_start <= scene_object.col_start and 
                self.col_end >= scene_object.col_end)
    
    def centroid(self) -> (int, int):
        return (np.floor((row_start + row_end)/2), np.floor((col_start + col_end)/2))

class Sidewalk(SceneObject):
    pass

class Road(SceneObject):
    pass

class MobileObject(SceneObject):
    def __init__(self,x:int,y:int,speed,destination: SceneObject, letter):
        super().init(row_start=x,row_end=x,col_start=y,col_end=y, letter=letter)
        self.destination = destination
        self.speed = speed
        self.dest_coords = destination.centroid()
    
    def update_coords(self,new_x,new_y):
        self.row_start = new_x
        self.row_end = new_y
        self.col_start = new_y
        self.col_end = new_y
    
    def time_step(self) -> (int, int):
        pass    




class Car(MobileObject): # Contents of Address Register. just kidding.
    def __init__(self, x, y, destination: SceneObject):
        super().init(x=x, y=y, destination=destination, letter='C')

class Pedestrian(MobileObject): # Contents of Address Register. just kidding.
    def __init__(self, x, y, destination: SceneObject):
        super().init(x=x, y=y, destination=destination, letter='P')


# Size of the crosswalk simulation matrix. One square is 1 meter on a side.
ROWS = 70
COLUMNS = 30
TIME = 0 # seconds

window = Scene(rows=ROWS, columns=COLUMNS)

traffic_light = TrafficLight(Period.I)

while True:
    window.simulation_step(traffic_light)
