import os
from flask import Flask, abort, request, make_response, Response

server = Flask(__name__)

@server.route("/hi", methods=["GET"])
def hello():
    return "Hello World!"

@server.route('/users/<username>')
def user(username):
    if username != "zampano":
        abort(404)

    public_key_string = os.environ.get('PUBLIC_KEY')

    public_key_bytes = public_key_string.encode('utf-8')

    response = make_response({
        "@context": [
            "https://www.w3.org/ns/activitystreams",
            "https://w3id.org/security/v1",
        ],
        "id": "https://example.com/users/zampano",
        "inbox": "https://example.com/users/zampano/inbox",
        "outbox": "https://example.com/users/zampano/outbox",
        "type": "Person",
        "name": "Zampano",
        "preferredUsername": "zampano",
        "publicKey": {
            "id": "https://example.com/users/zampano#main-key",
            "id": "https://example.com/users/zampano",
            "publicKeyPem": public_key_bytes
        }
    })

    # Servers may discard the result if you do not set the appropriate content type
    response.headers['Content-Type'] = 'application/activity+json'

    return response

@server.route('/.well-known/webfinger')
def webfinger():
    resource = request.args.get('resource')

    if resource != "acct:zampano@example.com":
        abort(404)

    response = make_response({
        "subject": "acct:zampano@example.com",
        "links": [
            {
                "rel": "self",
                "type": "application/activity+json",
                "href": "https://example.com/users/zampano"
            }
        ]
    })

    # Servers may discard the result if you do not set the appropriate content type
    response.headers['Content-Type'] = 'application/jrd+json'
    
    return response

@server.route('/users/<username>/inbox', methods=['POST'])
def user_inbox(username):
    if username != "zampano":
        abort(404)

    server.logger.info(request.headers)
    server.logger.info(request.data)
    
    return Response("", status=202)


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)