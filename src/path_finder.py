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

    def get_direction(self) -> tuple:
        """
        mod: this function calculates destination (target) block.

        Returns:
            :returns target_block -- next block to move on
            :returns turbo_flag -- next block to move on

        Raises:
            :raise NoSolution -- No possible direction to move on exception

        """
        self.generated_paths = list()
        possible_directions = self.tron_map.get_possible_directions(self.start_position)
        if not possible_directions:
            raise NoSolution('No possible direction to move on.')
        random_direction = possible_directions[randint(0, len(possible_directions) - 1)]
        turbo_flag = False

        if self.algorithm == 'Random':
            return random_direction, turbo_flag

        elif self.algorithm == 'Survival':
            direction_densities = list()
            for direction in possible_directions:
                density = self.tron_map.get_density(self.start_position, direction)
                direction_densities.append((density, direction))
            best_direction = sorted(direction_densities, key=lambda density_object: density_object[0])[0][1]
            return best_direction, turbo_flag

        elif self.algorithm == 'A*':
            for player_position in self.tron_map.players_positions:
                target_block = self.tron_map.get_possible_directions(player_position)[0]
                try:
                    generated_path = self.generate_path(self.start_position, target_block)
                    self.generated_paths.append(generated_path)
                except NoSolution:
                    continue

            if not self.generated_paths:
                return random_direction, turbo_flag

            shortest_path = self.get_shortest_path()
            if self.turbos_number and len(shortest_path) > 3:
                if shortest_path[0].row_index == shortest_path[1].row_index == shortest_path[2].row_index:
                    turbo_flag = True
                elif shortest_path[0].column_index == shortest_path[1].column_index == shortest_path[2].column_index:
                    turbo_flag = True
            next_position = shortest_path[1]
            return next_position, turbo_flag
        else:
            return random_direction, turbo_flag

    def generate_path(self, start_block: Position, target_block: Position) -> list:
        """
        mod: this function generates path to target_block.

        Arguments:
            :param start_block - destination position on the map
            :param target_block - destination position on the map

        Returns:
            :returns path to target_block

        Raises:
            :raise NoSolution -- No possible direction to move on exception

        """
        tron_map = self.tron_map

        def sorter(path_of_blocks: list):
            nonlocal tron_map, target_block
            covered_distance = len(path_of_blocks)
            last_node = path_of_blocks[-1]
            estimated_distance = tron_map.get_distance(last_node, target_block)
            total_cost = covered_distance + estimated_distance
            return total_cost

        closed_blocks = list()
        open_paths = list()
        open_paths.append([start_block])
        while open_paths:
            open_paths.sort(key=sorter)
            current_path = open_paths.pop(0)
            current_block = current_path[-1]
            if current_block in closed_blocks:
                continue
            if current_block == target_block:
                return current_path
            closed_blocks.append(current_block)
            for block in self.tron_map.get_possible_directions(current_block):
                if block in closed_blocks:
                    continue
                path = current_path + [block]
                open_paths.append(path)
        else:
            raise NoSolution('No possible path to reach destination.')

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
            return length

        sorted_paths = sorted(self.generated_paths, key=path_sorter, reverse=True)
        shortest_path = sorted_paths[0]
        return shortest_path


class NoSolution(Exception):
    """NoSolution exception ."""

    pass
