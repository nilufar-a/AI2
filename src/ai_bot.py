"""This module contains AI Bot implementation for TRON game."""
import sys

from flask import Flask
from map import Map
from path_finder import PathFinder
from position import Position

app = Flask(__name__)
current_map = None
path_finder = None

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'

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
    app.run(host='127.0.0.1', port=8080, debug=True)
