from datetime import date

from flask import Blueprint

from project.services.game_stats_service import count_results
from project.services.player_service import add_credits, create_player, save_player, get_player

bp = Blueprint('player', __name__)


@bp.route('/add_credits/<int:player_id>', methods=['POST'])
def add_credits_route(player_id):
    add_credits(player_id, 10)
    return {'message': 'Credits added.'}, 200


@bp.route('/create_player', methods=['POST', 'GET'])
def create_player_route():
    player = create_player()
    save_player(player)
    return player.to_dict(), 201


@bp.route('/get_player/<int:player_id>', methods=['GET'])
def get_player_route(player_id):
    player = get_player(player_id)
    if player is None:
        return {'message': 'Player doesnt exists'}, 400
    return player.to_dict(), 200


@bp.route('/get_player_stats_for_today/<int:player_id>', methods=['GET'])
def get_player_stats_for_today_route(player_id):
    player = get_player(player_id)
    if player is None:
        return {'message': 'Player doesnt exists'}, 400
    player_stats = count_results(player_id, date.today())
    return player_stats, 200
