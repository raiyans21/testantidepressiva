from flask import Blueprint, render_template
from flask_login import login_required
from datetime import datetime
from extensions import socketio  # Importiere SocketIO
from flask_socketio import emit

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/')
@login_required
def chat():
    return render_template('chat.html')

# SocketIO-Events
@socketio.on('send_message')
def handle_send_message(data):
    username = data.get('username')
    message = data.get('msg')
    color = data.get('color')
    reply_to = data.get('replyTo')
    timestamp = datetime.now().strftime('%H:%M')

    # Sende Nachricht an alle verbundenen Clients
    emit('receive_message', {
        'msg': message,
        'username': username,
        'time': timestamp,
        'color': color,
        'replyTo': reply_to
    }, broadcast=True)

# Reply-Funktion
@socketio.on('reply_message')
def handle_reply_message(data):
    username = data.get('username')
    reply_content = data.get('reply')
    message_id = data.get('message_id')
    timestamp = datetime.now().strftime('%H:%M')

    # Sende Antwort an alle Clients
    emit('reply_message', {
        'username': username,
        'reply': reply_content,
        'message_id': message_id,
        'time': timestamp
    }, broadcast=True)

# Delete-Funktion
@socketio.on('delete_message')
def handle_delete_message(data):
    message_id = data.get('message_id')

    # Sende Löschanfrage an alle Clients
    emit('delete_message', {'message_id': message_id}, broadcast=True)

# Bearbeiten-Funktion
@socketio.on('edit_message')
def handle_edit_message(data):
    message_id = data.get('message_id')
    new_content = data.get('new_content')

    # Sende bearbeitete Nachricht an alle Clients
    emit('edit_message', {
        'message_id': message_id,
        'new_content': new_content
    }, broadcast=True)

# Emoji-Reaktionen
@socketio.on('react_message')
def handle_react_message(data):
    message_id = data.get('message_id')
    emoji = data.get('emoji')
    username = data.get('username')

    # Sende Reaktion an alle Clients
    emit('react_message', {
        'message_id': message_id,
        'emoji': emoji,
        'username': username
    }, broadcast=True)
