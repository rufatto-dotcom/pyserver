from server.routing.router import get, post
from server.http.response import Response
from pyntaho.main import receive_data

@get("/teste")
def burro(request):
    return "ta no GET"

@get("/users/:id")
def user(request):
    return f"user {request.params['id']}"
    