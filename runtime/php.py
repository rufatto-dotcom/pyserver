import subprocess
import os
import urllib.parse
from server.http.response import Response

def execute_php(file_path, request):
    env = os.environ.copy()

    env.update({
        "REQUEST_METHOD": request.method,
        "SCRIPT_FILENAME": file_path,
        "SCRIPT_NAME": request.path,
        "QUERY_STRING": request.raw_query,
        "REQUEST_URI": request.path + ("?" + request.raw_query if request.raw_query else ""),
        "CONTENT_TYPE": request.headers.get("content-type", ""),
        "CONTENT_LENGTH": request.headers.get("content-length", "0"),
        "SERVER_PROTOCOL": request.protocol,
        "REMOTE_ADDR": request.client_ip[0],
        "GATEWAY_INTERFACE": "CGI/1.1",
        "REDIRECT_STATUS": "200"
    })

    process = subprocess.Popen(
        ["C:\\xampp\\php\\php-cgi.exe"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env
    )

    body = request.body

    if isinstance(body, dict):
        body = urllib.parse.urlencode(body)

    if isinstance(body, str):
        body = body.encode()

    stdout, stderr = process.communicate(body)

    if stderr:
        print(stderr.decode(errors="ignore"))

    headers_raw, body = stdout.split(b"\r\n\r\n", 1)

    headers = {}

    for line in headers_raw.decode(errors="ignore").split("\r\n"):
        if ": " in line:
            key, value = line.split(": ", 1)
            headers[key.lower()] = value

    status = headers.pop("status", "200 OK")
    status_code = int(status.split()[0])

    return Response(
        body=body,
        status=status_code,
        headers=headers
    )