# coding = utf-8

import os

import requests
from lxml import etree
from tqdm import tqdm
import json


def get_settings():
    with open('settings.json', 'r') as f:
        return json.load(f)


class ImgCrawler:
    def __init__(self):
        settings = get_settings()
        self.headers = settings['headers']
        self.pages_dir = settings['page_dir']
        self.base_url = settings['base_url']
        self.img_dir = settings['img_dir']
        self.json_dir = settings['img_json']

    def searchs(self, key_words, save_page=True, regrab=False, save_img=True, save_json=True):
        """
        Get multiple keyword images
        :param key_words:
        :param save_page:
        :param regrab:
        :param save_img:
        :param save_json:
        :return:
        """
        for each_k in key_words:
            self.search(each_k, save_page, regrab, save_img, save_json)

    def search(self, keyword, save_page=True, regrab=False, save_img=True, save_json=True):
        save_page_path = os.path.join(self.pages_dir, keyword + '.html')
        if not regrab and os.path.exists(save_page_path):
            print('From html saved file...')
            with open(save_page_path, 'r') as html_p:
                html_content = html_p.read()
        else:
            response = requests.get(self.base_url + keyword, headers=self.headers)
            html_content = response.text
            if save_page:
                self.save_page_html(keyword, html_content)

        img_json = {
            'key_word': keyword,
            'imgs': []
        }
        page_selector = etree.HTML(html_content)
        imgs = page_selector.xpath('//*[@id="search-result-page"]/div/div/div[2]/div/div[1]/div[1]/div/a')

        print('Getting: ', keyword)
        for i, img_selector in enumerate(tqdm(imgs)):
            img_bk_url = img_selector.xpath('./img/@data-backup')[0]
            img_ori_url = img_selector.xpath('./img/@data-original')[0]
            img_name = img_selector.xpath('./p/text()')[0] + "--" + str(i)
            if save_img:
                self.save_image(img_ori_url, img_name, keyword)
            img_json['imgs'].append({
                'img_name': img_name,
                'bk_url': img_bk_url,
                'ori_url': img_ori_url
            })
        if save_json:
            save_json_path = os.path.join(self.json_dir, keyword + '.json')
            if not os.path.exists(self.json_dir):
                os.makedirs(self.json_dir)
            with open(save_json_path, 'w+') as json_f:
                json_f.write(json.dumps(img_json))
        return img_json

    def save_page_html(self, key_word, html_content):
        if not os.path.exists(self.pages_dir):
            os.mkdir(self.pages_dir)
        page_saved_path = os.path.join(self.pages_dir, key_word + '.html')
        with open(page_saved_path, 'w+') as save_file:
            save_file.write(html_content)
        return page_saved_path

    def save_image(self, url, name, key_word):
        img_name = name + '.' + url.split('/')[-1].split('.')[-1]
        img_subdir = os.path.join(self.img_dir, key_word)
        if not os.path.exists(img_subdir):
            os.makedirs(img_subdir)
        img_saved_path = os.path.join(img_subdir, img_name)
        with open(img_saved_path, 'wb+') as img_f:
            img_f.write(requests.get(url, self.headers).content)
        return img_saved_path


if __name__ == '__main__':
    imgc = ImgCrawler()
    imgc.searchs(['!!!', '???'], save_img=True, save_json=True, save_page=True)
