from ai2thor.controller import Controller
controller = Controller(scene="FloorPlan10")
controller.step('PausePhysicsAutoSim')
for obj in controller.last_event.metadata['objects']:
    print(obj['name'], obj['pickupable'])