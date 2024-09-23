from flask import Flask

server = Flask(__name__)

@server.route("/hi", methods=["GET"])
def hello():
    return "Hello World!"


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)