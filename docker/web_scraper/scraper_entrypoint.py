"""
Note: 
This fork of newspaper must be used: https://github.com/n2itn/newspaper
"""
import newspaper
import json
import spider_domain
from async_multi import meta_async
from flask import Flask, request

app = Flask(__name__)


def scrape(url):
    try:
        article = newspaper.Article(url)
        article.download()
        article.parse()
    except newspaper.article.ArticleException:
        return ''
    output = article.text + ' ' + article.title
    return output


@app.route("/", methods=['POST'])
def lambda_handler():
    data = json.loads(request.data.decode('utf-8'))
    print(data)

    if data['service'] == 'download':

        output = scrape(data['url'])

        return json.dumps([output])

    elif data['service'] == 'spider':
        return json.dumps(spider_domain.crawl(data['url']))

    elif data['service'] == 'multi':
        urls = spider_domain.crawl(data['url'])
        articles_all = meta_async(urls)
        return json.dumps(articles_all)

    else:
        return json.dumps('submit valid service name')


if __name__ == '__main__':
    app.run(debug=False, use_reloader=True, host='0.0.0.0', threaded=True, port=6600)
