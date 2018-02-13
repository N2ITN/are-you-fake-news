"""
This is deployed to 

"""
from cnn_predict import orchestrate
import json


def lambda_handler(url, context=None):

    result = orchestrate(json.loads(url['body']))
    print(result)
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(result)
    }
