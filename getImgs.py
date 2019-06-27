# coding = utf-8
import os
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from lxml import etree
from tqdm import tqdm


def get_urls(page_sum=30):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) '
                      'Chrome/17.0.963.56 Safari/535.11'}

    urlSet = set()
    print('get the urls!')
    for page_id in tqdm(range(1, page_sum + 1)):
        response = requests.get('http://www.doutula.com/article/list/?page=' + str(page_id), headers=headers)
        bsObj = BeautifulSoup(response.text, 'lxml')
        for url in bsObj.find_all('a', class_='list-group-item'):
            if 'href' in url.attrs:
                urlSet.add(url.attrs['href'])

    urls = prepare_urls(urlSet)
    with open('urls.txt', 'w+') as out_f:
        for each_url in urls:
            out_f.write(str(each_url) + '\n')
    return urls


def prepare_urls(urlSet):
    doneList = list()
    doneSet_file_path = 'doneSet.txt'
    if os.path.isfile(doneSet_file_path):
        with open(doneSet_file_path, 'r') as f:
            for line in f.readlines():
                doneList.append(line)
    doneSet = set(doneList)
    return urlSet - doneSet


def get_imgs(urlSet=None):
    urls_file = 'urls.txt'
    if urlSet is None:
        urlSet = set()
        with open(urls_file, 'r') as f:
            for line in f.readlines():
                urlSet.add(line)
    print('get the imgs!')
    for link in tqdm(urlSet):
        response = requests.get(link, headers=headers)
        bsObj = BeautifulSoup(response.text, 'lxml')
        tree = etree.HTML(bsObj)
        print(tree)

    # if len(tree.h3.a.text) > 0:
    #     dirName = tree.h3.a.text.replace('/', '')
    # else:
    #     dirName = link.split('/')[-1] + '-noname'

    # if os.path.isdir(dirName):
    #     pass
    # else:
    #     os.mkdir(dirName)

    # os.chdir(dirName)

    # for l1 in bsObj('td'):

    #     for l2 in l1('img'):
    #

    #         if len(l2.attrs['src']) > 20 and requests.get(l2.attrs['src']).status_code == 200:
    #             downUrl = l2.attrs['src']
    #         elif len(l2.attrs['onerror'].split("'")[-2]) > 20 and requests.get(
    #                 l2.attrs['onerror'].split("'")[-2]).status_code == 200:
    #             downUrl = l2.attrs['onerror'].split("'")[-2]
    #         else:
    #             continue


    #         if downUrl == 'http://img7.doutula.com/production/uploads/image/':
    #             continue
    #


    #         if 'alt' in l2.attrs:
    #             if len(l2.attrs['alt']) == 0:
    #                 with open('noname-' + downUrl.split('/')[-1], 'wb') as f:
    #                     f.write(requests.get(downUrl).content)
    #                 f.close()
    #             else:
    #                 with open(l2.attrs['alt'].replace('/', '') + '.' + downUrl.split('.')[-1], 'wb') as f:
    #                     f.write(requests.get(downUrl).content)
    #                 f.close()
    #         else:
    #             with open('noname-' + downUrl.split('/')[-1], 'wb') as f:
    #                 f.write(requests.get(downUrl).content)
    #             f.close()
    #
    # #            time.sleep(0.5)
    #
    # os.chdir('..')
    # with open('doneSet', 'a') as f:
    #     f.writelines(link + '\n')
    # f.close()


if __name__ == '__main__':
    get_imgs(get_urls())
