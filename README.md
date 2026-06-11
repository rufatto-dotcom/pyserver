# pyserver

Servidor HTTP assíncrono implementado do zero em Python.

Sem Flask. Sem FastAPI. Sem Uvicorn. Só Python puro e o protocolo na mão.

---

## Por que?

Porque antes de usar um framework, eu precisava entender o que ele faz.

Esse projeto nasceu da necessidade de entender como um servidor web funciona por baixo — o parsing do protocolo HTTP, o roteamento, o ciclo de request/response, middlewares, CGI. Tudo implementado do zero.

Foi daqui que surgiu o [runtime-tool](https://github.com/rufatto-dotcom/runtime-tool).

---

## Funcionalidades

- Servidor HTTP assíncrono com `asyncio`
- Roteamento estático e dinâmico com parâmetros (`:id`)
- Suporte a `GET` e `POST`
- Parsing de `application/json` e `application/x-www-form-urlencoded`
- Sistema de middlewares
- Serving de arquivos estáticos
- Suporte a PHP via CGI
- Objetos `Request` e `Response` tipados

---

## Estrutura

```
pyserver/
├── app.py                  # Entrypoint e registro de rotas
├── routes.py               # Definição das rotas da aplicação
├── core/
│   ├── server.py           # Servidor asyncio
│   └── handler.py          # Handler de conexões
├── http/
│   ├── request.py          # Objeto Request
│   ├── requestParser.py    # Parsing do protocolo HTTP
│   ├── response.py         # Objeto Response
│   └── responseWriter.py   # Serialização da resposta
├── routing/
│   └── router.py           # Roteamento estático e dinâmico
├── middleware/
│   └── middleware.py       # Pipeline de middlewares
└── runtime/
    └── php.py              # Execução de PHP via CGI
```

---

## Como usar

```bash
git clone https://github.com/rufatto-dotcom/pyserver
cd pyserver
python app.py
```

### Definindo rotas

```python
from server.routing.router import get, post
from server.http.response import Response

@get("/users/:id")
def get_user(request):
    return f"User {request.params['id']}"

@post("/users")
def create_user(request):
    data = request.body  # dict se Content-Type: application/json
    return Response(data, status=201)
```

### Adicionando middlewares

```python
from server.middleware.middleware import add_middlewares
from server.http.response import Response

def auth_middleware(request):
    token = request.headers.get("authorization")
    if not token:
        return Response("Unauthorized", status=401)

add_middlewares(auth_middleware)
```

---

## Pré-requisitos

- Python 3.10+
- PHP (opcional, para suporte a arquivos `.php` via CGI)

---

## Projeto de estudo

Este é um projeto de estudo. O objetivo nunca foi substituir Flask ou FastAPI — foi entender o que eles fazem.

Pull requests e issues são bem-vindos.
