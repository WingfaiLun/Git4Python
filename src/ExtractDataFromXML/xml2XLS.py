#!/usr/bin/python
import xml.etree.cElementTree as ET
from collections import OrderedDict
from pyexcel_xls import save_data

#文件所在路径
path = r"E:\Users\lockon\Desktop\\"

#读取xml文件，如果xml文件编码有问题可能会读取出错
def getTree():
    tree = ET.parse(path + r"test.xml")
    return tree
    
#定义保存成xls文件的方法，最后遍历完成后调用
def saveOuput():
    save_data(path + "test.xls", xls_data)  

#Excel文件的内容用一个有序词典xls_data存放
xls_data = OrderedDict()
sheet1 = [[u"文章号", u"文章主题", u"年份", u"地区（国家）", u"期刊名", u"第一作者", u"合作作者", u"第一单位", u"合作单位", u"关键词", u"摘要"]]

tree = getTree()
#获取xml文件的根节点，这里根节点是PubmedArticleSet
root = tree.getroot()
#根节点下面是由若干个PubmedArticle节点组成的，每一个就是对应一篇文章的信息，用findall全部找出来
pubmedArticles = root.findall('PubmedArticle')

#遍历这些节点，获取所需要的信息
for pubmedArticle in pubmedArticles:
    #获取PubmedArticle下面的子节点MedlineCitation，
    medlineCitation = pubmedArticle.find('MedlineCitation')
    
    #初始化所有内容
    pmid = ''
    year = ''
    title = ''
    articleTitle = ''
    abstractText = ''
    firstAuthor = ''
    firstAffiliation = ''
    otherAuthors = ''
    otherAffiliation = ''
    country = ''
    keywords = ''
    
    #如果子节点 MedlineCitation存在，才有后面的操作，因为所需的内容全部都从这里拿
    if medlineCitation is not None:
        #如果MedlineCitation存在子节点PMID，读取其内容到变量pmid
        if medlineCitation.find('PMID') is not None:
            #文章号
            pmid = medlineCitation.find('PMID').text
    
        if medlineCitation.find('DateCreated') is not None:
            dateCreated = medlineCitation.find('DateCreated')
            if dateCreated.find('Year') is not None:
                #年份
                year = dateCreated.find('Year').text
        
        if medlineCitation.find('Article') is not None:
            article = medlineCitation.find('Article')
            if article.find('Journal') is not None:
                journal = article.find('Journal')
                if journal.find('Title') is not None: 
                    #期刊名
                    title = journal.find('Title').text
                    
            if article.find('ArticleTitle') is not None:
                #文章主题   
                articleTitle = article.find('ArticleTitle').text
        
            if article.find('Abstract') is not None:
                abstract = article.find('Abstract')
                if abstract.find('AbstractText') is not None:
                    #摘要
                    abstractText = abstract.find('AbstractText').text
        
            if article.find('AuthorList') is not None:
                if article.find('AuthorList').findall('Author') is not None:    
                    authorList = article.find('AuthorList').findall('Author')       
                    #遍历作者list
                    for i in range(len(authorList)):
                        #第一个节点Author的作者作为第一作者，对应的单位为第一单位
                        if i == 0:
                            firstAuthor = authorList[i].find('LastName').text + ' ' + authorList[i].find('ForeName').text
                            firstAffiliation = authorList[i].find('AffiliationInfo').find('Affiliation').text
                        #后面的节点都作为合作作者和合作单位
                        else:
                            #多个作者用逗号隔开
                            if len(otherAuthors) > 0:
                                otherAuthors += ', '
                            otherAuthors += authorList[i].find('LastName').text + ' ' + authorList[i].find('ForeName').text
                            currentAffiliation = authorList[i].find('AffiliationInfo').find('Affiliation').text
                            #如果当前这个作者的单位既不是第一单位，也不存在于合作单位，就加进合作单位里面
                            if currentAffiliation not in firstAffiliation and currentAffiliation not in otherAffiliation:
                                if len(otherAffiliation) > 0 :
                                    otherAffiliation += ', '
                                otherAffiliation += currentAffiliation
        
        if medlineCitation.find('MedlineJournalInfo') is not None:
            medlineJournalInfo = medlineCitation.find('MedlineJournalInfo')
            if medlineJournalInfo.find('Country') is not None:
                #国家
                country = medlineJournalInfo.find('Country').text
        
        if medlineCitation.find('KeywordList') is not None:
            if medlineCitation.find('KeywordList').findall('Keyword') is not None:
                keywordList = medlineCitation.find('KeywordList').findall('Keyword')
                #遍历关键词，每个关键词用分号隔开
                for keyword in keywordList:
                    if len(keywords) > 0:
                        keywords+= ';'
                    keywords += keyword.text
    
    #将每一篇文章所需信息装在一行，再装进Excel表单里面
    row_data = [pmid, articleTitle, year, country, title, firstAuthor, otherAuthors, firstAffiliation, otherAffiliation, keywords, abstractText]
    sheet1.append(row_data)

#将表单内容装进有序词典，也就是整个Excel的内容
xls_data.update({u"Result": sheet1})

#保存成文件
saveOuput()