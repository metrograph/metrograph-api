



from array import array
from unittest import case
from sanic.request import Request


class RequestValidator:

    def __init__(self) -> None:
        pass

    def validate(self, required_input: array, required_files: array, request: Request) -> bool:
        for parameter in required_input:
            if(request.form.get(parameter)) == None:
                return False
        for parameter in required_files:
            if(request.files.get(parameter)) == None:
                return False
        return True