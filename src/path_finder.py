"""This module contains PathFinder class."""
from map import Map
from position import Position


class PathFinder:
    """PathFinder class implementation."""

    def __init__(self):
        """mod: this method is constructor."""
        self.__set_tron_map(Map())
        self.__set_algorithm(str())
        self.__set_generated_paths(list())
        self.__set_turbo_number(list())

    def __get_tron_map(self) -> Map:
        return self.__tron_map

    def __set_tron_map(self, tron_map: Map):
        self.__tron_map = tron_map

    tron_map = property(__get_tron_map, __set_tron_map)

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

    def __get_turbo_number(self) -> int:
        return self.__turbo_number

    def __set_turbo_number(self, turbo_number: int):
        self.__turbo_number = turbo_number

    turbo_number = property(__get_turbo_number, __set_turbo_number)

    def get_direction(self) -> Position:
        """
        mod: this function calculates destination (target) block.

        Returns:
            :returns target_block

        """
        pass

    def generate_path(self, target_block: Position) -> list:
        """
        mod: this function generates path to target_block.

        Arguments:
            :param target_block - destination position on the map

        Returns:
            :returns path to target_block

        """
        pass

    def get_shortest_path(self) -> list:
        """
        mod: this function calculates shortest (cheapest) from generated paths.

        Returns:
            :returns shortest (cheapest) path

        """
        pass
