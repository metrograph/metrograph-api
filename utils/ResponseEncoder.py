


from json import JSONEncoder


class ResponseEncoder(JSONEncoder):

    def default(self, o):
        return o.__dict__