from flask import Flask, request, jsonify, Response, json, render_template
app = Flask(__name__)


def test_tiles():
    return render_template("index.html")

app.add_url_rule('/','/', test_tiles, methods=['GET'])

if __name__ == "__main__":
    app.run(debug=True)