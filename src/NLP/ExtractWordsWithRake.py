from rake_nltk import Rake
from pyexcel_xls import get_data
from pyexcel_xls import save_data

r = Rake()
path = r"E:\Users\lockon\Desktop\\"
inputFileName = r"test.xlsx"
ouputFileName = r"result.xls"

def getExcelData():
    xls_data = get_data(path + inputFileName)
    return xls_data

def saveExcelData(sheet1):
    xls_data.update({u"Sheet1": sheet1})  
    save_data(path + ouputFileName, xls_data)


xls_data = getExcelData()

#遍历excel里面的表单，因为只有第一个有内容，所以循环一次就中止
for sheet_n in xls_data.keys():
    break
sheet1 = xls_data[sheet_n]

#遍历sheet1里面的每一行
for rowData in sheet1:
    if rowData is not None and len(rowData) > 0:
        #keywords用来存放第二列的结果，是一个list类型
        keywords = []
        #调用那个nltk的方法
        r.extract_keywords_from_text(rowData[0])
        #phrases就是它算出来的那些高分词
        phrases = r.get_ranked_phrases()
        #遍历每一个phrase
        for phrase in phrases:
            #每一个item分别放着phrase和它对应的出现次数，格式如[question,12]
            item = []
            item.append(phrase)
            #rowData[0]就是原文，rowData[0].lower()就是将原文全部转成小写，因为那些phase算出来全是小写的
            #rowData[0].lower().count(phrase)就是数一下phrase在原文里面出现了多少次，算完之后结果加到item里面
            item.append(rowData[0].lower().count(phrase))
            keywords.append(item)   
            
        #如果表单里面只有第一列有内容，就直接用append加在后面
        if len(rowData) == 1:
            rowData.append(str(keywords))
        #如果表单里面不止第一行有内容，就直接把结果写在第二列
        elif len(rowData) > 1:
            rowData[1] = str(keywords)

#保存结果
saveExcelData(sheet1)
