import json

class responseWriter:
    status_messages = {
    200: "OK",
    302: "Found",
    404: "Not Found",
    500: "Internal Server Error"
    }
    
    @classmethod
    def build(cls, response):
        body = response.body
        
        if isinstance(body, (dict, list)):
            body = json.dumps(body).encode()
            response.headers["Content-Type"] = "application/json"

        elif isinstance(body, str):
            body = body.encode() 

        headers = [
            f"HTTP/1.1 {response.status} {cls.status_messages.get(response.status,'')}"
        ]

        for k, v in response.headers.items():
            if k.lower() == "status":
                continue
            headers.append(f"{k}: {v}")

        headers.append(f"Content-Length: {len(body)}")
        headers.append("Connection: close")

        raw = "\r\n".join(headers).encode() + b"\r\n\r\n" + body
        
        return raw