"""

	1	2	3	4	5	6	7	8	9	10	11						1	2	3	4	5	6	7	8	9	10	11
1				|								1				1				|								1
2				|								2				2				|								2
3				|								3				3				|								3
4				|								4				4				|								4
5				|								5				5				|	6	5	6					5
6				|		*						6				6				|	4	2	6					6
7				|								7				7				|	6	7	6					7
8				|								8				8				|	7	7	7					8
9	-	-	-	0	-	-	-	-	-	-	-	9				9	-	-	-	0	-	-	-	-	-	-	-	9
10				|								10				10				|								10
11				|								11				11				|								11
	1	2	3	4	5	6	7	8	9	10	11						1	2	3	4	5	6	7	8	9	10	11



+	Поиск оптимального путя до базы с оси x или y
+	Поиск оптимального путя до базы с любой точки
	Поиск направлнеия, где есть самое большое скопление энергии
	Запомнить местность, где много энергии  при возращении на базу
		Вычисление энергии|сохранение дороги до этой местности|

"""
import random
def find_best_direction_to_home(tBase_position,tShip_position,sType):
	iMap_width = iMap_height = 11
	iBase_coordinate = tBase_position[1] if sType == "vertically" else tBase_position[0]
	iShip_coordinate = tShip_position[1] if sType == "vertically" else tShip_position[0]
	iH_base = iMap_height - iBase_coordinate
	iH_ship = iMap_height - iShip_coordinate
	bIs_ship_on_top = True if iBase_coordinate-iShip_coordinate>0 else False
	if bIs_ship_on_top:
		iIndicator1_turn_count = iMap_height-iH_ship+iH_base
		iIndicator2_turn_count = iH_ship - iH_base
	else:
		iIndicator1_turn_count = iH_base - iH_ship
		iIndicator2_turn_count = iMap_height - iH_base+iH_ship
	sIndicator_1_name = "top" if sType == "vertically" else "left"
	sIndicator_2_name = "bottom" if sType == "vertically" else "right"
	optimal_turn_name = sIndicator_1_name if iIndicator1_turn_count<iIndicator2_turn_count else sIndicator_2_name
	optimal_turn_count = iIndicator1_turn_count if iIndicator1_turn_count<iIndicator2_turn_count else iIndicator2_turn_count
	return (optimal_turn_count,optimal_turn_name)

def find_best_direction_to_base_axis(tBase_position,tShip_position):
	dChoice = {}
	dChoice["horizontal"] = find_best_direction_to_home(tBase_position,tShip_position,"horizontal")
	dChoice["vertically"] = find_best_direction_to_home(tBase_position,tShip_position,"vertically")
	if dChoice["horizontal"][0] == dChoice["vertically"][0]:
		return dChoice[random.choice(["horizontal","vertically"])]
	else:
		return dChoice["horizontal"] if dChoice["horizontal"][0]< dChoice["vertically"][0] else dChoice["vertically"]

def go_home(tBase_position,tShip_position):
	if tBase_position[0] == tShip_position[0] and tBase_position[1] == tShip_position[1]:
		result = (0,"stay_still")
	elif tBase_position[0] != tShip_position[0] and tBase_position[1] != tShip_position[1]:
		print(f"2 условие")
		result = find_best_direction_to_base_axis(tBase_position,tShip_position)
	else:
		print(f"3 условие")
		sType = "vertically" if tBase_position[0] == tShip_position[0] else "horizontal"
		result = find_best_direction_to_home(tBase_position,tShip_position,sType)

	print(result)

# tBase_position = (4,9)
# tShip_position = (6,6)
# go_home(tBase_position,tShip_position)


class Direction:
	North = (0, -1)
	South = (0, 1)
	East = (1, 0)
	West = (-1, 0)
	Still = (0, 0)
	
	@staticmethod
	def get_all_cardinals():
		return [Direction.North, Direction.South, Direction.East, Direction.West]

class Ship:
	def __init__(self, x, y):
		self.x = x
		self.y = y
	def change_position(self,tDirection):
		self.tPosition = (self.tPosition[0]+tDirection[0],self.tPosition[1]+tDirection[2])
	
	def get_surrounding_cardinals(self):
		return [current_direction for current_direction in Direction.get_all_cardinals()]

a = Ship(4,6)
a.get_surrounding_cardinals()

class Base:
	tPosition = (4,9)

class Map:
	dGame_map = {
		(5,5):6,	(6,5):5,	(7,5):6,
		(5,6):4,	(6,6):2,	(7,6):6,
		(5,7):6,	(6,7):7,	(7,6):6,
		(5,8):7,	(6,8):7,	(7,8):7,
	}

def get_best_profit(tBase_position,tShip_position):
	# aDirections = [Direction.North, Direction.South, Direction.East, Direction.West, Direction.Still]
	pass

