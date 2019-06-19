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

def function_name(kShip,kBase):
	# если корабль находится под базой
	iHeight_map = 32
	bIs_ship_on_top = True if kBase[1]-kShip[1]>0 else False
	if bIs_ship_on_top  == True:
		# если корабль находится над базой
		iShipvverh = iHeight_map - kBase[1] + kShip[1]
		iShipvniz = kBase[1] - kShip[1] 
	else:
		# если корабль находится под базой
		iH_ship= iHeight_map - kShip[1]
		iTop_base = iHeight_map + kShip[0] - kBase[1]
		iShipvniz = iH_ship + iTop_base
		iShipvverh = iHeight_map - kBase[1] - iH_ship
	# print(f"вверх {iShipvverh} Вниз {iShipvniz}")
	if iShipvverh<iShipvniz:
		return Direction.North
	else:
		return Direction.South


while True:
	game.update_frame()
	me = game.me
	game_map = game.game_map
	command_queue = []
	for ship in me.get_ships():
		kShip = (ship.position.x,ship.position.y)
		kBase = (me.shipyard.position.x,me.shipyard.position.y)
		# Если энергии 0, то идет на север
		if ship.halite_amount == 0:
			now_doing = Direction.North
		# Если клеткада достаточно энергии или корабль полный
		if game_map[ship.position].halite_amount < constants.MAX_HALITE / 100 or ship.is_full:
			# Если корабль полный
			logging.info(f"1 {now_doing}")
			if ship.is_full:
				now_doing = function_name(kShip,kBase)
				# logging.info(f"2 {now_doing}")

			command_queue.append(
				ship.move(now_doing)
			)
		else:
			# Оставаться на месте
			command_queue.append(ship.stay_still())
	if game.turn_number == 1:
		create_ship()
	game.end_turn(command_queue)
