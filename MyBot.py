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
# This game object contains the initial game state.
game = hlt.Game()
# At this point "game" variable is populated with initial map data.
# This is a good place to do computationally expensive start-up pre-processing.
# As soon as you call "ready" function below, the 2 second per turn timer will start.
game.ready("MyPythonBot")
# Now that your bot is initialized, save a message to yourself in the log file with some important information.
#     Here, you log here your id, which you can always fetch from the game object by using my_id.
# logging.info("Successfully created bot! My Player ID is {}.".format(game.my_id))


def create_ship():
	command_queue.append(me.shipyard.spawn())

def is_on_top_part(y_coordination):
	return y_coordination >= 0 and y_coordination <= 15

def is_on_left_part(x_coordination):
	return x_coordination >= 0 and x_coordination <= 15

def get_name_of_direction(direction):
	if direction == Direction.North:
		return "North"
	elif direction == Direction.South:
		return "South"
	elif direction == Direction.West:
		return "West"
	elif direction == Direction.East:
		return "East"

def get_opposite_direction(direction):
	if direction == Direction.North:
		return Direction.South
	elif direction == Direction.South:
		return Direction.North
	elif direction == Direction.West:
		return Direction.East
	elif direction == Direction.East:
		return Direction.West

def turn_around(oShip,tNow_doing):
	tDirection,sShip_state = tNow_doing
	sNew_ship_state = "Return" if sShip_state == "Search" else "Return"
	sDireaction_name = get_name_of_direction(tDirection)
	if sDireaction_name == "North" or sDireaction_name == "South":
		if is_on_top_part(oShip.position.y):
			tNew_direction =  Direction.South
		else:
			tNew_direction =  Direction.North
	elif sDireaction_name == "West" or sDireaction_name == "Easth":
		pass
	return (tNew_direction,sNew_ship_state)
	

def get_type_of_ship(now_doing):
	
	pass

directions = [Direction.North, Direction.South, Direction.East, Direction.West]
vertical_ships = [Direction.North, Direction.South]
horizontal_ships = [Direction.East, Direction.West]
now_doing = (random.choice(directions),"Search")









now_doing = (Direction.West,"Search")
""" <<<Game Loop>>> """
while True:
	# This loop handles each turn of the game. The game object changes every turn, and you refresh that state by
	#     running update_frame().
	game.update_frame()
	# You extract player metadata and the updated map metadata here for convenience.
	me = game.me
	game_map = game.game_map

	# A command queue holds all the commands you will run this turn. You build this list up and submit it at the
	#     end of the turn.
	command_queue = []

	for ship in me.get_ships():
		if ship.halite_amount == 0:
			tNow_doing = (Direction.West,"Search")

		# new_direction = random.choice(directions)
		# choices = ship.position.get_surrounding_cardinals()
		# logging.info(Direction.North)
		# For each of your ships, move randomly if the ship is on a low halite location or the ship is full.
		#     Else, collect halite.
		if game_map[ship.position].halite_amount < constants.MAX_HALITE / 100 or ship.is_full:
			if ship.is_full:
				tNow_doing = turn_around(ship,tNow_doing)
			command_queue.append(
				ship.move(tNow_doing[0])
			)
		else:
			command_queue.append(ship.stay_still())
		logging.info("ship {} type of position {}".format(ship,type(ship.position)))

	if game.turn_number == 1:
		create_ship()

	# If the game is in the first 200 turns and you have enough halite, spawn a ship.
	# Don't spawn a ship if you currently have a ship at port, though - the ships will collide.
	# if game.turn_number <= 200 and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied:
	# create_ship()
	# command_queue.append(me.shipyard.spawn())

	# Send your moves back to the game environment, ending this turn.
	game.end_turn(command_queue)
