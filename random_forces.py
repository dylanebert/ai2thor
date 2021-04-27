from ai2thor.controller import Controller
import numpy as np
import pandas as pd
import random
from tqdm import tqdm


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
    controller.step('RotateRight', degrees=np.random.rand() * 360)
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
    found = False
    for y in np.arange(0., .5, .01):
        for sign in [-1, 1]:
            event = controller.step(
                action='TouchThenApplyForce',
                x=.5,
                y=.5 + y * sign,
                direction={
                    'x': dir[0],
                    'y': dir[1],
                    'z': dir[2]
                },
                moveMagnitude=force,
                handDistance=10
            )
            if event.metadata['actionReturn']['objectId'] == obj['objectId']:
                found = True
                break
    assert found

    data = []
    prev_pos = np.zeros((3,))
    for i in range(1000):
        controller.step('AdvancePhysicsStep', timestep=.01)
        obj = update_to_current_frame(controller, obj)
        pos = np.array([obj['position']['x'], obj['position']['y'], obj['position']['z']])
        motion = np.linalg.norm(pos - prev_pos)
        prev_pos = pos
        data.append(obj)
        if motion < 1e-4:
            break
    return data


if __name__ == '__main__':
    train_kitchens = [f'FloorPlan{i}' for i in range(1, 21)]
    controller = Controller(scene=random.choice(train_kitchens))
    obj = get_random_pickupable(controller)
    data = apply_random_force(controller, obj)
    df = []
    for row in data:
        df.append({
            'name': row['name'],
            'posX': row['position']['x'],
            'posY': row['position']['y'],
            'posZ': row['position']['z'],
            'rotX': row['rotation']['x'],
            'rotY': row['rotation']['y'],
            'rotZ': row['rotation']['z']
        })
    df = pd.DataFrame(df)
    
    import time
    timestr = time.strftime('%Y%m%d-%H%M%S')
    df.to_json(f'data/{timestr}.json', orient='index')