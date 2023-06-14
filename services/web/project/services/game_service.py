from .. import db
from ..models.game import Game
from ..models.player import Player


def create_game(player_id) -> Game | None:
    player = Player.query.get(player_id)
    if player is None:
        return None
    if player.credits < 3:
        return None

    player.credits -= 3
    game = Game(player_id=player_id)

    db.session.add(game)
    db.session.commit()

    return game


def save_game(game: Game):
    db.session.add(game)
    db.session.commit()


def get_game(game_id) -> Game | None:
    game = Game.query.get(game_id)
    return game
