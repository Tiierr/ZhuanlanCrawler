# -*- coding=utf-8 -*-
import time,os,codecs,sys
import requests
from bs4 import BeautifulSoup
import getpass
import main
reload(sys)
sys.setdefaultencoding('utf-8')

Default_Header = {'X-Requested-With': 'XMLHttpRequest',
                  'Referer': 'http://www.zhihu.com',
                  'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; '
                                'rv:39.0) Gecko/20100101 Firefox/39.0',
                  'Host': 'www.zhihu.com'}
_session = requests.session()
_session.headers.update(Default_Header)

BASE_URL = 'https://www.zhihu.com'
CAPTURE_URL = BASE_URL+'/captcha.gif?r='+str(int(time.time())*1000)+'&type=login'
PHONE_LOGIN = BASE_URL + '/login/phone_num'
BASE_ZHUANLAN_API = 'https://zhuanlan.zhihu.com/api/columns/'
BASE_ZHUANLAN = 'https://zhuanlan.zhihu.com'

head = '''
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
</head>
<body>
'''

def start(zlname):
    sub_folder = os.path.join(os.getcwd(),'papers')
    if not os.path.exists(sub_folder):
        os.mkdir(sub_folder)
    exists_file = os.listdir('papers')
    os.chdir(sub_folder)
    zhuanlan_text(zlname,exists_file)

def save2html(filename, html):
    try:
        filename = filename + '.html'
        f = codecs.open(filename, 'a', encoding='utf-8')
        f.write(html)
        f.close()
    except:
        pass


def login(username,password):
    '''登录知乎'''
    cap_content = _session.get(CAPTURE_URL).content
    cap_file = open('cap.gif','wb')
    cap_file.write(cap_content)
    cap_file.close()
    captcha = raw_input('capture:')
    data = {"phone_num":username,"password":password,"captcha":captcha}
    r = _session.post(PHONE_LOGIN, data)
    print (r.json())['msg']

def zhuanlan_text(zlname,exists_file):
    i = 1
    print('-----------------------文章爬取开始-----------------------\n')
    Default_Header = {
                  'Referer': 'https://zhuanlan.zhihu.com/' + zlname,
                  'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; '
                                'rv:39.0) Gecko/20100101 Firefox/39.0',
                  'Host': 'zhuanlan.zhihu.com'}
    _session = requests.session()
    _session.headers.update(Default_Header)
    TextAPI = BASE_ZHUANLAN_API+ zlname + '/posts?limit=100&offset='
    endFlag = True
    offset = 0

    while endFlag:
        TextContentHTML = (_session.get(TextAPI+str(offset))).json()
        all_body = ''
        for everText in TextContentHTML:
            filename = everText['title'].encode('utf-8') 
            title = '<h1>' + filename + '</h1>'
            author = '<p><b>' + everText['author']['name'].encode('utf-8') + '</b></p>'
            body = everText['content'].encode('utf-8')
            all_body = title + author + body + all_body
            print('--------------------正在保存第' + str(i) + '个文章--------------------\n')
            i = i + 1

        if zlname in exists_file:
            continue

        html = head + all_body + "</body></html>"
        save2html(zlname,html)

        if(len(TextContentHTML) < 100):
            endFlag = False
        offset = offset + 100

    print('-----------------------文章爬取完毕-----------------------\n')
    os.chdir("..")

if __name__ == '__main__':
    username = raw_input('phone_num: ')
    password = getpass.getpass('password: ')
    login(username,password)
    zlname = raw_input('请输入专栏英文名: ')
    start(zlname)
    main.start_transfer('papers')
