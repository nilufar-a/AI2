"""This module contains Map class."""
from position import Position


class Map:
    """Map class implementation."""
    
    def __init__(self):
        """mod: this method is constructor."""
        self.__set_map_scheme(dict())
        self.__set_players_positions(list())
        self.__set_bots_positions(list())
        self.__set_turbos_positions(list())
        self.__set_obstacles_positions(list())
        self.__set_traces_positions(list())

    def __get_map_scheme(self) -> dict:
        return self.__map_scheme

    def __set_map_scheme(self, map_scheme: dict):
        self.__map_scheme = map_scheme

    map_scheme = property(__get_map_scheme, __set_map_scheme)

    def __get_players_positions(self) -> list:
        return self.__players_positions

    def __set_players_positions(self, players_positions: list):
        self.__players_positions = players_positions

    players_positions = property(__get_players_positions, __set_players_positions)

    def __get_bots_positions(self) -> list:
        return self.__bots_positions

    def __set_bots_positions(self, bots_positions: list):
        self.__bots_positions = bots_positions

    bots_positions = property(__get_bots_positions, __set_bots_positions)

    def __get_turbos_positions(self) -> list:
        return self.__turbos_positions

    def __set_turbos_positions(self, turbos_positions: list):
        self.__turbos_positions = turbos_positions

    turbos_positions = property(__get_turbos_positions, __set_turbos_positions)

    def __get_obstacles_positions(self) -> list:
        return self.__obstacles_positions

    def __set_obstacles_positions(self, obstacles_positions: list):
        self.__obstacles_positions = obstacles_positions

    obstacles_positions = property(__get_obstacles_positions, __set_obstacles_positions)

    def __get_traces_positions(self) -> list:
        return self.__traces_positions

    def __set_traces_positions(self, traces_positions: list):
        self.__traces_positions = traces_positions

    traces_positions = property(__get_traces_positions, __set_traces_positions)

    def get_possible_directions(self, block: Position) -> list:
        """
        mod: this function generates list of possible direction to move.

        Arguments:
            :param block - current position on the map

        Returns:
            :returns list of possible blocks of the map to move on

        """
        possible_directions = list()
        for row_index in range(block.row_index - 1, block.row_index + 2):
            for column_index in range(block.column_index - 1, block.column_index + 2):
                if row_index >= self.map_scheme['height']:
                    continue
                if column_index >= self.map_scheme['width']:
                    continue
                if not((row_index == block.row_index) == (column_index == block.column_index)):
                    continue
                next_position = Position(row_index, column_index)
                if next_position in self.players_positions:
                    continue
                if next_position in self.bots_positions:
                    continue
                if next_position in self.obstacles_positions:
                    continue
                if next_position in self.traces_positions:
                    continue
                possible_directions.append(next_position)
        return possible_directions

    def get_distance(self, start_block: Position, end_block: Position) -> int:
        """
        mod: this function calculates distance to end block.

        Arguments:
            :param start_block - current position on the map
            :param end_block - destination position on the map

        Returns:
            :returns distance to end block

        """
        row_distance = abs(end_block.row_index - start_block.row_index)
        column_distance = abs(end_block.column_index - start_block.column_index)
        distance = row_distance + column_distance
        return distance

    def get_density(self, current_block: Position, direction_block: Position) -> float:
        """
        mod: this function calculates density of map segment.

        Arguments:
            :param current_block - current position on the map
            :param direction_block - direction position on the map

        Returns:
            :returns distance to end block

        """
        cell_counter = 0
        obstacle_counter = 0
        start_row = 0
        end_row = self.map_scheme['height']
        start_column = 0
        end_column = self.map_scheme['width']

        if direction_block.row_index > current_block.row_index:
            start_row = direction_block.row_index
        elif direction_block.row_index < current_block.row_index:
            end_row = direction_block.row_index

        if direction_block.column_index > current_block.column_index:
            start_column = direction_block.column_index
        elif direction_block.column_index < current_block.column_index:
            end_column = direction_block.column_index

        for row_index in range(start_row, end_row):
            for column_index in range(start_column, end_column):
                cell_position = Position(row_index, column_index)
                cell_counter += 1
                if cell_position in self.players_positions:
                    obstacle_counter += 1
                if cell_position in self.bots_positions:
                    obstacle_counter += 1
                if cell_position in self.obstacles_positions:
                    obstacle_counter += 1
                if cell_position in self.traces_positions:
                    obstacle_counter += 1

        density = obstacle_counter / cell_counter
        return density
