from pprint import pprint

import requests
from lxml import etree
import logging
from urllib.request import quote

timeout = 3
#headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}

motherUrl = 'https://zhidao.baidu.com/search?lm=0&rn=10&pn=0&fr=search&ie=gbk&word='

def getQuestion(question):
    """
    根据question从百度知道中获取相似问题/答案/链接
    输入：question
    返回：{
    'data': [
            {'simques': 相似问题, 'answer': 相似问题的答案, 'link': 相似问题的链接},
            {'simques': 相似问题, 'answer': 相似问题的答案, 'link': 相似问题的链接},
            ...
            ]
    'issuccess': True or False
    'desc': 状态描述
    }
    """
    url = motherUrl + quote(question.encode('gbk'))
    try:
        rsp = requests.get(url=url, headers=headers, timeout=timeout)
        page_str = rsp.text
    except Exception:
        return {'data': [], 'issuccess': False, 'desc': 'no response'}
    
    try:
        page_str = page_str.encode(rsp.encoding).decode('gbk')
    except Exception:
        try:
            page_str = page_str.encode(rsp.encoding).decode('utf8')
        except Exception:
            return {'data': [], 'issuccess': False, 'desc': 'coding error'}

    try:
        tree = etree.HTML(page_str)
    except Exception:
        return {'data': [], 'issuccess': False, 'desc': 'parse error'}
    
    data = []
    for row in tree.xpath('//div[@class="list-inner"]//dl[@class="dl" or @class="dl dl-last"]'):
        try:
            temp = {}
            temp['link'] = str(row.xpath('.//a[@class="ti"]/@href')[0])
            temp['simques'] = ''.join(row.xpath('.//a[@class="ti"]//text()'))
            temp['answer'] = ''.join(row.xpath('.//dd[@class="dd answer"]//text()')).replace('答：', '')
            data.append(temp)
        except Exception:
            continue
    
    if len(data) > 0:
        return {'data': data, 'issuccess': True, 'desc': 'normal'}
    else:
        return {'data': [], 'issuccess': False, 'desc': 'no result'}


if __name__ == '__main__':
    result = getQuestion('兰迪学科英语服务怎么样?')
    pprint(result)