from ai2thor.controller import Controller
import numpy as np
import pandas as pd
import random


controller = Controller(scene="FloorPlan10")
#controller.step('PausePhysicsAutoSim')


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
print(obj['position'])
obj = update_to_current_frame(obj)
print(obj['position'])

query = controller.step(
    action='GetObjectInFrame',
    x=.5,
    y=.5,
    forceAction=False
)
if query:
    print(query.metadata['actionReturn'])


'''for i in range(100):
    controller.step(
        action='AdvancePhysicsStep',
        timestep=.05
    )'''