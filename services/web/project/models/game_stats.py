from sqlalchemy.sql import func

from project import db


class GameStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    result = db.Column(db.String(10))  # win, lose, draw
    play_time = db.Column(db.Float)  # time in seconds
    endedAt = db.Column(db.DateTime(timezone=True),
                        server_default=func.now())  # date and time at the moment of creation

    def __init__(self, player_id: int, game_id: int, result: str, play_time: float):
        self.player_id = player_id
        self.game_id = game_id

        if result.lower() not in ['win', 'lose', 'draw']:
            raise ValueError('Invalid value for result. Expected one of: win, lose, draw')

        self.result = result
        self.play_time = play_time
