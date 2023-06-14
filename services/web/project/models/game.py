from project import db


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    state = db.Column(db.String(9), default='started')

    def to_dict(self):
        return {
            'id': self.id,
            'state': self.state,
            'player_id': self.player_id
        }

    def end_game(self):
        self.state = 'ended'
