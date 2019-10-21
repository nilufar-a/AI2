"""This module contains Map class."""
from position import Position


class Map:
    """Map class implementation."""
    
    def __init__(self):
        """mod: this method is constructor."""
        self.__set_map_scheme(dict())
        self.__set_player_positions(list())
        self.__set_bots_positions(list())
        self.__set_turbo_positions(list())

    def __get_map_scheme(self) -> dict:
        return self.__map_scheme

    def __set_map_scheme(self, map_scheme: dict):
        self.__map_scheme = map_scheme

    map_scheme = property(__get_map_scheme, __set_map_scheme)

    def __get_player_positions(self) -> list:
        return self.__player_positions

    def __set_player_positions(self, player_positions: list):
        self.__player_positions = player_positions

    player_positions = property(__get_player_positions, __set_player_positions)

    def __get_bots_positions(self) -> list:
        return self.__bots_positions

    def __set_bots_positions(self, bots_positions: list):
        self.__bots_positions = bots_positions

    bots_positions = property(__get_bots_positions, __set_bots_positions)

    def __get_turbo_positions(self) -> list:
        return self.__turbo_positions

    def __set_turbo_positions(self, turbo_positions: list):
        self.__turbo_positions = turbo_positions

    turbo_positions = property(__get_turbo_positions, __set_turbo_positions)

    def get_possible_directions(self, block: Position) -> list:
        """
        mod: this function generates list of possible direction to move.

        Arguments:
            :param block - current position on the map

        Returns:
            :returns list of possible blocks of the map to move on

        """
        pass

    def get_distance(self, start_block: Position, end_block: Position) -> int:
        """
        mod: this function calculates distance to end block.

        Arguments:
            :param start_block - current position on the map
            :param end_block - destination position on the map

        Returns:
            :returns distance to end block

        """
        pass
