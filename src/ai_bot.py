"""This module contains AI Bot implementation for TRON game."""
import sys

from flask import Flask, request
from map import Map
from path_finder import PathFinder
from position import Position

app = Flask(__name__)
current_map = None
path_finder = None

AI_ID=900

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'

@app.route('/getmove', methods=['POST'])
def get_move():
	try:
		gamestate = request.json
		ai = None

		# add obstacle
		_map = gamestate['map']
		left_wall = 	[{'xCoor' : i, 'yCoor' : 0} for i in range(_map['width'])]
		right_wall = 	[{'xCoor' : i, 'yCoor' : _map['height'] - 1} for i in range(_map['width'])]
		top_wall = 	[{'xCoor' : 0, 'yCoor' : i} for i in range(_map['height'])]
		bottom_wall = 	[{'xCoor' : _map['width'] - 1, 'yCoor' : i} for i in range(_map['height'])] 

		obstacles = left_wall + right_wall + top_wall + bottom_wall
				

		for obstacle in _map['obstacles']:
			obstacles.append(obstacle)

		print(obstacles)

		for player in gamestate['players']:
			# add head obstacles
			obstacles.append(player['headPosition'])

			# add body obstacles
			for point in player['tracer']:
				obstacles.append(point)

			# find the AI player
			if player['id'] == "900":
				ai = player

		direction = (ai['headPosition']['xCoor'] - ai['tracer'][0]['xCoor'],  ai['headPosition']['yCoor'] - ai['tracer'][0]['yCoor'])

		# directions
		
		forward = {'xCoor' : ai['headPosition']['xCoor'] + direction[0], 'yCoor' : ai['headPosition']['yCoor'] + direction[1]}


		left = [i * -1 for i in direction[::-1]]
		left = { 'xCoor' : ai['headPosition']['xCoor'] + left[0], 'yCoor' :  ai['headPosition']['yCoor'] + left[1]}

		right = direction[::-1]
		right = { 'xCoor' : ai['headPosition']['xCoor'] + right[0], 'yCoor' :  ai['headPosition']['yCoor'] + right[1]}

		if forward not in obstacles:
			return {'direction' : forward}

		if left not in obstacles:
			return {'direction' : left}

		if right not in obstacles:
			return {'direction' : right}
			
		return {'direction' : forward}
	except Exception as e:
		raise e
		return {"status" : "error", "error" : str(e)}


def main() -> None:
    """mod: this function is main function of the module."""
    pass


def parse_request() -> None:
    """mod: this function parses REST API request."""
    pass


def generate_response() -> None:
    """mod: this function generates REST API response."""
    pass


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
