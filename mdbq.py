#! usr/bin/python
#coding=utf-8 
__author__ = 'liuliang'
import re
import urllib
import urllib2
import os

# 妈蛋表情网
class MDBQ:
    # 初始化方法
    def __init__(self):
        pass
    def getContent(self,url):
        request = urllib2.Request(url)
        while True:
            try:
                response = urllib2.urlopen(request)
                content = response.read()
                return content
            except Exception, e:
                print "错误原因:",e
                print "正在尝试重新连接"
        
    def getTitle(self,content):
        pattern = re.compile('<div.*?class="s_tab".*?>(.*?)<div.*?class="nums">', re.S)
        title = re.search(pattern, content).group(1)
        pattern = re.compile('<a href=(.*?)>(.*?)</a>', re.S)
        items = re.findall(pattern, title)
        return items
    def mkDir(self,path):
        path = path.strip()
        isExists = os.path.exists(path)
        if not isExists:
            print u"偷偷新建了名字叫做",path,u'的文件夹'
            os.makedirs(path)
            return True
        else:
            print u"名为",path,'的文件夹已经创建成功'
            return False
    #遍历获取内容
    def getPage(self,items):
        for item in items:
            content = self.getContent("http://www.itlun.cn"+item[0].strip('\''))
            pattern = re.compile('<li><span.*?class="pageinfo">.*?<strong>(.*?)</strong>.*?</li>', re.S)
            result = re.search(pattern, content)
            if result:
                allPage = int(result.group(1))
                for x in xrange(1,allPage+1):
                    print "正在创建F:/mdbq/"+item[1]+"/"+str(x)+"的目录"
                    self.mkDir("F:/mdbq/"+item[1]+"/"+str(x))
                    result = re.search(re.compile('/list-(.*?).html', re.S), item[0])
                    if result:
                        # print "http://www.tilun.con/plus/list.php?tid="+result.group(1)+"&PageNo="+str(x)
                        content = self.getContent("http://www.itlun.cn/plus/list.php?tid="+result.group(1)+"&PageNo="+str(x))
                        print "http://www.itlun.cn/plus/list.php?tid="+result.group(1)+"&PageNo="+str(x)
                        pattern = re.compile('<LI><a href="(.*?)" title=".*?" target="_blank"><IMG border="0".*?</a>', re.S)
                        its = re.findall(pattern, content)
                        for it in its:
                            infoUrl = "http://www.itlun.cn"+it.strip('\'')
                            content = self.getContent(infoUrl)
                            pattern = re.compile('<div.*?<div.*?class="divcss5-max-width".*? align="center">.*?<img src=(.*?)id=.*?alt=(.*?) title=.*?border=.*?/></a>.*?<DIV class="cShowPage">', re.S)
                            imgInfo = re.search(pattern, content)
                            # 分割字符串，获取图片类型
                            if imgInfo:
                                img = imgInfo.group(1).strip('\'').replace('\'','').split('.')
                                imgType = img.pop()
                                print imgInfo.group(1).strip('\'').replace('\'','')
                                filename = self.filenameFilter(imgInfo.group(2).strip('\'').replace('\'','')+"."+imgType)
                                self.saveImg(imgInfo.group(1).strip('\'').replace('\'',''), "F:/mdbq/"+item[1]+"/"+str(x)+"/"+filename)
    def saveImg(self,imgurl,filename):
        u = urllib.urlopen(imgurl)
        data = u.read()
        with open(filename, 'wb') as f:
            f.write(data)
            print '保持图片'+filename    
    def filenameFilter(self, filename):
        charlist = ["*", "?", "\\", "/", ":", "\"", "<", ">", "|"]   
        if (len(filename) >255):
            filename = filename[0:254]
        for char in charlist:
            if char in filename:
                filename = filename.replace(char, "_")
                print filename
        return filename  
mdbq = MDBQ()
# 获取首页
content = mdbq.getContent("http://www.itlun.cn/")
# 获取标题链接与标题名称
items = mdbq.getTitle(content)
mdbq.getPage(items)




