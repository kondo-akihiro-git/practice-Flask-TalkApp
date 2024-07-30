from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Message

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/chat')
@login_required
def chat():
    messages = Message.query.all()
    return render_template('chat.html', username=current_user.username, messages=messages)
