# coding:utf-8
from __future__ import unicode_literals, print_function

import os
import leancloud
import time
from leancloud import Object
from zhihu_oauth import ZhihuClient
from bs4 import BeautifulSoup

class zhihu():
    def __init__(self):
        leancloud.init("xxxx","xxxx")
        self.num = 1

    def login(self):
        TOKEN_FILE = 'token.pkl'

        client = ZhihuClient()

        if os.path.isfile(TOKEN_FILE):
            client.load_token(TOKEN_FILE)
        else:
            client.login_in_terminal()
            client.save_token(TOKEN_FILE)
        return client

    def getZhuanLan(self,client,zhuanlan):
        zl = ZhuanLan()
        column = client.column(zhuanlan)

        # 专栏id
        zl.set('name',column.id)
        # 专栏作者
        zl.set('author',column.author.name)
        # 专栏名
        zl.set('title',column.title)
        # 专栏描述
        zl.set('description',column.description)
        # 专栏文章数量
        zl.set('articles_count',column.articles_count)

        return zl

    def getArticle(self,client,zhuanlan,zl):
        column = client.column(zhuanlan)
        relation = zl.relation('containedArticles')

        for article in column.articles:
            try:
                art = Article()
                # 文章标题
                print(('title',article.title))
                art.set('title',article.title).save()
                # 作者
                art.set('author',article.author.name).save()
                # 文章摘要
                art.set('excerpt',article.excerpt).save()
                # 文章正文
                soup = BeautifulSoup(article.content,'lxml')
                content = soup.get_text()
                art.set('content',content).save()
                # 所属专栏名
                art.set('column_name',article.column.title).save()
                # 文章id
                art.set('art_art_id',article.id).save()
                # 文章封面图
                art.set('image_url',article.image_url).save()
                # 点赞数
                art.set('voteup_count',article.voteup_count).save()
                # 发表时间
                localtime = time.localtime(article.updated_time)
                created_time = time.strftime("%Y-%m-%d %H:%M:%S", localtime)
                art.set('created_time',created_time).save()
                relation.add(art)
                print('正在保存第' + str(self.num) + '篇文章')
                self.num += 1
                time.sleep(2)
            except:
                pass

        zl.save()
        print('保存完毕')

    def start(self,zhuanlan):
        client = self.login()
        zl = self.getZhuanLan(client,zhuanlan)
        self.getArticle(client,zhuanlan,zl)

class ZhuanLan(Object):
    # name
    @property
    def name(self):
        return self.get('name')
    @name.setter
    def name(self, value):
        return self.set('name', value)

    # author
    @property
    def author(self):
        return self.get('author')
    @author.setter
    def author(self, value):
        return self.set('author', value)

    # title
    @property
    def title(self):
        return self.get('title')
    @title.setter
    def title(self, value):
        return self.set('title', value)

    # description
    @property
    def description(self):
        return self.get('description')
    @description.setter
    def description(self, value):
        return self.set('description', value)

    # articles_count
    @property
    def articles_count(self):
        return self.get('articles_count')
    @articles_count.setter
    def articles_count(self, value):
        return self.set('articles_count', value)

class Article(Object):
    # author
    @property
    def author(self):
        return self.get('author')
    @author.setter
    def author(self, value):
        return self.set('author', value)

    # title
    @property
    def title(self):
        return self.get('title')
    @title.setter
    def title(self, value):
        return self.set('title', value)

    # excerpt
    @property
    def excerpt(self):
        return self.get('excerpt')
    @excerpt.setter
    def excerpt(self, value):
        return self.set('excerpt', value)

    # content
    @property
    def content(self):
        return self.get('content')
    @content.setter
    def content(self, value):
        return self.set('content', value)

    # column_name
    @property
    def column_name(self):
        return self.get('column_name')
    @column_name.setter
    def column_name(self, value):
        return self.set('column_name', value)

    # art_id
    @property
    def art_id(self):
        return self.get('art_id')
    @art_id.setter
    def art_id(self, value):
        return self.set('art_id', value)

    # image_url
    @property
    def image_url(self):
        return self.get('image_url')
    @image_url.setter
    def image_url(self, value):
        return self.set('image_url', value)

    # voteup_count
    @property
    def voteup_count(self):
        return self.get('voteup_count')
    @voteup_count.setter
    def voteup_count(self, value):
        return self.set('voteup_count', value)

    # created_time
    @property
    def created_time(self):
        return self.get('created_time')
    @created_time.setter
    def created_time(self, value):
        return self.set('created_time', value)

if __name__ == "__main__":
    zhuanlan = zhihu()
    # 输入专栏名
    zhuanlan.start('xxx')
