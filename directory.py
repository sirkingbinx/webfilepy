# directory.py - handles rendering directories

import flask
import os
import pathlib
from datetime import datetime
from config import Config

def show_dir(path: pathlib.Path):
    items_html = []
    dir_top = 0

    if str(path) != ".":
        items_html.append({
            "name": "Back",
            "modified": "---",
            "link": "/" if path.parent == pathlib.Path(Config.root_folder) else os.path.join("/", str(path.parent)),
            "dir": False,
            "back": True
        })

    for item in path.iterdir():
        last_modified = datetime.fromtimestamp(os.path.getmtime(item.resolve(True)))
        data = {
            "name": item.name,
            "modified": last_modified.strftime("%Y-%m-%d %H:%M"),
            "link": str(os.path.join("/", path, item.name)),
            "dir": item.is_dir(),
            "back": False
        }

        if data["dir"]:
            items_html.insert(dir_top + 1, data)
            dir_top = items_html.index(data)
        else:
            items_html.append(data)

    return flask.render_template("directory.html", dirname=f"{str(path) if str(path) != "." else "/ (root)"}", items=items_html)