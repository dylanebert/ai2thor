from ai2thor.controller import Controller
import numpy as np
import pandas as pd
import random


controller = Controller(scene="FloorPlan10")


def get_random_pickupable():
    candidates = []
    for obj in controller.last_event.metadata['objects']:
        if obj['pickupable']:
            candidates.append(obj)
    return random.choice(candidates)


def update_to_current_frame(obj):
    name = obj['name']
    for candidate in controller.last_event.metadata['objects']:
        if candidate['name'] == name:
            return candidate


obj = get_random_pickupable()
controller.step(
    action='PickupObject',
    objectId=obj['objectId'],
    forceAction=True,
    manualInteract=False
)
controller.step('PausePhysicsAutoSim')
controller.step(action='DropHandObject')
controller.step('AdvancePhysicsStep', timestep=.01)

dir = np.random.rand(3)
dir /= np.linalg.norm(dir)
event = controller.step(
    action='TouchThenApplyForce',
    x=.5,
    y=.5,
    direction={
        'x': dir[0],
        'y': dir[1],
        'z': dir[2]
    },
    moveMagnitude=100,
    handDistance=1.5
)
print(event.metadata['actionReturn'])
obj = update_to_current_frame(obj)
print(obj['position'])
for i in range(100):
    controller.step(action='AdvancePhysicsStep', timestep=.05)
obj = update_to_current_frame(obj)
print(obj['position'])