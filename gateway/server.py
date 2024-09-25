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

    public_key_string = "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4/6XAdTngp/ndMMpH4A6\niVb10gKOPhYF6kMMHugEoW1oUYH66DPiw5DELm7VMjI/G2Yjz4XmubUMb1Asx/u/\nDF3lGMe3I2+EHUlOR61Bu5luMO0ADoSixf74fi6ytiUijyiBUclTgpAxbcJ3P1D6\nVahZwKbdqUvmXbM2JzGyctBIUp+zLZk0NzuKKHcElB5HTt+hW/PhwtQwJT5mt03F\nQsKxzMM9i4upSCcH4jCuOrYEepxelw6el1yBgPuCiS5qDBpLEMU2JN40tEahxC9y\n36F7OPKt17EZk1bhp9pfndf4yCGzHw6dp5l4hZOvwZ6vkAbftZWsecIwRpfSiue5\nuwIDAQAB\n-----END PUBLIC KEY-----\n"

    public_key_bytes = bytes(public_key_string, 'utf-8')
    return public_key_bytes
    # public_key_string.encode('utf-8')
    # response = make_response({
    #     "@context": [
    #         "https://www.w3.org/ns/activitystreams",
    #         "https://w3id.org/security/v1",
    #     ],
    #     "id": "https://eduard/users/zampano",
    #     "inbox": "https://eduard/users/zampano/inbox",
    #     "outbox": "https://eduard/users/zampano/outbox",
    #     "type": "Person",
    #     "name": "Zampano",
    #     "preferredUsername": "zampano",
    #     "publicKey": {
    #         "id": "https://eduard/users/zampano#main-key",
    #         "id": "https://eduard/users/zampano",
    #         "publicKeyPem": public_key_bytes
    #     }
    # })

    # # Servers may discard the result if you do not set the appropriate content type
    # response.headers['Content-Type'] = 'application/activity+json'

    # return response

@server.route('/.well-known/webfinger')
def webfinger():
    resource = request.args.get('resource')

    if resource != "acct:zampano@eduard":
        abort(404)

    response = make_response({
        "subject": "acct:zampano@eduard",
        "links": [
            {
                "rel": "self",
                "type": "application/activity+json",
                "href": "https://eduard/users/zampano"
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