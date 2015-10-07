# -*- coding: utf-8 -*-

import urllib,urllib2,re,time,thread,sqlite3,string
import sys 
from mail_test2 import mailtest

class Spider_Model:

    def __init__(self):
        self.page = 1
        self.pages = []
        self.enable = False
        self.conn = None
        self.cursor = None

        
    def GetPage(self,page):
        myUrl = "http://m.byr.cn/board/ParttimeJob"+"?p="+page
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'   
        headers = { 'User-Agent' : user_agent }   
        req = urllib2.Request(myUrl, headers = headers)
        myResponse = urllib2.urlopen(req)
        myPage = myResponse.read()
        unicodePage = myPage.decode("utf-8")

        myItems = re.findall('<li.*?><div><a href="(.*?)">(.*?)</a>',unicodePage,re.S)
        items = []
        for item in myItems:
            if not item[0].find('class')>=0:
                items.append([item[0],item[1]])
        return items

    def LoadPage(self):
        while self.enable:
            if len(self.pages)<2:
                try:
                    myPage = self.GetPage(str(self.page))
                    self.page += 1
                    self.pages.append(myPage)
                except BaseException,e:
                    print e

                else:
                    time.sleep(1)

    def GetEmail(self,myUrl):
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'   
        headers = { 'User-Agent' : user_agent }   
        req = urllib2.Request(myUrl, headers = headers)
        myResponse = urllib2.urlopen(req)
        myPage = myResponse.read()
        unicodePage = myPage.decode("utf-8")

        myEmail = re.search('[a-zA-Z0-9](([a-zA-Z0-9]*\.[a-zA-Z0-9]*)|[a-zA-Z0-9]*)[a-zA-Z0-9]@([a-z0-9A-Z]+\.)+[a-zA-Z]{2,}',unicodePage,re.S)

        return myEmail

    

    def ShowPage(self,nowPage,page):
        self.conn = sqlite3.connect('forum.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('create table if not exists forum_data (id INTEGER primary key, title varchar(20), attr varchar(20),email varchar(20))')

        #下面部分需要您自己填入!!!!!
        #发送方邮箱地址
        from_addr = 'xxx'
        #发送方邮箱密码
        password = 'xxx'
        #发送方邮箱smtp
        smtp_server = 'xxx'
        #邮件标题
        title = 'xxxx'
        #邮件正文
        content = 'xxxx'
        #附件在本地的绝对路径
        address = u'xxx'
        #关键词 例子
        key_word = u'猿题库'
        words = key_word.split(" ")
        
        count = 1
        for items in nowPage:
            if page <= 5:
                attr = items[0].split('ParttimeJob/')
                article_id = string.atoi(attr[1])
                article_title = items[1]
                article_attr = 'http://m.byr.cn/article/ParttimeJob/'+attr[1]
                myEmail = self.GetEmail(article_attr)
                
                is_want = True
                if myEmail is None:
                    page_email = 'null'
                else:
                    page_email = myEmail.group(0)
                    to_addr = page_email
                    if count<=10:
                        for word in words:
                            if word not in article_title:
                                is_want = False
                                break
                        if is_want:
                            self.cursor.execute("SELECT * FROM forum_data WHERE id = %d" %article_id)
                            result = self.cursor.fetchone()
                            if result is None:
                                mailtest(from_addr, to_addr, title, content, address, smtp_server, password) 
                                print article_title 
                                count = count+1
                                self.cursor.execute("insert or ignore into forum_data (id ,title, attr, email) values (?, ?, ?, ?)",(article_id, article_title, article_attr, page_email))
                                self.conn.commit()
            else:
                self.cursor.close()
                self.conn.close()
                self.enable = False
                break

    def Start(self):
        self.enable = True
        page = self.page

        print u'目前已投递简历如下：'
        
        thread.start_new_thread(self.LoadPage,())

        while self.enable:
            if self.pages:
                nowPage = self.pages[0]
                del self.pages[0]
                self.ShowPage(nowPage,page)
                page += 1


           


print u'请按下回车开始自动投递简历：'

raw_input(' ')
myModel = Spider_Model()    
myModel.Start() 
  
               

    
                
                                 
        
