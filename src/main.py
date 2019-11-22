"""This module contains AI Bot implementation for TRON game."""
import requests
import json
from threading import Thread
from flask import Flask, request, make_response
from map import Map
from path_finder import PathFinder, NoSolution

app = Flask(__name__)

# todo add URLs and method names (find in in APIGateway REST API Description)
api_gateway_urls = None
get_current_state_method = None
post_move_method = None
unregister_user_method = None


@app.route('/', methods=['GET'])
def test_response():
    """Return a HTTP response."""
    return make_response('OK', 200)


@app.route('/ai-bot', methods=['POST'])
def create_bot():
    # todo check JSON key names (in APIGateway/MatchMaking REST API Description)
    # todo write API request description together with AI1/APIGateway/MatchMaking teams
    data = request.get_json()
    user_id = data['userID']
    game_id = data['gameID']
    token = data['token']

    if user_id and game_id and token:
        bot = Thread(target=bot_routine, args=(user_id, game_id, token), daemon=True)
        bot.start()
        return make_response('OK', 200)
    else:
        return make_response('BAD REQUEST', 400)


def bot_routine(user_id: int, game_id: int, token: str) -> None:
    """mod: this function is main function of the module."""
    current_map = Map()
    path_finder = PathFinder()
    start_position = None
    next_move = None
    turbo_flag = False
    current_state_response = None
    game_status_flag = True

    def send_current_state_request() -> None:
        """mod: this function sends REST API request."""
        global api_gateway_urls, get_current_state_method
        nonlocal user_id, game_id, token, current_state_response
        # todo check JSON key names (in APIGateway REST API Description)
        current_state_response = requests.post(api_gateway_urls + get_current_state_method,
                                               data={'UserID': user_id, 'GameId': game_id, "Token": token})

    def send_post_move_request() -> None:
        global api_gateway_urls, post_move_method
        """mod: this function sends REST API request."""
        nonlocal start_position, next_move, turbo_flag, user_id, game_id, token
        # todo check JSON key names (in APIGateway REST API Description)
        # todo check JSON "Direction" key possible values
        direction = None
        if next_move.row_index > start_position.row_index:
            direction = 'UP'
        elif next_move.row_index < start_position.row_index:
            direction = 'DOWN'
        elif next_move.column_index > start_position.column_index:
            direction = 'RIGHT'
        elif next_move.column_index < start_position.column_index:
            direction = 'LEFT'
        requests.post(api_gateway_urls + post_move_method,
                      data={'Direction': direction, 'UserID': user_id, 'TurboFlag': turbo_flag})

    def send_unregister_user_request() -> None:
        """mod: this function sends REST API request."""
        global api_gateway_urls, unregister_user_method
        nonlocal user_id, token
        # todo check JSON key names (in APIGateway/UserAuthentication REST API Description)
        requests.delete(api_gateway_urls + unregister_user_method,
                        data={'userID': user_id, "token": token})

    def parse_current_state_response() -> None:
        """mod: this function parses REST API response."""
        nonlocal current_state_response, current_map, path_finder, start_position, game_status_flag, user_id
        # todo check JSON key names (in APIGateway and GameEngine REST API Description)
        # todo add parsing logic
        game_state = json.loads(current_state_response.form.get('data'))

        time_elapsed = None
        current_map.map_scheme['height'] = game_state['map']['height']
        current_map.map_scheme['width'] = game_state['map']['width']
        current_map.obstacles_positions = game_state['map']['obstacles']
        current_map.bots_positions = game_state['map']['power-ups']
        current_map.traces_positions = game_state['map']['tracers']
        path_finder.tron_map = current_map

        players_positions = list()
        for player in game_state['players']:
            if player['id'] == user_id:
                start_position = player['headPosition']
                path_finder.start_position = start_position
                path_finder.turbos_number = player['turboAmount']
                time_elapsed = player["timeElapsed"]
            else:
                players_positions.append(player['headPosition'])
        current_map.players_positions = players_positions
        if not time_elapsed:
            game_status_flag = False
        elif time_elapsed > 500:
            path_finder.algorithm = 'Random'
        elif time_elapsed > 100:
            path_finder.algorithm = 'Survival'
        else:
            path_finder.algorithm = 'A*'

    while True:
        send_current_state_request()
        parse_current_state_response()
        if not game_status_flag:
            send_unregister_user_request()
            return
        try:
            next_move, turbo_flag = path_finder.get_direction()
            send_post_move_request()
        except NoSolution:
            continue


if __name__ == '__main__':
    app.run(debug=True)
