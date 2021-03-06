#!/usr/bin/python
from xml.etree import cElementTree
from collections import OrderedDict
from pyexcel_xls import save_data
import re

#文件所在路径
path = r"E:\Users\lockon\Desktop\\"
txtFileName = r"644.txt"
xmlFileName = r"644.xml"
ouputFileName = r"644.xls"

#读取xml文件，如果xml文件编码有问题可能会读取出错
def getPubmedArticlesFromXML():
    tree = cElementTree.parse(path + xmlFileName)
    #获取xml文件的根节点，这里根节点是PubmedArticleSet
    root = tree.getroot()
    #根节点下面是由若干个PubmedArticle节点组成的，每一个就是对应一篇文章的信息，用findall全部找出来
    pubmedArticles = root.findall('PubmedArticle')
    return pubmedArticles

#以utf-8编码读取源文件的所有字节
def getArticlesFromTXT():
    f = open(path + txtFileName, 'r', encoding='utf-8').read()
    regexArticle = re.compile(r'PMID[\s\S]*?PL  - ')
    #articles就是所有文章的集合
    articles = re.findall(regexArticle, f)
    return articles

#定义保存成xls文件的方法，最后遍历完成后调用
def saveOuput(sheet1):
    #Excel文件的内容用一个有序词典xls_data存放
    xls_data = OrderedDict()
    #将表单内容装进有序词典，也就是整个Excel的内容
    xls_data.update({u"Result": sheet1})
    save_data(path + ouputFileName, xls_data)  

#遍历这些节点，获取所需要的信息
def extractXML(pubmedArticles, sheet1):
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
        language = ''
        publicationType = ''
#         MedlineJournalCOUNTRY = ''
        authorAffiliation = ''
        webAuthor = ''
        journalName = ''
        meshHeadings = ''
        
        #如果子节点 MedlineCitation存在，才有后面的操作，因为所需的内容全部都从这里拿
        if medlineCitation is not None:
            #如果MedlineCitation存在子节点PMID，读取其内容到变量pmid
            if medlineCitation.find('PMID') is not None:
                #文章号
                pmid = medlineCitation.find('PMID').text
        
            if medlineCitation.find('Article') is not None:
                article = medlineCitation.find('Article')
                if article.find('Journal') is not None:
                    journal = article.find('Journal')
                    if journal.find('Title') is not None: 
                        #期刊名
                        title = journal.find('Title').text
                    if journal.find('ISOAbbreviation') is not None:
                        journalName = journal.find('ISOAbbreviation').text
                    if journal.find('JournalIssue') is not None and journal.find('JournalIssue').find('PubDate') is not None and journal.find('JournalIssue').find('PubDate').find('Year') is not None:
                        year = journal.find('JournalIssue').find('PubDate').find('Year').text
                if article.find('ArticleTitle') is not None:
                    #文章主题   
                    articleTitle = article.find('ArticleTitle').text
            
                if article.find('Abstract') is not None:
                    abstract = article.find('Abstract')
                    abstractList = abstract.findall('AbstractText')
                    if abstractList is not None:
                        #摘要
                        for abstractItem in abstractList: 
                            if abstractItem.text is not None:
                                if len(abstractText) > 0:
                                    abstractText = abstractText + '\n' + abstractItem.text
                                else:
                                    abstractText = abstractItem.text
            
                if article.find('AuthorList') is not None:
                    if article.find('AuthorList').findall('Author') is not None:    
                        authorList = article.find('AuthorList').findall('Author')       
                        #遍历作者list
                        for i in range(len(authorList)):
                            #第一个节点Author的作者作为第一作者，对应的单位为第一单位
                            if authorList[i].find('LastName') is not None:
                                currentAuthor = authorList[i].find('LastName').text
                            else:
                                print("名字都没有：" + pmid)
                            if authorList[i].find('ForeName') is not None: 
                                foreName = authorList[i].find('ForeName').text
                                foreNames = foreName.split(" ")
                                name = ""
                                if len(foreNames) > 1 :   
                                    for nameItem in foreNames:
                                        name = name + nameItem[0]
                                else:
                                    name = foreName
                                currentAuthor += " " + name
                            affiliations = authorList[i].findall('AffiliationInfo')
                            currentAffiliation = ''
                            cleanAffiliations = []
                            for affiliationItem in affiliations:
                                if len(currentAffiliation) > 0 :
                                    currentAffiliation += " / "
                                affiliationItemText = affiliationItem.find('Affiliation').text
                                if affiliationItemText[len(affiliationItemText) - 1] == "." :
                                    affiliationItemText = affiliationItemText[:-1]
                                reg = r"[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}"
                                affiliationWithoutMail = re.sub(reg, '', affiliationItemText)
                                if len(affiliationWithoutMail) < len(affiliationItemText):
                                    if affiliationWithoutMail[len(affiliationWithoutMail) - 2 :] == ". " :
                                        affiliationWithoutMail = affiliationWithoutMail[:-2]
                                    if len(webAuthor) > 0:
                                        if currentAuthor not in webAuthor:
                                            webAuthor += " ; " + currentAuthor
                                    else:
                                        webAuthor += currentAuthor
                                    affiliationItemText = affiliationWithoutMail
                                cleanAffiliations.append(affiliationItemText)
                                currentAffiliation += affiliationItemText
                                
                            if i == 0:
                                firstAuthor = currentAuthor
                                firstAffiliation = currentAffiliation
                                if len(currentAffiliation.strip()) > 0:
                                    authorAffiliation = currentAuthor + " : " + currentAffiliation
                                else:
                                    authorAffiliation = currentAuthor
                            #后面的节点都作为合作作者和合作单位
                            else:
                                #多个作者用逗号隔开
                                if len(otherAuthors) > 0 :
                                    otherAuthors += ' ; ' + currentAuthor
                                else :
                                    otherAuthors = currentAuthor
                                #如果当前这个作者的单位既不是第一单位，也不存在于合作单位，就加进合作单位里面
                                for affiliationItemText in cleanAffiliations:
                                    if affiliationItemText not in firstAffiliation and affiliationItemText not in otherAffiliation:
                                        if len(otherAffiliation) > 0 :
                                            otherAffiliation += ' ; ' + affiliationItemText
                                        else :
                                            otherAffiliation = affiliationItemText
                                if len(currentAffiliation.strip()) > 0:    
                                    authorAffiliation = authorAffiliation + " ; " + currentAuthor + " : " + currentAffiliation
                                else:
                                    authorAffiliation = authorAffiliation + " ; " + currentAuthor
                                
                if article.find('Language') is not None:
                    language = article.find('Language').text
                
                if article.find('PublicationTypeList') is not None:
                    publicationTypeList = article.find('PublicationTypeList').findall('PublicationType')
                    for publicationTypeItem in publicationTypeList:
                        if len(publicationType) > 0:
                            publicationType = publicationType + " ; " + publicationTypeItem.text
                        else:
                            publicationType = publicationTypeItem.text
                            
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
                            keywords+= ' ; '
                        keywords += keyword.text
            
            if medlineCitation.find('MeshHeadingList') is not None:
                if medlineCitation.find('MeshHeadingList').findall('MeshHeading') is not None:
                    meshHeadingList = medlineCitation.find('MeshHeadingList').findall('MeshHeading')
                    for meshHeading in meshHeadingList:
                        if meshHeading.find("DescriptorName") is not None:
                            if len (meshHeadings) > 0:
                                meshHeadings += ' ; '
                            meshHeadings += meshHeading.find("DescriptorName").text
                            
        #将每一篇文章所需信息装在一行，再装进Excel表单里面
        row_data = [pmid, articleTitle, year, country, title, journalName, firstAuthor, otherAuthors, firstAffiliation, otherAffiliation, keywords, abstractText, language, publicationType, country, authorAffiliation, webAuthor, meshHeadings]
        sheet1.append(row_data)

def extractTXT(articles, sheet1):
    articleIndex = 1
    
    #遍历所有文章的集合，一个个处理
    for article in articles:
        #作者-机构合并后的结果
        authorAffiliation = ''
        #是不是第一条作者的记录
        isFirstAuthor = True
        #是不是第一条AD的记录
        isFirstAD = True
        #当前的标签
        currentIndex = ''
        
        articleLines = article.split('\n')
        for line in articleLines:
            if re.match(r'PMID- ', line):
                currentIndex = 'PMID'
            elif re.match(r'TI  - ', line):
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
                    if currentIndex == 'AD':
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
                continue
                
        sheet1[articleIndex].append(authorAffiliation)
        articleIndex += 1

if __name__ == '__main__':
    sheet1 = [[u"文章号", u"文章主题", u"年份", u"地区（国家）", u"期刊名", "Journal-ab", u"第一作者", u"合作作者", u"第一单位", u"合作单位", u"关键词", u"摘要", "Language", "PublicationType", "MedlineJournalCOUNTRY", u"作者-机构", u"通讯作者", u"MeshHeading", u"作者-机构1"]]
    
    #读取xml文件的内容，输出到sheet1中
    pubmedArticles = getPubmedArticlesFromXML()
    print("The number of articles in XML is: " + str(len(pubmedArticles)))
    extractXML(pubmedArticles, sheet1)
    
    #读取txt文件的内容，输出到sheet1中
    articles = getArticlesFromTXT()
    print("The number of articles in TXT is: " + str(len(articles)))
    extractTXT(articles, sheet1)
    
    #保存sheet1成excel文件
    saveOuput(sheet1)