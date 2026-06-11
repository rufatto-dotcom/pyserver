import re
from server.runtime.php import execute_php
import os
from server.http.response import Response

routers_static = {
    "GET": {},
    "POST": {},
}

routers_dinamic = {
    "GET": [],
    "POST": [],
}

def get(path):
    def decorator(func):
        params = []
        if ":" in path:
            params = re.findall(r":(\w+)", path)
            pattern = re.sub(r":\w+", r"([^/]+)", path)
            pattern = "^" + pattern + "$"
            pattern = re.compile(pattern)
            routers_dinamic["GET"].append({
                "pattern": pattern,
                "params": params,
                "handler": func
            })
        else:
            routers_static["GET"][path] = func
            
        return func
    return decorator

def post(path):
    def decorator(func):
        params = []
        if ":" in path:
            params = re.findall(r":(\w+)", path)
            pattern = re.sub(r":\w+", r"([^/]+)", path)
            pattern = "^" + pattern + "$"
            pattern = re.compile(pattern)
            routers_dinamic["POST"].append({
                "pattern": pattern,
                "params": params,
                "handler": func
            })
        else:
            routers_static["POST"][path] = func
            
        return func
    return decorator

ROOT = "."

def serve_static_file(path, request):
    if path == "/":
        path = "/index.php"
        
    file_path = ROOT + path
    
    if os.path.isdir(file_path):
        file_path = os.path.join(file_path, "index.php")
    
    if not os.path.exists(file_path):
        return Response(
            body="Not Found",
            status=404,
            headers={"Content-Type": "text/plain"}
        )
    
    if file_path.endswith(".php"):
        return execute_php(file_path, request)
    
    extension = file_path.rpartition(".")[-1].lower()
    
    mime_types = {
        "html": "text/html",
        "css": "text/css",
        "js": "application/javascript",
        "png": "image/png",
        "jpg": "image/jpeg",
        "ico": "image/x-icon"
    }
    
    content_type = mime_types.get(extension, "application/octet-stream")
    
    with open(file_path, "rb") as f:
        content = f.read()
        
    return Response(
        body=content,
        status=200,
        headers={
            "Content-Type": content_type
        }
    )