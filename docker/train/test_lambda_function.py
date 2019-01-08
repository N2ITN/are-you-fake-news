# from lambda_function import lambda_handler

import requests
api = 'https://lbs45qdjea.execute-api.us-west-2.amazonaws.com/dev/dnn_nlp'

print(
    requests.post(
        api, {'body': '3+1=4-1 thats 3 quick maths. everyday mans on the block. smoke trees. '}).text)
print('short test passed')

print(
    requests.post(api, {
        'body':
            str('3+1=4-1 thats 3 quick maths. everyday mans on the block. smoke trees. ' * 1000) +
            ' ||~~|| take mans twix by force '
    }).text)
print(">1000 test passed")
