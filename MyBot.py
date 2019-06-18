#!/usr/bin/env python3
# Python 3.6

# Import the Halite SDK, which will let you interact with the game.
import hlt

# This library contains constant values.
from hlt import constants

# This library contains direction metadata to better interface with the game.
from hlt.positionals import Direction

# This library allows you to generate random numbers.
import random

# Logging allows you to save messages for yourself. This is required because the regular STDOUT
# (print statements) are reserved for the engine-bot communication.
import logging

""" <<<Game Begin>>> """

game = hlt.Game()
game.ready("MyPythonBot")
logging.info("Successfully created bot! My Player ID is {}.".format(game.my_id))
def create_ship():
	command_queue.append(me.shipyard.spawn())
directions = [Direction.North, Direction.South, Direction.East, Direction.West]

now_doing = Direction.North
""" <<<Game Loop>>> """
while True:
	game.update_frame()
	me = game.me
	game_map = game.game_map
	command_queue = []
	if me.halite_amount >= 4500:
		now_doing = Direction.North
	for ship in me.get_ships():
		new_direction = random.choice(directions)
		control = False 
		if game_map[ship.position].halite_amount < constants.MAX_HALITE / 100 or ship.is_full:
			if ship.is_full:
				now_doing = Direction.South
			command_queue.append(
				ship.move(now_doing)
			)
		else:
			command_queue.append(ship.stay_still())

	if game.turn_number == 1:
		create_ship()
	game.end_turn(command_queue)
