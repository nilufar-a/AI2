"""This module contains Position class."""


class Position:
    """Position class implementation."""

    def __init__(self, row_index: int, column_index: int):
        """mod: this method is constructor."""
        self.__set_row_index(row_index)
        self.__set_row_index(column_index)

    def __get_row_index(self) -> int:
        return self.__row_index

    def __set_row_index(self, row_index: int):
        self.__row_index = row_index

    row_index = property(__get_row_index, __set_row_index)

    def __get_column_index(self) -> int:
        return self.__column_index

    def __set_column_index(self, column_index: int):
        self.__column_index = column_index

    column_index = property(__get_column_index, __set_column_index)
