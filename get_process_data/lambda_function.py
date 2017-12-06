from nn_predict import orchestrate
import json


def lambda_handler(url, context=None):
    print(url)
    result = orchestrate(json.loads(url['body']))
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(dict(result))
    }
    
    

