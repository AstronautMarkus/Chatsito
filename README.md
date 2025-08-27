# Chatsito

This is a mini real-time chat using Flask and Flask-SocketIO. It allows guests to join and chat on the local network without authentication.

## How to run

1. Make sure you have your virtual environment activated and dependencies installed.
2. Start the server:

```
python app.py
```

3. Open in any browser on your local network:

```
http://<YOUR_PC_IP>:5000
```

Replace `<YOUR_PC_IP>` with your machine's local IP address.

## Notes
- No registration or authentication required.
- All messages are visible in real time to all connected users.
- You can open it from multiple devices on the same network.
