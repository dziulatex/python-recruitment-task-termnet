import logging

from flask.cli import FlaskGroup
from flask_migrate import Migrate

logging.basicConfig(level=logging.DEBUG)
from project import create_app, db

app, socketio = create_app()
cli = FlaskGroup(app)
migrate = Migrate(app, db)


@app.cli.command("create_db")
def create_db():
    db.create_all()


if __name__ == '__main__':
    cli()
    socketio.run(app, allow_unsafe_werkzeug=True)  # This line is enough to start the server
