import flask
import pathlib
import os
import sys

from config import Config

# Views
import file
import directory

root_dir = sys.argv[1] if len(sys.argv) > 1 else ""
port = int(sys.argv[2]) if len(sys.argv) > 2 else 5000

Config.root_folder = root_dir
Config.port = port

server = flask.Flask(__name__)

@server.route('/', defaults={'path': ''})
@server.route('/<path:path>')
def view(path: str):
    adv_path = pathlib.Path(os.path.join(root_dir, path))
    
    # 404
    if not adv_path.exists():
        return flask.Response("404 Not Found", status=404, mimetype="text/plain")
    
    if path == "" or adv_path.is_dir():
        # Directory
        return directory.show_dir(adv_path)
    else:
        # File
        return file.show_file(adv_path)

server.run(port=Config.port, debug=False)