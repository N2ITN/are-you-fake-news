"""
Note: 
This fork of newspaper must be used: https://github.com/n2itn/newspaper
"""
import newspaper
import json


def lambda_handler(data, context=None):
    url = data['body']
    try:
        article = newspaper.Article(url)
        article.download()
        article.parse()
    except newspaper.article.ArticleException:
        return ''

    output = article.text + ' ' + article.title

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(output)
    }
