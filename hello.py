"""

    Metrograph - Python Action Template
    
    Template version:   1.0.0
    Runtime:            Python
    Runtime Version:    3.9.10
    License:            MIT
    Docs:               https://docs.metrograph.io/action/templates

"""

import json

def __handler__(event, context=None):

    # TODO: Implement action code here..

    result = {
        "message": "Hello Metrograph!"
    }

    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }