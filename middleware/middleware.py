from server.http.response import Response
from server.http.responseWriter import responseWriter

middlewares = []

def middleware(func):
    middlewares.append(func)
    return func

def run_middlewares(request):
    for middleware in middlewares:
        response = middleware(request)
        
        if response:
            return response

    return None

@middleware
def log_middleware(request):
    print(request.method, request.path)

@middleware
def ip_filter(request):
    allowed = ["127.0.0.1", "192.168.15.4"]

    ip = request.client_ip[0]

    if ip not in allowed:
        return Response("IP não autorizado", 403)

@middleware
def security_middleware(request):
    if ".." in request.path:
        return Response("Forbidden", 403)    