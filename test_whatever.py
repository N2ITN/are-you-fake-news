from multiprocessing.dummy import Pool

p = Pool(20)


def dothingstourl(link):
    'download_url'
    'parse_results'


links = [1, 2, 3, 4, 5, 6, 8, 9]

p.map(dothingstourl(), link)
