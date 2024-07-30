from flask_socketio import emit
from app import socketio

@socketio.on('send_message')
def handle_send_message_event(data):
    from app.models import Message, db
    message = Message(content=data['message'], user_id=data['user_id'])
    db.session.add(message)
    db.session.commit()
    emit('receive_message', {
        'username': data['username'],
        'content': data['message']
    }, broadcast=True)
