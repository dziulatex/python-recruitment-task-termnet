from .. import db
from ..models.player import Player


def add_credits(player_id: int, amount: int):
    player = Player.query.get(player_id)
    if player.credits == 0:
        player.credits += amount
        db.session.commit()


def create_player() -> Player:
    player = Player()
    return player


def save_player(player):
    db.session.add(player)
    db.session.commit()


def get_player(player_id) -> Player | None:
    player = Player.query.get(player_id)
    return player
