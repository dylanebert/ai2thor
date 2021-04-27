from ai2thor.controller import Controller
import numpy as np
import pandas as pd
import random


def get_random_pickupable(controller):
    candidates = []
    for obj in controller.last_event.metadata['objects']:
        if obj['pickupable']:
            candidates.append(obj)
    return random.choice(candidates)


def update_to_current_frame(controller, obj):
    name = obj['name']
    for candidate in controller.last_event.metadata['objects']:
        if candidate['name'] == name:
            return candidate


def apply_random_force(controller, obj):
    controller.step('UnpausePhysicsAutoSim')
    controller.step(
        action='PickupObject',
        objectId=obj['objectId'],
        forceAction=True,
        manualInteract=False
    )
    controller.step('PausePhysicsAutoSim')
    controller.step('DropHandObject')
    controller.step('AdvancePhysicsStep', timestep=.01)

    dir = np.random.rand(3)
    dir /= np.linalg.norm(dir)
    force = np.random.rand() * 100
    event = controller.step(
        action='TouchThenApplyForce',
        x=.5,
        y=.6,
        direction={
            'x': dir[0],
            'y': dir[1],
            'z': dir[2]
        },
        moveMagnitude=force,
        handDistance=10
    )
    if not event.metadata['actionReturn']['objectId'] == obj['objectId']:
        return []

    data = []
    for i in range(1000):
        controller.step('AdvancePhysicsStep', timestep=.01)
        obj = update_to_current_frame(controller, obj)
        data.append(obj)
        print(i)
    return data


if __name__ == '__main__':
    controller = Controller(scene="FloorPlan10")
    done = False
    while not done:
        obj = get_random_pickupable(controller)
        data = apply_random_force(controller, obj)
        print(data)
        if not data == []:
            done = True
    print(data)