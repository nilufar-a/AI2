"""This module contains AI Bot implementation for TRON game."""
import sys

from flask import Flask
from map import Map
from path_finder import PathFinder
from position import Position

app = None
current_map = None
path_finder = None


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
    app = Flask(__name__)
    app.run(sys.argv)
