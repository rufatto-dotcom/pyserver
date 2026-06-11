from .request import Request
import asyncio
from urllib.parse import urlparse, parse_qs
import json

class requestParser:
    def __init__(self, reader, addr):
        self.reader = reader
        self.addr = addr
        
    async def parse(self):
        data = b""

        while b"\r\n\r\n" not in data:
            chunk = await self.reader.read(1024)
            if not chunk:
                return None
            data += chunk

        headers_part, body_part = data.split(b"\r\n\r\n", 1)
        headers_lines = headers_part.decode().split("\r\n")

        request_lines = headers_lines[0]
        method, raw_path, protocol = request_lines.split(" ")

        headers = {}

        for line in headers_lines[1:]:
            if ": " in line:
                key, value = line.split(": ", 1)
                headers[key.lower()] = value

        content_length = int(headers.get("content-length", 0))

        while len(body_part) < content_length:
            chunk = await self.reader.read(1024)
            if not chunk:
                break
            body_part += chunk
            
        body = body_part.decode()
        body = self.parse_body(headers, body)
        
        parsed_url = urlparse(raw_path)
        
        return Request(
            method=method,
            path=parsed_url.path,
            protocol=protocol,
            headers=headers,
            query=parse_qs(parsed_url.query),
            raw_query=parsed_url.query,
            body=body,
            client_ip=self.addr
        )
    
    def parse_request(self, method, raw_path, protocol, headers, body, addr):
        parsed_url = urlparse(raw_path)

        path = parsed_url.path
        query = parse_qs(parsed_url.query)

        body = self.parse_body(headers, body)

        return {
            "method": method,
            "path": path,
            "protocol": protocol,
            "headers": headers,
            "query": query,
            "body": body,
            "client_ip": addr
        }
        
    def parse_body(self, headers, body):
        content_type = headers.get("content-type", "")

        if "application/json" in content_type and body:
            return json.loads(body)
        
        if "application/x-www-form-urlencoded" in content_type:
            data = parse_qs(body)
            return {key: value[0] for key, value in data.items()}
        
        return body