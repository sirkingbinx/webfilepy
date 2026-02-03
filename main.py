from flask import Flask, redirect, render_template, request, send_file, Response
import pathlib

server = Flask(__name__)

@server.route('/', defaults={'path': ''})
@server.route('/<path:path>')
def view_file(path):
    if not pathlib.Path(path).exists():
        return Response("404 Not Found", status=404, mimetype="text/plain")
    
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