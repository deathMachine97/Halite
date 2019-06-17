"""

	1	2	3	4	5	6	7	8	9	10	11
1												1
2												2
3												3
4												4
5												5
6												6
7												7
8				*								8
9				0						/		9
10												10
11												11
	1	2	3	4	5	6	7	8	9	10	11	

"""
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
	return sIndicator_1_name if iIndicator1_turn_count<iIndicator2_turn_count else sIndicator_2_name

sType = "hor"
tBase_position = (4,9)
tShip_position = (10,9)
result = find_best_direction_to_home(tBase_position,tShip_position,sType)
print(result)