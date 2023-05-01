# -*- codeing = utf-8 -*-
from bs4 import BeautifulSoup
import re
import requests
import os
import pandas as pd
import sys
import random
import time
# 导入自定义模块（GUI组件）
#import WindowShow
#import DataVis

#定义一个函数来输入检索信息
def input_message(web):
        '''
        在web网站中输入检索信息：关键信息、作者、年份、期刊并返回serch后的url
        '''
        url = web + '/search'
        
        print('请输入检索信息！')
        terms = input('Find articles with these terms:')
        if terms != '':
            url = url + '?qs=' + terms
        
        authors = input('Author(s):')
        if terms != '':
            url = url + '&authors=' + authors
        
        years = input('Year(s):')
        if terms != '':
            url = url + '&date=' + years
        
        journal = input('In this journal or book title:')
        if terms != '':
            url = url + '&pub=' + journal
          
        if url != web + '/search':
            return url
        else:
            print('未输入任何检索信息！')
            sys.exit('程序中止！')

#定义一个函数获取网页信息
def get_page(url,headers=None):
     '''
     发送请求获取网页信息
     '''

     time.sleep(random.randint(1,5))#就是隔一段时间再运行
     r = requests.get(url,headers=headers)

     return r.text

#定义一个函数对每一个文章的网页进行检索，获取信息
def analyze_paper(url):
        '''
        对每一个文章的网页进行检索，获取信息
        :param url: 需要检索的文章的url
        :return: msg: 包含文章的标题、作者、DOI、摘要、被引量、年份、关键词信息，若返回None,则表示不为期刊论文，跳过该文献
        '''
        content = get_page(url)
        # 匹配结果均为一个列表，关键词、作者、需要保留为List，其余需要转换为str
        # 关键词
        keyword = re.findall('target="_blank" class="">(.*?)</a></span>', content)
        if not keyword:
            print('不为论文...')   # 如果检索的不是期刊论文，则跳过
            return None
        msg = dict(keyword=keyword)
        # 文章标题
        title = re.findall('"{\'act_block\':\'main\',\'button_tp\':\'title\'}"\s+>\s+(\S+)\s+</a>', content)
        # 作者
        author = re.findall('"{\'button_tp\':\'author\'}">(.*?)</a>', content)
        # 摘要
        abstract = re.findall('<p class="abstract" data-sign="">(.*?)</p>', content)
        # DOI
        DOI = re.findall('data-click="{\'button_tp\':\'doi\'}">\s+(.*?)\s+</p>', content)
        # 被引量
        f = re.findall('"{\'button_tp\':\'sc_cited\'}">\s+(\d+)\s+</a>', content)
        # 年份
        pub_time = re.findall('<p class="kw_main" data-click="{\'button_tp\':\'year\'}">\s+(\d+)\s+</p>', content)
        # 更新字典
        # 使用try处理异常，可能有些页面会有信息缺失
        print(author)
        try:
            msg.update({'title': title[0],
                        'author': author,
                        'abstract': abstract[0],
                        'DOI': DOI[0],
                        'f': f[0],
                        'time': pub_time[0]
                        })
        except IndexError:
            Ti = None if title==[] else title[0]
            Au = None if author==[] else author[0]
            Ab = None if abstract==[] else abstract[0]
            Doi = None if DOI==[] else DOI[0]
            fac = None if f==[] else f[0]
            Pt = None if pub_time==[] else pub_time[0]
            msg.update({'title': Ti,
                        'author': Au,
                        'abstract': Ab,
                        'DOI': Doi,
                        'f': fac,
                        'time': Pt
                        })
        return msg

#定义一个函数获取每个文章链接
def analyze_page(content):
    '''
    解析网页信息
    :param content: 获取的网页信息（解码后的）
    '''
    #获取每一个文章的链接
    soup = BeautifulSoup(markup=content, features='lxml')
    urls_list = soup.find_all('a', href=re.compile('^//xueshu.baidu.com/usercenter/paper'))
    # 对该页面所有文章链接进行迭代
    for url in urls_list:
        message = self.analyze_paper('https:'+url['href'])  # 获取文章页面的信息
        if message:
            '''保存数据'''
            print(f'第{self.paper_num}篇文章爬取中')
            self.save_data(message)     # 保存文献信息
            self.paper_num += 1
        else:
            continue
    # 进行下一页爬取，判断是否还存在下一页的链接
    next_urls = re.findall('<a href="(.*?)" class="n" style="margin-right', content)
    # 若存在下一页内容，则继续爬取
    if next_urls:
        next_url = self.base_url + next_urls[0]
        content = self.get_page(next_url)
        self.analyze_page(content)
    else:
        print('爬虫结束...')

def save_data(self, msg):
    '''
    保存数据，包括文章标题、作者、关键词、被引量、摘要、年份、DOI
    :param msg: 有七个键值对的字典
    '''
    MSG = {'title':msg['title'],
            'author':str(['author']),
            'keyword':str(['keyword']),
            'f':msg['f'],
            'time':msg['time'],
            'DOI':msg['DOI'],
            'abstract':msg['abstract']
            } # 重新组织字典内顺序

    self.data = self.data.append(pd.DataFrame([MSG]))

def start(self):
    '''执行爬虫'''
    print('爬虫开始...')
    # 创建存储信息的文件夹
    try:
        os.makedirs('./BaiduScholar/')
    except FileExistsError:  # 如果文件夹已经存在，则跳过
        pass
    new_url = self.input_message(self.base_url)
    content = self.get_page(url=new_url)
    self.analyze_page(content)
    self.data.to_excel('./BaiduScholar/BaiduScholar.xlsx', index=False)

web = 'https://www.sciencedirect.com'
url=input_message(web)
text=get_page(url)
print(text)