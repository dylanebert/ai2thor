from ai2thor.controller import Controller
import numpy as np
import pandas as pd
import random


controller = Controller(scene="FloorPlan10")
controller.step('PausePhysicsAutoSim')


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
print(obj['position'])

controller.step(
    action='PushObject',
    objectId=obj['objectId'],
    moveMagnitude='100',
    forceAction=True
)
for i in range(100):
    controller.step(
        action='AdvancePhysicsStep',
        timestep=.05
    )


obj = update_to_current_frame(obj)
print(obj['position'])