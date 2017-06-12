#!/usr/bin/python
from collections import OrderedDict
from pyexcel_xls import save_data
import re

#以utf-8编码读取源文件的所有字节
def getArticles():
    f = open(r"E:\Users\lockon\Desktop\644.txt", 'r', encoding='utf-8').read()
    regexArticle = re.compile(r'PMID[\s\S]*?PL  - ')
    #articles就是所有文章的集合
    articles = re.findall(regexArticle, f)
    return articles

#定义保存成xls文件的方法，最后遍历完成后调用
def saveOuput():
    save_data(r"E:\Users\lockon\Desktop\data644.xls", xls_data) 
    
#初始化excel的数据
xls_data = OrderedDict()
sheet1 = [["PMID", "TI", u"作者-机构", "PT"]]

articles = getArticles()
#遍历所有文章的集合，一个个处理
for article in articles:
    row_data = []
    
    articleLines = article.split('\n')
    
    pmid = ''
    ti = ''
    authorAffiliation = ''
    pt = ''
    
    #是不是第一条作者的记录
    isFirstAuthor = True
    #是不是第一条AD的记录
    isFirstAD = True
    #是不是第一条PT的记录
    isFirstPT = True
    #当前的标签
    currentIndex = ''
    
    for line in articleLines:
        if re.match(r'PMID- ', line):
            pmid = re.sub(r'PMID- ', '', line)
        elif re.match(r'TI  - ', line):
            lineContent = re.sub(r'TI  - ', '', line)
            if lineContent[len(lineContent) - 1] == "." :
                lineContent = lineContent[:-1]
            ti = lineContent
            currentIndex = 'TI'
        elif re.match(r'PG  - ', line) or re.match(r'LID - ', line) or re.match(r'AB  - ', line):
            #当遍历到这些不需要的标签，就说明AD或者TI的内容已经遍历完，可以将当前标签改成一个不会用到的来跳过那个if elif(65-68行)
            currentIndex = 'NIL'
        elif re.match(r'      ', line):
            lineContent = re.sub(r'      ', '', line)
            lineContent = re.sub(r". Electronic address:", '', lineContent) 
            if lineContent[len(lineContent) - 1] == "." :
                lineContent = lineContent[:-1]
                reg = r"[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}"
                lineContentWithoutMail = re.sub(reg, '', lineContent)
                if len(lineContentWithoutMail) < len(lineContent):
                    if lineContentWithoutMail[len(lineContentWithoutMail) - 2 :] == ". " :
                        lineContentWithoutMail = lineContentWithoutMail[:-2]
                    lineContent = lineContentWithoutMail
            if len(lineContent.strip()) > 0:
                if currentIndex == 'TI':
                    ti += " " + lineContent
                elif currentIndex == 'AD':
                    authorAffiliation += " " + lineContent
        elif re.match(r'FAU - ', line):
            if isFirstAuthor:
                authorAffiliation = re.sub(r'FAU - ', '', line)
                isFirstAuthor = False
            else:
                authorAffiliation += " ; " + re.sub(r'FAU - ', '', line)
            isFirstAD = True
        elif re.match(r'AU  - ', line):
            authorAffiliation += " [" + re.sub(r'AU  - ', '', line) + "]"
        elif re.match(r'AD  - ', line): 
            lineContent = re.sub(r'AD  - ', '', line)
            lineContent = re.sub(r" Electronic address:", '', lineContent)
            currentIndex = 'AD'
            if lineContent[len(lineContent) - 1] == "." or lineContent[len(lineContent) - 1] == ";":
                lineContent = lineContent[:-1]
            if isFirstAD:
                authorAffiliation += " : " + lineContent
                isFirstAD = False
            else:
                authorAffiliation += " / " + lineContent
        elif re.match(r'PT  - ', line):
            if isFirstPT:
                pt = re.sub(r'PT  - ', '', line)
                isFirstPT = False
            else:
                pt += " ; " + re.sub(r'PT  - ', '', line)
            
    row_data = [pmid, ti, authorAffiliation, pt]
    sheet1.append(row_data)
    
#将整个表单sheet1更新到xls_data，命名为Result, xls_data就是excel的所有内容
xls_data.update({u"Result": sheet1})

# 保存成xls文件
saveOuput()