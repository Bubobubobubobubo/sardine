import os
import logging

from flask import Flask, send_from_directory, request, Response, jsonify
from pygtail import Pygtail
from flask_cors import CORS
from pathlib import Path
from rich import print
from appdirs import *


APP_NAME, APP_AUTHOR = "Sardine", "Bubobubobubo"
USER_DIR = Path(user_data_dir(APP_NAME, APP_AUTHOR))
LOG_FILE = USER_DIR / "sardine.log"

__all__ = ("WebServer",)

class WebServer():

    """
    This is a small Flask WebServer serving the Sardine Code Editor. This
    web server is also charged of loading / dispatching locally stored
    buffer files that act as a temporary memory for the editor. Files are
    stored in plain-text in the Sardine configuration folder under the buffers/
    folder.
    """

    def __init__(self, host="localhost", port=5000):
        self.host, self.port = host, port
        self.local_files = self.load_buffer_files(
            path=USER_DIR / "buffers"
        )

    def load_buffer_files(self, path: Path) -> dict:
        """
        Loading buffer files from a local folder. If the folder doesn't 
        exis, this function will automatically create it and load empty 
        files for the first round. If the folder exists, read files in their 
        current state
        """
        buffer_files: dict = {}

        # Creating the folder to store text files if it doesn't exist
        if not os.path.isdir(str(USER_DIR / "buffers")):
            try:
                os.makedirs(str(USER_DIR / "buffers"))
                for filename in range(0, 10):
                    print(f"Creating file {filename}.py.")
                    Path(USER_DIR / "buffers" / f"{filename}.py").touch()
                    buffer_files[filename] = ""
                    return buffer_files
            except FileExistsError or OSError:
                print("[red]Fishery was not able to create web editor files![/red]")
                exit()
        # If it already exists, read files from the folder
        else:
            buffer_folder = Path(USER_DIR / "buffers")
            for file in os.listdir(buffer_folder):
                with open(buffer_folder / file, 'r') as buffer:
                    buffer_files[file] = buffer.read() 
            return buffer_files

    def start(self, console):
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
        print(f"Starting server {self.host} on {self.port}")
        app = server_factory(console)
        app.run(
            host=self.host, 
            port=self.port, 
            use_reloader=False, 
            debug=False
        )

    def start_in_thread(self, console):
        from threading import Thread
        Thread(target=self.start, args=(console,)).start()

    def open_in_browser(self):
        import webbrowser
        print("[red]Opening embedded editor at: [yellow]http://127.0.0.1:5000[/yellow][/red]")
        webbrowser.open(f"http://{self.host}:{self.port}")


def server_factory(console):
    app = Flask(__name__, static_folder='../client/build')
    CORS(app, resources={r"/*": {"origins": "*"}})
    
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

    @app.route('/text_files', methods=['GET'])
    def get_text_files():
        files = {}
        for file_name in os.listdir(USER_DIR / "buffers"):
            if file_name.endswith('.txt'):
                with open(os.path.join(USER_DIR / "buffers", file_name)) as f:
                    files[file_name] = f.read()
        files = jsonify(files)
        files.headers.add('Access-Control-Allow-Origin', '*')
        return Response(files)

    return app


if __name__ == '__main__':
    server_factory().run()