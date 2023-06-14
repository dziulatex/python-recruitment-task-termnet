from datetime import datetime

from flask_socketio import emit
from flask_socketio import join_room

from project import socketio, redis_store
from project.services.game_service import get_game
from project.signals.tic_tac_toe_game_signals import tic_tac_toe_draw, tic_tac_toe_won, tic_tac_toe_lost
from project.tic_tac_toe import TicTacToe
from project.utils.utils import app_datetime_format


@socketio.on('message')
def on_join(data):
    gameId = data['game_id']
    print("mess")
    join_room(gameId)


@socketio.on('join')
def on_connect(data):
    game = get_game(data['game_id'])
    if redis_store.get(data['game_id']) is None:
        board = TicTacToe()
        redis_store.set(data['game_id'], board.to_json())
        redis_store.set(str(data['game_id']) + '-time', datetime.now().strftime(app_datetime_format))
        print('set_board')


@socketio.on('move')
def handle_move(data):
    board_json = redis_store.get(data['game_id'])
    if board_json is not None:
        row = data['row']
        col = data['col']
        board = TicTacToe()
        board.from_json(board_json)
        board.fix_spot(int(row), int(col), 0)
        if board.is_player_win(0):
            emit('win', {'winner': 0})
            tic_tac_toe_won.send(data['game_id'])
            return
        if board.is_board_filled():
            emit('draw')
            tic_tac_toe_draw.send(data['game_id'])
            return
        fixedByBot = board.random_fix_spot(1)
        if board.is_player_win(1):
            emit('move', {'row': fixedByBot[0], 'col': fixedByBot[1], 'game_id': data['game_id']})
            emit('win', {'winner': 1})
            tic_tac_toe_lost.send(data['game_id'])
            return
        if board.is_board_filled():
            emit('draw')
            tic_tac_toe_draw.send(data['game_id'])
            return
        redis_store.set(data['game_id'], board.to_json())
        emit('move', {'row': fixedByBot[0], 'col': fixedByBot[1], 'game_id': data['game_id']})


@socketio.on('connect')
def handle_connect(data):
    print('conn')
