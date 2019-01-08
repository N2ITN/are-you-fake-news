from plotter import plot
import json


def lambda_handler(data, context=None):
    print(data)
    scores, url, url_clean = json.loads(data['body'])

    plot(scores, url, url_clean)
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps("Success!")
    }


# if __name__ == '__main__':

#     payload = json.dumps({
#         'body': [{
#             'fake news': 0.026105,
#             'center': 0.017353,
#             'left': 0.069697,
#             'extreme left': 0.001491,
#             'mixed': 0.293917,
#             'low': 0.006344,
#             'right-center': 0.062835,
#             'propaganda': 0.011925,
#             'conspiracy': 0.036079,
#             'hate': 0.002538,
#             'high': 0.29368,
#             'satire': 0.023235,
#             'extreme right': 0.013205,
#             'very high': 0.002354,
#             'pro-science': 0.001237,
#             'left-center': 0.101551,
#             'right': 0.151564
#         }, 'rad.com', 'rad.com']
#     })
#     lambda_handler(payload)
