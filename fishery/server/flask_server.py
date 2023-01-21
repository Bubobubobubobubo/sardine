import os
from flask import Flask, send_from_directory, request, Response
from pygtail import Pygtail


from appdirs import *
from pathlib import Path

APP_NAME, APP_AUTHOR = "Sardine", "Bubobubobubo"
USER_DIR = Path(user_data_dir(APP_NAME, APP_AUTHOR))
LOG_FILE = USER_DIR / "sardine.log"

__all__ = ("WebServer",)

class WebServer():
    def __init__(self, host="localhost", port=5000):
        self.host = host
        self.port = port

    def start(self, console):
        import logging
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
        print("Starting server" + str(self.host) + ":" + str(self.port))
        app = server_factory(console)
        app.run(host=self.host, port=self.port, use_reloader=False, debug=False)

    def start_in_thread(self, console):
        from threading import Thread
        Thread(target=self.start, args=(console,)).start()

    def open_in_browser(self):
        import webbrowser
        print("[red]Opening embedded editor at: [yellow]http://127.0.0.1:5000[/yellow][/red]")
        webbrowser.open(f"http://{self.host}:{self.port}")


def server_factory(console):
    app = Flask(__name__, static_folder='../client/build')

    @app.post('/execute')
    def execute():
        code = request.json['code']
        try:
            console.push(code)
            return { 'code': code }
        except Exception as e:
            return { 'error': str(e) }
        
    # Serve React App
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        if path != "" and os.path.exists(app.static_folder + '/' + path):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')


    @app.route('/log')
    def progress_log():
        def generate():
            for line in Pygtail(str(LOG_FILE), every_n=0.01):
                yield "data:" + str(line) + "\n\n"
        return Response(generate(), mimetype= 'text/event-stream')
    
    return app

    
if __name__ == '__main__':
    server_factory().run()
