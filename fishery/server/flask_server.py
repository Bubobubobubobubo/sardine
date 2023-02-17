from flask import Flask, send_from_directory, request, Response, jsonify
from pygtail import Pygtail
from typing import Optional
from flask_cors import CORS
from pathlib import Path
from rich import print
from appdirs import *
import logging
import os

# Monkey-patching to prevent some initial printing
# More info can be found here: https://gist.github.com/daryltucker/e40c59a267ea75db12b1
import flask.cli    
flask.cli.show_server_banner = lambda *args: None
logging.getLogger("werkzeug").disabled = True



APP_NAME, APP_AUTHOR = "Sardine", "Bubobubobubo"
USER_DIR = Path(user_data_dir(APP_NAME, APP_AUTHOR))
LOG_FILE = USER_DIR / "sardine.log"
FILENAMES = [
        "0.py", "1.py", "2.py", "3.py",
        "4.py", "5.py", "6.py", "7.py",
        "8.py", "9.py", "10.py",
]

# We need to create the log file if it doesn't already exist
Path(LOG_FILE).touch(exist_ok=True)

__all__ = ("WebServer",)

class WebServer():

    """
    This is a small Flask WebServer serving the Sardine Code Editor. This web server is
    also charged of loading / dispatching locally stored buffer files that act as a
    temporary memory for the editor. Files are stored in plain-text in the Sardine conf-
    iguration folder under the buffers/folder.
    """

    def __init__(self, host="localhost", port=8000):
        self.host, self.port = host, port
        self.local_files = self.load_buffer_files()


    def check_buffer_files(self) -> None:
        """This function will check the integrity of the buffer folder.""" 
        buffer_folder: Path = Path(USER_DIR / "buffers")
        for filename in FILENAMES:
            check_file: Path = buffer_folder / filename
            if not check_file.exists():
                print(f'Creating file {str(filename)}!')
                Path(check_file).touch()
            else:
                print(f'Loading file {str(filename)}')


    def load_buffer_files(self) -> Optional[dict]:
        """
        Loading buffer files from a local folder. If the folder doesn't exist, this 
        function will automatically create it and load empty files for the first round. 
        If the folder exists, read files in their current state
        """
        buffer_files: dict = {}

        # Creating the folder to store text files if it doesn't exist
        if not (USER_DIR / "buffers").is_dir():
            try:
                (USER_DIR / "buffers").mkdir()
                for filename in list(range(0, 10)):
                    print(f"Creating file {filename}.py.")
                    Path(USER_DIR / "buffers" / f"{filename}.py").touch()
                    buffer_files[filename] = ""
                    return buffer_files
            except FileExistsError or OSError:
                print("[red]Fishery was not able to create web editor files![/red]")
                exit()
        # If it already exists, read files from the folder
        else:
            self.check_buffer_files()
            buffer_folder = Path(USER_DIR / "buffers")
            for file in os.listdir(buffer_folder):
                with open((buffer_folder / file).as_posix(), 'r') as buffer:
                    buffer_files[file] = buffer.read()
            return buffer_files

    def start(self, console):

        app = server_factory(console)

        # Start the application
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
    app.logger.disabled = True  # Disable some of the logging
    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.post('/open_folder')
    def open_folder():
        """Open Sardine Default Folder using the default file Explorer"""
        import platform
        def showFileExplorer(file):  # Path to file (string)
            if platform.system() == "Windows":
                import os
                os.startfile(file)
            elif platform.system() == "Darwin":
                import subprocess
                subprocess.call(["open", "-R", file])
            else:
                import subprocess
                subprocess.Popen(["xdg-open", file])

        # Open the file explorer
        showFileExplorer(str(USER_DIR))

        return "OK"
    
    @app.post('/execute')
    def execute():
        code = request.json['code']
        try:
            console.push(code)
            return { 'code': code }
        except Exception as e:
            return { 'error': str(e) }
        
    # Serve App
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
            for line in Pygtail(str(LOG_FILE), every_n=2):
                yield "data:" + str(line) + "\n\n"
        return Response(generate(), mimetype= 'text/event-stream')

    @app.route('/text_files', methods=['GET'])
    def get_text_files():
        files = {}
        for file_name in os.listdir(USER_DIR / "buffers"):
            if file_name.endswith('.py'):
                buffer_directory = USER_DIR / "buffers"
                with open((buffer_directory / file_name).as_posix(), 'r') as f:
                    files[file_name] = f.read()
        files = jsonify(files)
        print(files)
        files.headers.add('Access-Control-Allow-Origin', '*')
        return files

    @app.route('/save', methods=['POST'])
    def save_files_to_disk() -> str:
        data = request.get_json(silent=True)

        if data:
            # Iterating over the dictionary we just received and dispatching to text files :)
            for key, content in data.items():
                # We need to strip the key first because it is formatted in a weird way.
                key = ''.join(c for c in key if c not in "[]")
                # Writing the file itself
                with open(USER_DIR / "buffers" / f"{key}.py", 'w') as new_file:
                    new_file.write(content)
            return "OK"
        else:
            return "FAILED"

    return app


if __name__ == '__main__':
    server_factory().run(debug=False)
