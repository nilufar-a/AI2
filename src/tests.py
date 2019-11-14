import unittest

import main
from map import Map
from path_finder import PathFinder
from position import Position


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.current_map = Map()
        self.current_map.map_scheme['height'] = 32
        self.current_map.map_scheme['width'] = 32
        self.current_map.obstacles_positions = list()
        self.current_map.bots_positions = list()
        self.current_map.traces_positions = list()
        self.current_map.players_positions = [Position(0, 15), Position(15, 15), Position(5, 5)]
        self.current_map.obstacles_positions = [Position(0, 2), Position(4, 4)]
        self.path_finder = PathFinder()
        self.path_finder.tron_map = self.current_map
        start_position = Position(0, 0)
        self.path_finder.start_position = start_position
        self.path_finder.turbos_number = 0

    def test_random_algorithm(self):
        self.path_finder.algorithm = 'Random'
        next_move = self.path_finder.get_direction()
        self.assertTrue(next_move in self.current_map.get_possible_directions(self.path_finder.start_position))
        print(f'Random algorithm: {next_move}')

    def test_survival_algorithm(self):
        self.path_finder.algorithm = 'Survival'
        next_move = self.path_finder.get_direction()
        self.assertTrue(next_move in self.current_map.get_possible_directions(self.path_finder.start_position))
        print(f'Survival algorithm: {next_move}')

    def test_a_star_algorithm(self):
        self.path_finder.algorithm = 'A*'
        next_move = self.path_finder.get_direction()
        self.assertTrue(next_move in self.current_map.get_possible_directions(self.path_finder.start_position))
        print(f'A* algorithm: {next_move}')


if __name__ == '__main__':
    unittest.main()
