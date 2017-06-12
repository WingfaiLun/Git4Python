#!/usr/bin/python
#encoding=UTF-8
import urllib.request
import re

index = 0
regexPage = re.compile(r'http://news.*?html')
regexPageTitle = re.compile(r'headline">.*</h1>') 
regexPageContent = re.compile(r'articleBody">[\s\S]*?</script></div>')
regexChineseChar = re.compile(r'[－{2})|(（）)|(【】)|({})|(《》]*\d*[\u4e00-\u9fa5].*?</p>')

sourceUrl = "http://news.sohu.com"
sourceCode = urllib.request.urlopen(sourceUrl).read()
sourceCode = sourceCode.decode('gbk')

pageAddresslist = re.findall(regexPage, sourceCode)
pageAddresslist = list(set(pageAddresslist))

for url in pageAddresslist:
    print(url)
    pageSourceCode = urllib.request.urlopen(url).read()
    try:
        pageSourceCode = pageSourceCode.decode('gbk')
    except Exception as e:
        print ('found exception: ' + str(e))
        pageSourceCode = pageSourceCode.decode('utf-8')

    tempTitle = re.findall(regexPageTitle, pageSourceCode)
    tempContent = re.findall(regexPageContent, pageSourceCode)
    content = ''
    if len(tempTitle) > 0 and len(tempContent) > 0:
        tempTitle = tempTitle[0].replace(u'headline">', '')
        tempTitle = tempTitle.replace(u'</h1>', '')
        tempContent = tempContent[0].replace(u'\u3000', '')
        tempContent = re.findall(regexChineseChar, tempContent)
        index += 1
        content = str(index) + ': ' + tempTitle + '\n'
        for contentItem in tempContent:
            contentItem = contentItem.replace(u'</p>', '')
            contentItem = contentItem.replace(u'</strong>', '')
            content += contentItem + '\n'
    
    if len(content) > 0:
        f = open(r"E:\Users\lockon\Desktop\test.txt",'a')
        f.write(content + '\n')
        f.close()
    print(content)