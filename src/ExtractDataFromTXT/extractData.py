#!/usr/bin/python
from collections import OrderedDict
from pyexcel_xls import save_data
import re

#以utf-8编码读取源文件的所有字节
def getArticles():
    f = open(r"E:\Users\lockon\Desktop\rawdata_all1.txt", 'r', encoding='utf-8').read()
    regexArticle = re.compile(r'【[\s\S]*?--')
    #articles就是所有文章的集合
    articles = re.findall(regexArticle, f)
    return articles

#定义保存成xls文件的方法，最后遍历完成后调用
def saveOuput():
    save_data(r"E:\Users\lockon\Desktop\rawdata_all1.xls", xls_data)  
    
#初始化excel的数据
xls_data = OrderedDict()
sheet1 = []
firstRow = []
changedIndex = 0
articles = getArticles()
#遍历所有文章的集合，一个个处理
for article in articles:
    #初始化row_data，它是数组形式，每一个元素代表excel里面的一格，它是excel表里面每一行的内容
    row_data = []
    tempFirstRow = []
    #'\n'是换行符，用换行符将整篇文章的每一行分隔开，articleLines就是所有行的内容集合
    articleLines = article.split('\n')
    #遍历当前文章的每一行的内容
    for line in articleLines:
        #如果当前行是带有'【】'这个符号的，就可以加入对应的方格里面
        if re.match(r'【.*】', line):
            #加入之前先把'【】'这些标签内容去掉，方格里面因为不需要
            index = re.match(r'【.*】', line).group()
            content = re.sub(r'【.*】', '', line)
            row_data.append(content)
            tempFirstRow.append(index)
        #这个elif是python里的else if
        elif re.match(r'--', line):
            #如果当前行内容是'--',说明这篇文章的所有内容遍历完了,可以跳出遍历每一行的循环
            break
        else:
            #如果当前行不包含标签符【】，也不是最后一行，就说明是参考文献的内容
            #因为要将他们是参考文献的内容，所以要向同一格里面塞
            #先通过数组长度获取参考文献这个格子的索引号，因为数组都是从0开始，所以要减一
            referenceIIndex = len(row_data) - 1
            #将已有的参考文献内容和当前行的内容合并，以分号和换行符隔开
            #如果当前参考文献内容为空，说明是第一个，不需要加分号和换行符
            if len(row_data[referenceIIndex]) > 0:
                currentIndexContent = row_data[referenceIIndex] + ';\n' + line
            else:
                currentIndexContent = line
            #将拼好的参考文献内容塞回去对应的格子
            row_data[referenceIIndex] = currentIndexContent
    
    if len(firstRow) > 0:
        if len(firstRow) < len(tempFirstRow):
            #新出现的字段的位置，changedIndex就是字段'关键词'的所在位置
            changedIndex = 0
            for i in range(len(firstRow)):
                if firstRow[i] != tempFirstRow[i]:
                    changedIndex = i
                    break
            if changedIndex != 0:
                firstRow.insert(changedIndex, tempFirstRow[changedIndex])
            else:
                changedIndex = len(firstRow)
                firstRow.append(tempFirstRow[-1])
    else:
        firstRow = tempFirstRow
        
    #将已经拼好的excel里面一整行的内容加进表单sheet1里面
    sheet1.append(row_data)

#遍历所有已经放进excel的内容，如果某一行的长度小于字段总数，说明没有关键词这个字段，那么插入一个空的元素到相应的地方
for row in sheet1:
    if len(row) < len(firstRow):
        row.insert(changedIndex, "")

#最后才插入能包括所有字段的第一行    
sheet1.insert(0, firstRow)

#将整个表单sheet1更新到xls_data，命名为Result, xls_data就是excel的所有内容
xls_data.update({u"Result": sheet1})

# 保存成xls文件
saveOuput()