#!/usr/bin/python
from collections import OrderedDict
from pyexcel_xls import save_data
import re

#以utf-8编码读取源文件的所有字节
f = open(r"E:\Users\lockon\Desktop\LY_20170602204532.txt", 'r', encoding='utf-8').read()

#这个正则表达式是匹配每一篇文章，因为每篇文章都是'【来源篇名】'开头，'--'结束，所以下面的正则表达式就可以提取出每篇文章的内容
regexArticle = re.compile(r'【[\s\S]*?--')
#articles就是所有文章的集合
articles = re.findall(regexArticle, f)

#初始化excel的数据
xls_data = OrderedDict()
#初始化excel的第一个表达内容，这个属于xls_data的一部分
sheet1 = []
#第一行内容
sheet1.append([u"【来源篇名】", u"【英文篇名】", u"【来源作者】", u"【基    金】", u"【期    刊】", u"【第一机构】", u"【机构名称】", u"【第一作者】", u"【中图类号】", u"【年代卷期】", u"【基金类别】", "【参考文献】"])

#遍历所有文章的集合，一个个处理
for article in articles:
    #初始化row_data，它是数组形式，每一个元素代表excel里面的一格，它是excel表里面每一行的内容
    row_data = []
    
    #'\n'是换行符，用换行符将整篇文章的每一行分隔开，articleLines就是所有行的内容集合
    articleLines = article.split('\n')
    #遍历当前文章的每一行的内容
    for line in articleLines:
        #如果当前行是带有'【】'这个符号的，就可以加入对应的方格里面
        if re.match(r'【.*】', line):
            #加入之前先把'【】'这些标签内容去掉，方格里面因为不需要
            content = re.sub(r'【.*】', '', line)
            row_data.append(content)
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
            
    #将已经拼好的excel里面一整行的内容加进表单sheet1里面
    sheet1.append(row_data)
#将整个表单sheet1更新到xls_data，命名为Result, xls_data就是excel的所有内容
xls_data.update({u"Result": sheet1})

# 保存成xls文件  
save_data(r"E:\Users\lockon\Desktop\data.xls", xls_data)  