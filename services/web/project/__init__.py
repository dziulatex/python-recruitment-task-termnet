import redis
from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

# initialize database
db = SQLAlchemy()
socketio = SocketIO()

# initialize Redis
redis_store = redis.Redis(host='cache', port=6379, db=0, password='random', charset="utf-8", decode_responses=True)


def create_app():
    app = Flask(__name__)
    app.config.from_object("project.config.Config")

    db.init_app(app)

    # Register blueprints
    from .routes import player_routes, game_routes
    app.register_blueprint(player_routes.bp)
    app.register_blueprint(game_routes.bp)
    from .routes import game_socket
    socketio.init_app(app, logger=True, engineio_logger=True)
    return app, socketio
