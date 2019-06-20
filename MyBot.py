#!/usr/bin/env python3
# Python 3.6
import hlt
from hlt import constants
from hlt.positionals import Direction
import random
import logging
""" <<<Game Begin>>> """
game = hlt.Game()
game.ready("MyPythonBot")
def create_ship():
	command_queue.append(me.shipyard.spawn())

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

def go_home(oShip,tNow_doing):
	tDirection,sShip_state = tNow_doing
	sDireaction_name = get_name_of_direction(tDirection)
	sType = "vertically" if (sDireaction_name == "North" or sDireaction_name == "South") else "horizontal"
	tBase_position = (me.shipyard.position.x,me.shipyard.position.y)
	tShip_position = (oShip.position.x,oShip.position.y)
	# Если корабль находится на базе. Находится на стадии планирование
	if tBase_position[0] == tShip_position[0] and tBase_position[1] == tShip_position[1]:
		pass
		# tNew_direction = (0,"stay_still")
	# Если корабль не находится на оси x и y
	elif tBase_position[0] != tShip_position[0] and tBase_position[1] != tShip_position[1]:
		tNew_direction = find_best_direction_to_base_axis(tBase_position,tShip_position)
		logging.info(f"Выполнено 2 условие {tNew_direction}		{tNow_doing}")
	# Если корабль находится на оси x или y
	elif (tBase_position[0] != tShip_position[0] and tBase_position[1] == tShip_position[1]) or (tBase_position[0] == tShip_position[0] and tBase_position[1] != tShip_position[1]):
		sType = "vertically" if tBase_position[0] == tShip_position[0] else "horizontal"
		tNew_direction = find_best_direction_to_home(tBase_position,tShip_position,sType)
		logging.info(f"Выполнено 3 условие {tNew_direction}		{tNow_doing}")
	return (tNew_direction[1],sShip_state)

def find_best_direction_to_base_axis(tBase_position,tShip_position):
	dChoice = {}
	dChoice["horizontal"] = find_best_direction_to_home(tBase_position,tShip_position,"horizontal")
	dChoice["vertically"] = find_best_direction_to_home(tBase_position,tShip_position,"vertically")
	if dChoice["horizontal"][0] == dChoice["vertically"][0]:
		return dChoice[random.choice(["horizontal","vertically"])]
	else:
		return dChoice["horizontal"] if dChoice["horizontal"][0]< dChoice["vertically"][0] else dChoice["vertically"]

def find_best_direction_to_home(tBase_position,tShip_position,sType):
	iMap_width = iMap_height = 32
	iBase_coordinate = tBase_position[1] if sType == "vertically" else tBase_position[0]
	iShip_coordinate = tShip_position[1] if sType == "vertically" else tShip_position[0]
	iH_base = iMap_height - iBase_coordinate
	iH_ship = iMap_height - iShip_coordinate
	bIs_ship_on_top = True if iBase_coordinate-iShip_coordinate>0 else False
	# logging.info(f"iBase_coordinate {iBase_coordinate} iShip_coordinate {iShip_coordinate}")
	if bIs_ship_on_top:
		iIndicator1_turn_count = iMap_height-iH_ship+iH_base
		iIndicator2_turn_count = iH_ship - iH_base
	else:
		iIndicator1_turn_count = iH_base - iH_ship
		iIndicator2_turn_count = iMap_height - iH_base+iH_ship
	sIndicator_1_name = Direction.North if sType == "vertically" else Direction.West
	sIndicator_2_name = Direction.South if sType == "vertically" else Direction.East
	tOptimal_turn_diraction = sIndicator_1_name if iIndicator1_turn_count<iIndicator2_turn_count else sIndicator_2_name
	iOptimal_turn_count = iIndicator1_turn_count if iIndicator1_turn_count<iIndicator2_turn_count else iIndicator2_turn_count
	return (iOptimal_turn_count,tOptimal_turn_diraction)

directions = [Direction.North, Direction.South, Direction.East, Direction.West]
tNow_doing = (random.choice(directions),"Search")
# now_doing = (Direction.West,"Search")
""" <<<Game Loop>>> """
while True:
	game.update_frame()
	me = game.me
	game_map = game.game_map
	command_queue = []
	for ship in me.get_ships():
		if ship.halite_amount == 0 or tNow_doing[1] == "Search":
			tNow_doing = (random.choice(directions),"Search")
		# choices = ship.position.get_surrounding_cardinals()
		if game_map[ship.position].halite_amount < constants.MAX_HALITE / 100 or ship.is_full:
			if ship.is_full:
				tNow_doing = (tNow_doing[0],"Return")
			if tNow_doing[1] == "Return":
				tNow_doing = go_home(ship,tNow_doing)
			command_queue.append(
				ship.move(tNow_doing[0])
			)
		else:
			command_queue.append(ship.stay_still())
		# logging.info("ship {} type of position {}".format(ship,type(ship.position)))
	if game.turn_number == 1:
		create_ship()

	# If the game is in the first 200 turns and you have enough halite, spawn a ship.
	# Don't spawn a ship if you currently have a ship at port, though - the ships will collide.
	# if game.turn_number <= 200 and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied:
	# create_ship()
	# Send your moves back to the game environment, ending this turn.
	game.end_turn(command_queue)
