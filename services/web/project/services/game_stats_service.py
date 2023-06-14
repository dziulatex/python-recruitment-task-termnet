from datetime import datetime

from sqlalchemy import func

from .. import db
from ..models.game_stats import GameStats


def count_results(player_id: int, date: datetime.date):
    # Get start and end of the day
    start_of_day = datetime.combine(date, datetime.min.time())
    end_of_day = datetime.combine(date, datetime.max.time())

    results = (db.session.query(GameStats.result, func.count(GameStats.result))
               .filter_by(player_id=player_id)
               .filter(GameStats.endedAt.between(start_of_day, end_of_day))
               .group_by(GameStats.result)
               .all())

    counts = {"wins": 0, "draws": 0, "loses": 0}
    for result, count in results:
        if result == 'win':
            counts['wins'] = count
        elif result == 'draw':
            counts['draws'] = count
        elif result == 'lose':
            counts['loses'] = count

    return counts


def save(game_stats: GameStats):
    db.session.add(game_stats)
    db.session.commit()
