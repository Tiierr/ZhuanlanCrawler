# ZhuanlanCrawler

获取知乎专栏文章内容有三种方式。
- 通过直接解析专栏url,提取文章内容
- 利用知乎专栏API获取文章内容
- 利用大神的写的zhihu_oauth模块获取文章内容

`module method`中的代码是利用[@77大神](https://github.com/7sDream)的[zhihu_oauth](https://github.com/7sDream/zhihu-oauth)模块获取文章内容

## 一. 安装 zhihu_oauth



```python
>>> pip install zhihu_oauth
```
## 二. 使用 load_token 登录

```python

TOKEN_FILE = 'token.pkl'

client = ZhihuClient()

if os.path.isfile(TOKEN_FILE):
    client.load_token(TOKEN_FILE)
else:
    client.login_in_terminal()
    client.save_token(TOKEN_FILE)

```
## 三. 获取专栏信息
```python

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

```
## 四. 获取文章信息
```python
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
```
## 五. 数据存储

```python
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
```
- 数据的存储为 leanCloud 云存储。
- 我们采用 property 属性来构建实体类。即面向对象思想的一些体现。这样存储过程就更为直观简单。

## 六. 数据截图

### 专栏
![](http://p1.bqimg.com/567571/d294686013f91832.png)

### 文章
![](http://p1.bqimg.com/567571/5f848d0140ded6ba.png)
