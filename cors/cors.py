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


def add_cors_headers(request, response):
    #try:
    print(request.route)
    if request.method != "OPTIONS":
        print("#####################")
        print(request)
        methods = [method for method in request.route.methods]
        print(methods)
        _add_cors_headers(response, methods)
    #except:
    #    _add_cors_headers(response, methods = [])

 

 