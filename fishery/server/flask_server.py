import os
from flask import Flask, send_from_directory, request
from flask_socketio import SocketIO, emit, send




__all__ = ("Server",)


class Server:
    def __init__(self, console):
        app = Flask(__name__, static_folder='../client/build')
        self.app = app;
        socketio = SocketIO(app, cors_allowed_origins='*')
        self.socketio = socketio;

        @app.post('/execute')
        def execute():
            code = request.json['code']
            try:
                console.push(code)
                return { 'code': code }
            except Exception as e:
                return { 'error': str(e) }
            
        @socketio.on('execute')
        def live_execute(json):
            code = json['code']
            try:
                console.push(code)
                emit('executed', { 'code': code })
            except Exception as e:
                emit( 'error', { 'error': str(e) } )

        @socketio.on('ping')
        def ping():
            emit('pong', { 'data': 'pong' })

        # Serve React App
        @app.route('/', defaults={'path': ''})
        @app.route('/<path:path>')
        def serve(path):
            if path != "" and os.path.exists(app.static_folder + '/' + path):
                return send_from_directory(app.static_folder, path)
            else:
                return send_from_directory(app.static_folder, 'index.html')

    def broadcast(self, event, data):
        self.socketio.emit(event, data)
        pass
    
if __name__ == '__main__':
    # app.run(use_reloader=True, port=3000, threaded=True)
    pass
