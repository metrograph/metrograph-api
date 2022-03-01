



from array import array
from unittest import case
from sanic.request import Request


class RequestValidator:

    def __init__(self) -> None:
        pass

    def validate(self, required_input: array, request: Request) -> bool:
        for parameter in required_input:
            if type(parameter) == str:
                if(request.form.get(parameter)) == None:
                    return False
            elif type(parameter) == list:
                if(type(request.form.get(parameter[0]))) != parameter[1]:
                    print('====')
                    print(parameter[0])
                    print(type(request.files.get(parameter[0])))
                    print('====')
                    return False
        return True