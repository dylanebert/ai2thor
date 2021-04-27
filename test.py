from ai2thor.controller import Controller
import pandas as pd
import random


controller = Controller(scene="FloorPlan10")
controller.step('PausePhysicsAutoSim')


def get_random_pickupable():
    candidates = []
    for obj in controller.last_event.metadata['objects']:
        if obj['pickupable']:
            candidates.append(obj['objectId'])
    return random.choice(candidates)


obj = get_random_pickupable()
print(obj)