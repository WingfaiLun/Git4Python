from rake_nltk import Rake
from pyexcel_xls import get_data
from pyexcel_xls import save_data
from textblob import TextBlob

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
    
    blob = TextBlob(rowData[0])
    phrases = blob.noun_phrases
    
    keywords = []
    for phrase in phrases:
        item = []
        item.append(phrase)
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


