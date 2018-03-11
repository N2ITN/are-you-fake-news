from helpers import timeit
import boto3
bucket = boto3.resource('s3').Bucket('fakenewsimg')
import requests


@timeit
def save_plot(page, scores):
    ''' clear bucket of matching images, run plotter to make new images'''
    scores = scores['scores']

    print("Plotting article:")
    plot_api = 'https://lbs45qdjea.execute-api.us-west-2.amazonaws.com/dev/plotter'
    payload = [scores, page + '_fb', page + '_fb']
    print(requests.post(plot_api, json=payload).text)
    print("results")
    print(payload)


import scrape_fb
import mongo_get_links


def process_fb_page(page):
    try:
        scores = mongo_get_links.check_scores(page)
        print(scores)
        save_plot(page, scores)
        return scores['posts']
    except StopIteration:
        print('no scores in db')
        pass
    try:
        scores = scrape_fb.scrape(page)
        if not scores:
            return False
        save_plot(page, scores)
    except Exception as e:
        print('ERROR ' + e)
        return False
    return scores['posts']


if __name__ == '__main__':
    process_fb_page('nytimes')