import unittest

import main
from map import Map
from path_finder import PathFinder, NoSolution
from position import Position


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.current_map = Map()
        self.path_finder = PathFinder()
        self.path_finder.tron_map = self.current_map

    def arrangement_1(self):
        self.current_map.map_scheme['height'] = 64
        self.current_map.map_scheme['width'] = 64
        self.current_map.obstacles_positions = list()
        self.current_map.bots_positions = list()
        self.current_map.traces_positions = list()
        self.current_map.players_positions = [Position(63, 63)]

        self.path_finder.start_position = Position(0, 0)
        self.path_finder.turbos_number = 0

    def arrangement_2(self):
        self.current_map.map_scheme['height'] = 16
        self.current_map.map_scheme['width'] = 16
        self.current_map.obstacles_positions = [Position(0, 1), Position(1, 1), Position(2, 1), Position(3, 1),
                                                Position(4, 1), Position(5, 1), Position(6, 1), Position(7, 1)]
        self.current_map.bots_positions = [Position(6, 0)]
        self.current_map.traces_positions = [Position(8, 0), Position(9, 0), Position(10, 0), Position(11, 0),
                                             Position(12, 0), Position(13, 0), Position(14, 0), Position(15, 0)]
        self.current_map.players_positions = [Position(15, 1)]

        self.path_finder.start_position = Position(7, 0)
        self.path_finder.turbos_number = 3

    def arrangement_3(self):
        self.current_map.map_scheme['height'] = 64
        self.current_map.map_scheme['width'] = 64
        self.current_map.obstacles_positions = list()
        self.current_map.bots_positions = list()
        self.current_map.traces_positions = list()
        self.current_map.players_positions = [Position(63, 63)]

        self.path_finder.start_position = Position(0, 0)
        self.path_finder.turbos_number = 1

    def arrangement_4(self):
        self.current_map.map_scheme['height'] = 16
        self.current_map.map_scheme['width'] = 16
        self.current_map.obstacles_positions = list()
        self.current_map.bots_positions = list()
        self.current_map.traces_positions = [Position(0, 7), Position(1, 7), Position(2, 7), Position(3, 7),
                                             Position(4, 7), Position(5, 7), Position(6, 7), Position(7, 7)]
        self.current_map.players_positions = [Position(0, 8)]

        self.path_finder.start_position = Position(3, 3)
        self.path_finder.turbos_number = 3

    def arrangement_5(self):
        self.current_map.map_scheme['height'] = 16
        self.current_map.map_scheme['width'] = 16
        self.current_map.obstacles_positions = [Position(8, 8), Position(8, 9), Position(8, 10), Position(8, 11),
                                                Position(8, 12), Position(8, 13), Position(8, 14), Position(8, 15)]
        self.current_map.bots_positions = list()
        self.current_map.traces_positions = [Position(0, 7), Position(1, 7), Position(2, 7), Position(3, 7),
                                             Position(4, 7), Position(5, 7), Position(6, 7), Position(7, 7)]
        self.current_map.players_positions = [Position(0, 8)]

        self.path_finder.start_position = Position(10, 15)
        self.path_finder.turbos_number = 3

    def test_get_direction_1(self):
        for algorithm in ('Random', 'Survival', 'A*'):
            self.path_finder.algorithm = algorithm
            with self.subTest(algorithm=algorithm, arrangement=1):
                self.arrangement_1()
                next_move, turbo_flag = self.path_finder.get_direction()
                self.assertTrue(next_move in self.current_map.get_possible_directions(self.path_finder.start_position))
                self.assertFalse(turbo_flag)

    def test_get_direction_2(self):
        for algorithm in ('Random', 'Survival', 'A*'):
            self.path_finder.algorithm = algorithm
            with self.subTest(algorithm=algorithm, arrangement=2):
                self.arrangement_2()
                with self.assertRaises(NoSolution):
                    self.path_finder.get_direction()

    def test_get_direction_3(self):
        for algorithm in ('Random', 'Survival', 'A*'):
            self.path_finder.algorithm = algorithm
            with self.subTest(algorithm=algorithm, arrangement=3):
                self.arrangement_3()
                next_move, turbo_flag = self.path_finder.get_direction()
                self.assertTrue(next_move in self.current_map.get_possible_directions(self.path_finder.start_position))

                if algorithm == 'Random':
                    self.assertFalse(turbo_flag)
                elif algorithm == 'Survival':
                    self.assertFalse(turbo_flag)
                elif algorithm == 'A*':
                    self.assertTrue(turbo_flag)
                else:
                    raise Exception('Unknown algorithm')

    def test_get_direction_4(self):
        for algorithm in ('Random', 'Survival', 'A*'):
            self.path_finder.algorithm = algorithm
            with self.subTest(algorithm=algorithm, arrangement=4):
                self.arrangement_4()
                next_move, turbo_flag = self.path_finder.get_direction()
                self.assertTrue(next_move in self.current_map.get_possible_directions(self.path_finder.start_position))

                if algorithm == 'Random':
                    self.assertFalse(turbo_flag)
                elif algorithm == 'Survival':
                    self.assertFalse(turbo_flag)
                elif algorithm == 'A*':
                    self.assertTrue(turbo_flag)
                else:
                    raise Exception('Unknown algorithm')

    def test_get_direction_5(self):
        for algorithm in ('Random', 'Survival', 'A*'):
            self.path_finder.algorithm = algorithm
            with self.subTest(algorithm=algorithm, arrangement=5):
                self.arrangement_5()
                next_move, turbo_flag = self.path_finder.get_direction()
                self.assertTrue(next_move in self.current_map.get_possible_directions(self.path_finder.start_position))

                if algorithm == 'Random':
                    self.assertFalse(turbo_flag)
                elif algorithm == 'Survival':
                    self.assertFalse(turbo_flag)
                elif algorithm == 'A*':
                    self.assertFalse(turbo_flag)
                else:
                    raise Exception('Unknown algorithm')


if __name__ == '__main__':
    unittest.main()
