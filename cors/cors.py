from typing import Iterable


def _add_cors_headers(response, methods: Iterable[str]) -> None:
    allow_methods = list(set(methods))
    if "OPTIONS" not in allow_methods:
        allow_methods.append("OPTIONS")
    headers = {
        "Access-Control-Allow-Methods": "*",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Credentials": "true",
        "Access-Control-Allow-Headers": (
            "origin, content-type, accept, "
            "authorization, x-xsrf-token, x-request-id"
        ),
    }
    response.headers.extend(headers)

#TODO: THIS METHOD IS BASICALLY USELESS, IT ONLY CALLS THE PREVIOUS ONE -> ALL CORS ARE OPEN

def add_cors_headers(request, response):
    try:
        if request.method != "OPTIONS":
            methods = [method for method in request.route.methods]
            _add_cors_headers(response, methods)
    except:
        _add_cors_headers(response, methods = [])

 

 