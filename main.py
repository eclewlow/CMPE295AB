# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
#!/usr/bin/env python

# Copyright (c) 2021 Computer Vision Center (CVC) at the Universitat Autonoma de
# Barcelona (UAB).
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

"""Example script to generate traffic in the simulation"""

import glob
import os
import sys
import time

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

from carla import VehicleLightState as vls

import argparse
import logging
from numpy import random

def main():
    try:
        client = carla.Client('127.0.0.1', 2000)
        client.set_timeout(10.0)
        client.load_world('Town06')
        client.reload_world()
        world = client.get_world()
        spawn_points = world.get_map().get_spawn_points()
        print(spawn_points)
        print(len(spawn_points))
        actor_list = world.get_actors()
        print(len(actor_list))
        print(actor_list)
        for actor in actor_list.filter('vehicle.*.*'):
            actor.destroy()
        blueprint_library = world.get_blueprint_library()
        vehicle_bp = random.choice(blueprint_library.filter('vehicle.*.*'))
        actor = world.spawn_actor(vehicle_bp, spawn_points[0])

        spectator = world.get_spectator()
        transform = actor.get_transform()
        spectator.set_transform(carla.Transform(transform.location + carla.Location(z=50),
                                                carla.Rotation(pitch=-90)))
        actor.set_autopilot(True)

        while True:
            transform = actor.get_transform()
            spectator.set_transform(carla.Transform(transform.location + carla.Location(z=50),
                                                    carla.Rotation(pitch=-90)))
            world.wait_for_tick()
    finally:
        actor_list = world.get_actors()
        print(len(actor_list))
        print(actor_list)
        for actor in actor_list.filter('vehicle.*.*'):
            actor.destroy()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print("done")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
