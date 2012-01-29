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

location = ''

locate = ''
if location:
    locate = '/' + location

urls = (
    '^'+locate+'/get(.*)', 'get',
    locate+'(.*)', 'index')


class reblog:
    def GET(self): raise web.seeother('/')


render = web.template.render('tmpl',)
recent = []

class index:

    def GET(self, arg):
        results = ''
        return render.index('','',results,location,recent)

    def POST(self, arg):
        i = web.input()
        if i:
            keyword = i.keyword.encode('utf-8')
            global recent
            recent = [keyword] + recent
            #recent.append(keyword)
            result = os.popen('mlocate '+keyword).read().split('\n')
            length = len(result)-1
            if length == 0:
                return render.index(keyword,'未找到匹配内容', [],location,'')
            results = []
            limit = 1000
            if length < limit:
                limit = length
            length = '有'+str(length)+'个文件匹配，显示前'+str(limit)+'个'
            for i in result:
                results.append(i.decode('utf-8'))
            return render.index(keyword,length, results[:limit], location, '')

class get:
    def GET(self, url):
        if not url:
            url = '/'
        #print url.encode('utf-8')
        client_ip = web.ctx.ip
        #print client_ip
        if client_ip  in ['127.0.0.1','localhost'] or url.startswith(('/home/public')):
            if os.path.isfile(url):
                if not url.split('/')[1] in ['lib','root']:
                    try:
                        f = open(url,'rb').read()
                        return f
                    except:
                        return '文件读取失败'
            elif os.path.isdir(url):
                temp_list = os.listdir(url)
                #print chardet.detect(temp_list[1])
                results = []
                for i  in temp_list:
                    results.append(i)
                if url == '/':
                    url = ''
                return render.list(results, location, url)
        return '文件禁止访问'

def webheader():
    web.header('Content-Type', 'text/html')

#app.add_processor(web.loadhook(webheader))

app_main = web.application(urls, globals())
application = app_main.wsgifunc()
if __name__=='__main__':
    app_main.run()
