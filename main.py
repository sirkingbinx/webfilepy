from flask import Flask, redirect, render_template, request, send_file, Response
import pathlib
import os
import datetime

server = Flask(__name__)

@server.route('/', defaults={'path': ''})
@server.route('/<path:path>')
def view_file(path):
    realpath = pathlib.Path(path)

    if not realpath.exists():
        return Response("404 Not Found", status=404, mimetype="text/plain")
    
    if path == "" or realpath.is_dir():
        items_html = []
        dir_top = 0

        if path != "":
            items_html.append({
                "name": "Back",
                "modified": "---",
                "link": str(os.path.join("/", str(realpath.parent))),
                "dir": False,
                "back": True
            })

        for item in realpath.iterdir():
            last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(item.resolve(True)))
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

        return render_template("directory.html", dirname=f"/{path}", items=items_html)
    
    try:
        with open(path, "r") as file:
            content = "\n".join(file.readlines())

            try:
                raw = request.args.get("raw", False, bool)
                download = request.args.get("download", False, bool)

                if download:
                    return send_file(path, as_attachment=True)
                
                if raw:
                    return Response(content, status=200, mimetype="text/plain")
            except ValueError:
                print("Bad value for raw/download param, ignoring..")
            
            return render_template("file.html", filename=path, filecontent=content)
    except UnicodeDecodeError:
        try:
            raw = request.args.get("raw", False, bool)
            download = request.args.get("download", False, bool)
        
            if download or raw:
                return send_file(path, as_attachment=True)
        except ValueError:
            print("Bad value for raw/download param, ignoring..")

        return render_template("file.html", filename=path, filecontent="The file you're requesting isn't a text file, so we can't preview it here.")

server.run()