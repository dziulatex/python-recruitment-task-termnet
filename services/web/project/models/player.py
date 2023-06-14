from project import db


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    credits = db.Column(db.Integer, default=10)

    def to_dict(self):
        return {
            'id': self.id,
            'credits': self.credits
        }
