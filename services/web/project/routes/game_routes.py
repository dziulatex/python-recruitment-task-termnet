from flask import Blueprint, render_template

from project.services.game_service import create_game
from project.services.player_service import get_player

bp = Blueprint('game', __name__)


@bp.route('/create_game/<int:player_id>', methods=['POST'])
def create_game_route(player_id):
    game = create_game(player_id)
    if game is None:
        return {'message': 'Not enough credits, or player doesnt exists'}, 400
    return game.to_dict(), 200


@bp.route('/play/<int:player_id>')
def play_game_route(player_id):
    player = get_player(player_id)
    if player is None:
        return render_template("tic_tac_toe.html", player="", credits="", error="Player doesnt exist")
    return render_template("tic_tac_toe.html", player=player_id, credits=player.credits, error="")
