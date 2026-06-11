from server.http.request import Request
from server.http.requestParser import requestParser
from server.http.response import Response
from server.http.responseWriter import responseWriter
from server.middleware.middleware import run_middlewares
from server.routing.router import routers_dinamic, routers_static, serve_static_file

async def handle_client_connection(reader, writer):
    addr = writer.get_extra_info("peername")
    print(f"Handling connection from {addr}")
    try:
        parser = requestParser(reader, addr)
        request = await parser.parse()
        
        if not request:
            return
        
        middleware_response = run_middlewares(request)
        
        if middleware_response:
            response = middleware_response
        else:
            response = handle_request(request)
            
        raw = responseWriter.build(response)
        
        writer.write(raw)
        await writer.drain()
        
    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    except KeyboardInterrupt:
        print(f"Shutting down server")
        
    finally:
        writer.close()
        await writer.wait_closed()
        
def handle_request(request):
    method = request.method
    path = request.path
    
    for route in routers_dinamic.get(method, []):
        match = route["pattern"].match(path)
        
        if match:
            values = match.groups()
            params = dict(zip(route["params"], values))
            request.params = params
            
            handler = route["handler"]
            result = handler(request)
            
            return normalize_response(result)
            
    try:
        func = routers_static.get(method, {}).get(path)
        
        if func:
            result = func(request)
            return normalize_response(result)
        
        static = serve_static_file(path, request)

        if static:
            return static
            
        return Response("404 Not Found", 404)
    except Exception as e:
        print("Server Error: ", e)
        return Response("Internal Server Error", 500)
    
def normalize_response(result):
    if isinstance(result, Response):
        return result

    if isinstance(result, tuple) and len(result) == 3:
        body, status, headers = result

        if isinstance(status, str):
            status = int(status.split()[0])

        return Response(body, status=status, headers=headers)

    return Response(result)