# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 12:48:31 2018

@author: LIANGOC
"""

import base64
import requests
import os
from bs4 import BeautifulSoup


def get_urls(url):
    '''获取一个页面的所有图片的链接'''
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Host': 'jandan.net'
    }
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'lxml')
    tags = soup.select('.img-hash')
    return tags


def get_html(url):
    """请求页面，返回响应"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'
    }
    try:
        resp = requests.get(url, headers=headers)   
        if resp.status_code == 200:
            return resp
        return None
    except ConnectionError:
        print('Error.')
    return None


def download_img(dir_path, img_url):
    """下载"""
    filename = img_url[-14:]
    img_content = get_html(img_url).content
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    try:
        with open(os.path.join(dir_path, filename), 'wb') as f:
            f.write(img_content)
            return True
    except Exception as e:
        print(e)
        return False
    

def main(dir_path, page=48):
    base_url = 'http://jandan.net/ooxx/'
    for i in range(page+1):
        page_url = base_url + 'page-{}/'.format(48-i)
        print(page_url)

        for tag in get_urls(page_url):
            img_hash = tag.text
            url = base64.b64decode(img_hash)
            img_url = str(url,'utf-8') #byte转换成str
            
            r = download_img(dir_path, 'http:' + img_url)
            if r: print('success')


if __name__ == '__main__':
    dir_path = 'D:\Python\Spider_Data\photo'
    main(dir_path)

