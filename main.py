from flask import Flask, render_template

server = Flask(__name__)

@server.route("/")
def home():
    return render_template("file.html", filename="hello.txt", filecontent="hello world!")

server.run(debug=True)