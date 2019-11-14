"""This module contains Position class."""


class Position:
    """Position class implementation."""

    def __init__(self, row_index: int, column_index: int):
        """mod: this method is constructor."""
        self.__set_row_index(row_index)
        self.__set_column_index(column_index)

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

    def __eq__(self, other):
        if self.row_index == other.row_index and self.column_index == other.column_index:
            return True
        else:
            return False

    def __str__(self):
        return f"Row: {self.row_index}, Column: {self.column_index}"
