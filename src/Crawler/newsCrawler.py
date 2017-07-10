#!/usr/bin/python
import urllib.request
from bs4 import BeautifulSoup
import re

path = r"E:\Users\lockon\Desktop\\"
ouputFileName = r"test1.txt"

#定义保存新闻内容的方法
def writeNews2File(news):
    #第一个参数是文件目录，如果文件不存在会重新创建
    #第二个参数'a'表示每次都在文件最下面写入内容，不会覆盖原有的
    #第三个参数，将新闻以utf-8编码写入文件
    f = open(path + ouputFileName,'a', encoding='utf-8')
    f.write(news + '\n')
    f.close()

#搜狐的主页，以这个为起点，从这里搜索搜狐的新闻链接
sourceUrl = "http://news.sohu.com"
#获取网页里面的html源代码，搜狐主页的编码格式是gbk
sourceCode = urllib.request.urlopen(sourceUrl).read()
sourceCode = sourceCode.decode('gbk')
#搜狐上面匹配新闻网页的正则表达式
regexPage = re.compile(r'http://news.*?html')
#从网页的html源代码中找出所有匹配新闻链接格式的内容，用pageAddresslist存放
pageAddresslist = re.findall(regexPage, sourceCode)
#去除重复的链接(list是有序可重复的集合，set是无序不重复的集合)
#先将pageAddresslist转换成set可以去除重复的内容，再转换list类型方便后面操作
pageAddresslist = list(set(pageAddresslist))

#用来记录新闻条数
index = 1

#遍历爬出来的新闻链接
for url in pageAddresslist:
    #读取当前新闻链接的源代码
    try:
        html = urllib.request.urlopen(url).read()
    except Exception as e:
        print ('found exception: ' + str(e))
        continue
    
    #初始化新闻内容
    news = ''
    #将页面源代码用BeautifulSoup格式化成soup对象，这样方便我们提取里面的内容
    soup = BeautifulSoup(html,'html.parser')
    #因为不同网站标签的名字都不一样，所以下面的代码适用搜狐
    #判断这个页面有没有title这个标签，如果连新闻标题都没有就跳过
    #continue是停止当前这个url的操作，就是这个url不会执行后面context那堆代码(下一个url还会继续)
    if soup.title is None:
        continue
    #获取id为contentText的html标签
    contentText = soup.find_all(id='contentText')
    #所得结果contentText是一个list对象，因为是以id来获取，所以结果应该只有一个
    #判断contentText和它的第一个元素是否为空，如果为空就不再执行后面的代码
    if contentText is not None and len(contentText) > 0 and contentText[0] is not None:
        #在id为contentText的标签里找出所有p标签，p是paragraph，就是段落内容
        paras = contentText[0].find_all('p')
        #如果有段落说明有正文内容，下面就开始拼新闻的内容
        if len(paras) > 0:
            #news在前面已经初始化了，先写上新闻序号和新闻链接，'\n'是换行符
            news = str(index) + ': ' + url + '\n'
            #再加入新闻标题
            news += soup.title.string + '\n'
            #下面开始加上正文内容，遍历前面找到的所有段落内容
            for para in paras:
                #正常来说用.string方法就可以获取到文本的内容
                #但是搜狐里面有些小标题，在p标签里面还加了子标签strong，所以要做处理
                tempContent = para.string
                #如果string是空，说明当前p标签还有子标签
                #contents方法可以获取当前标签的所有子标签
                #返回的结果是一个list类型，搜狐新闻网页这里有两个元素
                #第一个是子标签是文章缩进的两个空格，第二个才是带有文本内容strong标签
                if tempContent is None and len(para.contents) > 1:
                    tempContent = para.contents[1].string
                
                #有时候并不是所有页面的html格式都一样，所以有可能上面得到的tempContent是空的
                #如果是空的就跳过,如果有内容就加入到新闻的内容里面
                if tempContent is not None and len(tempContent) > 0 :
                    news += tempContent + '\n'
        
        #处理完当前页面的新闻内容，如果新闻内容是有东西的，就调用前面定义的方法写入到本地文件里面            
        if len(news) > 0:
            #这个只是在运行的时候打出日志看看
            print(news)
            #记录新闻的数量
            index += 1
            #调用方法写入文件
            writeNews2File(news)