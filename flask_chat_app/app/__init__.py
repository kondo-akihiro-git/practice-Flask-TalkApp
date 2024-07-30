from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_socketio import SocketIO

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
socketio = SocketIO()

@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    socketio.init_app(app)

    with app.app_context():
        from . import routes, auth, models

    app.register_blueprint(routes.main)
    app.register_blueprint(auth.auth)

    from .events import handle_send_message_event  # 追加

    return app

# events.py ファイルを新しく作成し、イベントハンドラを定義します
def handle_send_message_event(data):
    from app.models import Message, db
    message = Message(content=data['message'], user_id=data['user_id'])
    db.session.add(message)
    db.session.commit()
    emit('receive_message', {
        'username': data['username'],
        'content': data['message']
    }, broadcast=True)
