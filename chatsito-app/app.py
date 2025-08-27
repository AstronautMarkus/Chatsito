import os
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*')

mysql_config = {
    'host': os.getenv('MYSQL_HOST'),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DATABASE')
}

def get_db_connection():
    return mysql.connector.connect(**mysql_config)

@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('join')
def handle_join(data):
    username = data['username']
    ip = request.remote_addr
    room = 'main'
    join_room(room)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, ip) VALUES (%s, %s)", (username, ip))
        conn.commit()

        cursor.execute("SELECT username, message, created_at FROM messages ORDER BY created_at ASC LIMIT 50")
        messages = cursor.fetchall()
        cursor.close()
        conn.close()
        for user, msg, created in messages:
            emit('message', {'username': user, 'msg': msg})
    except Exception as e:
        print(f"Error guardando usuario o cargando mensajes: {e}")
    emit('message', {'username': username, 'msg': f'se ha unido al chat.'}, room=room)


@socketio.on('typing')
def handle_typing(data):
    username = data.get('username')
    typing = data.get('typing', False)
    emit('typing', {'username': username if typing else ''}, broadcast=True, include_self=False)

@socketio.on('message')
def handle_message(data):
    username = data['username']
    msg = data['msg']
    ip = request.remote_addr
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (username, ip, message) VALUES (%s, %s, %s)", (username, ip, msg))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error guardando mensaje: {e}")
    emit('message', {'username': username, 'msg': msg}, room='main')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
