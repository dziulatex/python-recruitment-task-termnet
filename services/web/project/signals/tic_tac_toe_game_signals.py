from datetime import datetime

from blinker import Namespace

from project import redis_store
from project.models.game_stats import GameStats
from project.services import game_service, player_service, game_stats_service
from project.services.game_service import get_game
from project.utils.utils import app_datetime_format

my_signals = Namespace()
tic_tac_toe_won = my_signals.signal('tic_tac_toe_won')
tic_tac_toe_draw = my_signals.signal('tic_tac_toe_draw')
tic_tac_toe_lost = my_signals.signal('tic_tac_toe_lost')


@tic_tac_toe_won.connect
def handle_tic_tac_toe_won(game_id: int):
    game = get_game(game_id)
    game.end_game()
    player = player_service.get_player(game.player_id)

    dateTimeStr = redis_store.get(str(game_id) + '-time')
    dateTime = datetime.strptime(str(dateTimeStr), app_datetime_format)
    midTime = datetime.now() - dateTime
    seconds = midTime.total_seconds()
    gameStats = GameStats(game.player_id, game_id, 'win', seconds)
    game_stats_service.save(gameStats)

    player.credits = player.credits + 4
    game_service.save_game(game)
    player_service.save_player(player)
    redis_store.delete(game_id)
    print("win")


@tic_tac_toe_lost.connect
def handle_tic_tac_toe_lost(game_id: int):
    game = get_game(game_id)
    game.end_game()
    game_service.save_game(game)

    dateTimeStr = redis_store.get(str(game_id) + '-time')
    dateTime = datetime.strptime(str(dateTimeStr), app_datetime_format)
    midTime = datetime.now() - dateTime
    seconds = midTime.total_seconds()
    gameStats = GameStats(game.player_id, game_id, 'lost', seconds)
    game_stats_service.save(gameStats)

    redis_store.delete(game_id)
    print("lost")


@tic_tac_toe_draw.connect
def handle_tic_tac_toe_draw(game_id: int):
    game = get_game(game_id)
    game.end_game()
    game_service.save_game(game)

    dateTimeStr = redis_store.get(str(game_id) + '-time')
    dateTime = datetime.strptime(str(dateTimeStr), app_datetime_format)
    midTime = datetime.now() - dateTime
    seconds = midTime.total_seconds()
    gameStats = GameStats(game.player_id, game_id, 'draw', seconds)
    game_stats_service.save(gameStats)

    redis_store.delete(game_id)
    print("draw")
