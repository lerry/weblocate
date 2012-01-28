#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
For:
by Lerry  http://lerry.org
Start from 2011-11-30 18:54
Last edit at 2011-11-30 18:54
Finish at 2011-11-30 21:30
'''
import os
import web

urls = (
   '/', 'index',
   '^/get(.*)','get',
)

render = web.template.render('tmpl',)
recent = []


class index:

    def GET(self):
        results = ''
        return render.index('','',results, recent)

    def POST(self):
        i = web.input()
        if i:
            keyword = i.keyword.encode('utf-8')
            recent.append(keyword)
            result = os.popen('mlocate '+keyword).read().split('\n')
            length = len(result)-1
            if length == 0:
                return render.index(keyword,'未找到匹配内容', [], '')
            results = []
            limit = 1000
            if length < limit:
                limit = length
            length = '有'+str(length)+'个文件匹配，显示前'+str(limit)+'个'
            for i in result:
                results.append(i.decode('utf-8'))
            return render.index(keyword,length, results[:limit], '')

class get:
    def GET(self, url):
        if not url.split('/')[1] in ['lib','root']:
            try:
                f = open(url,'rb').read()
                #web.header('Content-type','application/octet-stream')
               # web.header('Transfer-Encoding','chunked')
                return f#url.encode('utf-8')
            except:
                return '文件读取失败'
        else:
            return '文件禁止访问'
        #print '^-^'

def webheader():
    web.header('Content-Type', 'text/html')

app = web.application(urls,globals(),autoreload=True)
#app.add_processor(web.loadhook(webheader))

if __name__ == '__main__':
    app.run()
