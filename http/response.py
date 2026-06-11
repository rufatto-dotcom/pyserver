class Response:
    def __init__(self, body, status=200, content_type=None, headers=None):
        self.body = body
        self.status = status
        self.content_type = content_type
        self.headers = dict(headers or {})
        
        if content_type:
            self.headers["Content-Type"] = content_type