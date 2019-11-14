"""This module contains PathFinder class."""
from random import randint
from map import Map
from position import Position


class PathFinder:
    """PathFinder class implementation."""

    def __init__(self):
        """mod: this method is constructor."""
        self.__set_tron_map(Map())
        self.__set_start_position(Position(0, 0))
        self.__set_algorithm(str())
        self.__set_generated_paths(list())
        self.__set_turbos_number(list())

    def __get_tron_map(self) -> Map:
        return self.__tron_map

    def __set_tron_map(self, tron_map: Map):
        self.__tron_map = tron_map

    tron_map = property(__get_tron_map, __set_tron_map)

    def __get_start_position(self) -> Position:
        return self.__start_position

    def __set_start_position(self, start_position: Position):
        self.__start_position = start_position

    start_position = property(__get_start_position, __set_start_position)

    def __get_algorithm(self) -> str:
        return self.__algorithm

    def __set_algorithm(self, algorithm: str):
        self.__algorithm = algorithm

    algorithm = property(__get_algorithm, __set_algorithm)

    def __get_generated_paths(self) -> list:
        return self.__generated_paths

    def __set_generated_paths(self, generated_paths: list):
        self.__generated_paths = generated_paths

    generated_paths = property(__get_generated_paths, __set_generated_paths)

    def __get_turbos_number(self) -> int:
        return self.__turbos_number

    def __set_turbos_number(self, turbos_number: int):
        self.__turbos_number = turbos_number

    turbos_number = property(__get_turbos_number, __set_turbos_number)

    def get_direction(self) -> Position:
        """
        mod: this function calculates destination (target) block.

        Returns:
            :returns target_block

        """
        possible_directions = self.tron_map.get_possible_directions(self.start_position)
        random_direction = possible_directions[randint(0, len(possible_directions) - 1)]

        if self.algorithm == 'Random':
            return random_direction

        elif self.algorithm == 'Survival':
            direction_densities = list()
            for direction in possible_directions:
                density = self.tron_map.get_density(self.start_position, direction)
                direction_densities.append((density, direction))
            best_direction = sorted(direction_densities, key=lambda density_object: density_object[0])[0][1]
            return best_direction

        elif self.algorithm == 'A*':
            for player_position in self.tron_map.players_positions:
                target_block = self.tron_map.get_possible_directions(player_position)[0]
                generated_path = self.generate_path(self.start_position, target_block, list())
                self.generated_paths.append(generated_path)
            shortest_path = self.get_shortest_path()
            next_position = shortest_path[0]
            return next_position
        else:
            return random_direction

    def generate_path(self, start_block: Position, target_block: Position, path: list) -> list:
        """
        mod: this function generates path to target_block.

        Arguments:
            :param start_block - destination position on the map
            :param target_block - destination position on the map
            :param path - already calculated path

        Returns:
            :returns path to target_block

        """
        if start_block == target_block:
            return path

        tron_map = self.tron_map

        def sorter(current_block: Position):
            nonlocal tron_map, target_block
            covered_distance = len(path)
            estimated_distance = tron_map.get_distance(current_block, target_block)
            total_cost = covered_distance + estimated_distance
            return total_cost

        possible_directions = self.tron_map.get_possible_directions(start_block)
        for i, direction in enumerate(possible_directions):
            if direction in path:
                possible_directions.pop(i)

        for next_block in sorted(possible_directions, key=sorter):
            new_path = list(path)
            new_path.append(next_block)

            return_value = self.generate_path(next_block, target_block, new_path)
            if return_value:
                return return_value
            else:
                continue

    def get_shortest_path(self) -> list:
        """
        mod: this function calculates shortest (cheapest) from generated paths.

        Returns:
            :returns shortest (cheapest) path

        """
        turbos_number = self.turbos_number
        tron_map = self.tron_map
        start_position = self.start_position

        def path_sorter(path: list):
            nonlocal turbos_number, tron_map, start_position

            if turbos_number == 0:
                return len(path)
            length = 0
            horizontal_consecutive = 0
            vertical_consecutive = 0
            previous_position = start_position
            for current_position in path:
                if turbos_number > 0:
                    if current_position.row_index == previous_position.row_index:
                        vertical_consecutive = 0
                        horizontal_consecutive += 1
                    elif current_position.column_index == previous_position.column_index:
                        horizontal_consecutive = 0
                        vertical_consecutive += 1
                    else:
                        if current_position not in tron_map.turbos_positions:
                            length += 1

                    if horizontal_consecutive == 3 or vertical_consecutive == 3:
                        horizontal_consecutive = 0
                        vertical_consecutive = 0
                        length -= 2
                else:
                    if current_position not in tron_map.turbos_positions:
                        length += 1

        sorted_paths = sorted(self.generated_paths, key=path_sorter, reverse=True)
        shortest_path = sorted_paths[0]
        return shortest_path
