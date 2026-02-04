# file.py - handles rendering files (text, image & audio)

import flask
import os
import pathlib
from config import Config

def show_file(filepath: pathlib.Path):
    back_url = "/" if filepath.parent == pathlib.Path(Config.root_folder) else os.path.join("/", str(filepath.parent))
    try:
        with open(os.path.join(Config.root_folder, str(filepath)), "r") as file:
            content = "\n".join(file.readlines())

            try:
                raw = flask.request.args.get("raw", False, bool)
                download = flask.request.args.get("download", False, bool)

                if download:
                    return flask.send_file(str(filepath), as_attachment=True)
                
                if raw:
                    return flask.Response(content, status=200, mimetype="text/plain")
            except ValueError:
                print("Bad value for raw/download param, ignoring..")
            
            return flask.render_template("file.html", back_url=back_url, filename=str(filepath), filecontent=content)
    except UnicodeDecodeError:
        try:
            raw = flask.request.args.get("raw", False, bool)
            download = flask.request.args.get("download", False, bool)
        
            if download or raw:
                return flask.send_file(str(filepath), as_attachment=True)
        except ValueError:
            print("Bad value for raw/download param, ignoring..")

        return flask.render_template("file.html", back_url=back_url, filename=str(filepath), filecontent="The file you're requesting isn't a text file, so we can't preview it here.")