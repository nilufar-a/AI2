"""This module contains AI Bot implementation for TRON game."""
import requests
from threading import Thread
from flask import Flask, request, make_response
from map import Map
from path_finder import PathFinder

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
    user_id = request.form.get('userID')
    game_id = request.form.get('gameID')
    token = request.form.get('token')

    if user_id and game_id and token:
        bot = Thread(target=bot_routine, args=(user_id, game_id, token), daemon=True)
        bot.start()
        return make_response('OK', 200)
    else:
        return make_response('BAD REQUEST', 400)


def bot_routine(user_id, game_id, token) -> None:
    """mod: this function is main function of the module."""
    current_map = Map()
    path_finder = PathFinder()
    next_move = None
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
        nonlocal next_move, user_id, game_id, token
        # todo check JSON key names (in APIGateway REST API Description)
        # todo check JSON "Direction" key possible values
        requests.post(api_gateway_urls + post_move_method,
                      data={'Direction': next_move, 'UserID': user_id, 'TurboFlag': True})

    def send_unregister_user_request() -> None:
        """mod: this function sends REST API request."""
        global api_gateway_urls, unregister_user_method
        nonlocal user_id, token
        # todo check JSON key names (in APIGateway/UserAuthentication REST API Description)
        requests.delete(api_gateway_urls + unregister_user_method,
                        data={'userID': user_id, "token": token})

    def parse_current_state_response() -> None:
        """mod: this function parses REST API response."""
        nonlocal current_state_response, current_map, path_finder, game_status_flag
        # todo check JSON key names (in APIGateway and GameEngine REST API Description)
        # todo add parsing logic
        current_state_response.form.get('data')
        game_status_flag = None
        if game_status_flag:
            current_map.map_scheme = None
            current_map.players_positions = None
            current_map.bots_positions = None
            current_map.turbos_positions = None
            current_map.obstacles_positions = None
            current_map.traces_positions = None

            path_finder.tron_map = current_map
            path_finder.start_position = None
            path_finder.algorithm = None
            path_finder.turbos_number = None

    while True:
        send_current_state_request()
        parse_current_state_response()
        if not game_status_flag:
            send_unregister_user_request()
            return
        next_move = path_finder.get_direction()
        send_post_move_request()


if __name__ == '__main__':
    app.run(debug=True)
