import json

from middleware.JWT import JWT

class AuthMiddleware:

    ignoreProcessRequestForPaths = ["/signup", "/login"]

    def __init__(self):
        self.jwt = JWT()

    def process_request(self, req, resp):
        """Process the request before routing it.
        Note:
            Because Falcon routes each request based on req.path, a
            request can be effectively re-routed by setting that
            attribute to a new value from within process_request().
        Args:
            req: Request object that will eventually be
                routed to an on_* responder method.
            resp: Response object that will be routed to
                the on_* responder.
        """
        if req.method != "OPTIONS" and req.path not in AuthMiddleware.ignoreProcessRequestForPaths:
            if req.headers["AUTHORIZATION"]:
                decoded_jwt = self.jwt.decode(req.headers["AUTHORIZATION"].split()[1])
                if not decoded_jwt:
                    resp.body = json.dumps({
                        "responseId": 101,
                        "message": "token expired"
                    })
                    resp.complete = True
                else:
                    req.params["userId"] = decoded_jwt["returnData"]["_id"]["$oid"]

    def process_response(self, req, resp, resource, req_succeeded):
        """Post-processing of the response (after routing).
        Args:
            req: Request object.
            resp: Response object.
            resource: Resource object to which the request was
                routed. May be None if no route was found
                for the request.
            req_succeeded: True if no exceptions were raised while
                the framework processed and routed the request;
                otherwise False.
        """
        if req.method == "GET" and req.path == "/fast-forward":
            if req.headers["AUTHORIZATION"]:
                decoded_jwt = self.jwt.decode(req.headers["AUTHORIZATION"].split()[1])
                if not decoded_jwt:
                    resp.body = json.dumps({
                        "responseId": 101,
                        "message": "token expired"
                    })
                else:
                    resp.body = json.dumps(decoded_jwt)
        elif req_succeeded and req.method != "OPTIONS" and req.path == "/login":
            respBody = json.loads(resp.body)
            _id = respBody["returnData"]["_id"]["$oid"]
            encoded_jwt = self.jwt.encode(respBody).decode("utf-8")
            respBody["token"] = encoded_jwt
            resp.body = json.dumps(respBody)
