from ai2thor.controller import Controller
import pandas as pd
controller = Controller(scene="FloorPlan10")
controller.step('PausePhysicsAutoSim')
data = []
for obj in controller.last_event.metadata['objects']:
    if obj['pickupable']:
        name = obj['name']
        pos = obj['position']
        rot = obj['rotation']
        print(name, pos, rot)