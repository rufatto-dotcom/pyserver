class Request:
    def __init__(self, method, path, protocol, headers, query, raw_query, body, client_ip):
        self.method = method
        self.path = path
        self.protocol = protocol
        self.headers = headers
        self.query = query
        self.raw_query = raw_query
        self.body = body
        self.client_ip = client_ip