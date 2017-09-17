#!/usr/bin/python
from pyexcel_xls import get_data
from pyexcel_xls import save_data
import re, time

path = r"C:\Users\Administrator\Desktop\\"
inputFileName = r"address.xlsx"
ouputFileName = r"address_output.xls"  #保存的时候只能保存xls格式..

#读取excel里面第一个表单的内容
def getDataFromXLSX(path, fileName):
    excelData = get_data(path + fileName) 
    return excelData

#保存处理后的内容到excel文件
def saveDataToXLSX(path, fileName, excelData):
    save_data(path + fileName, excelData)  

def extractData(excelData):
    #要转化的内容放在excel的第一个表单，所以只循环一次就终止
    for sheet_n in excelData.keys():
        break
    sourceData = excelData[sheet_n]
    
    #初始化存放结果的表单
    sheetFormat1 = [[u"序号", u"作者", u"单位", u"国家"]]
    sheetFormat2 = []

    #excel第一行是表头之类的内容，不在处理范围，所以从1(就是第二行)开始循环
    for rowIndex in range(1, len(sourceData)):
        #sourceData[row]这里row是行数，sourceData[row]表示源数据第rowIndex行的内容
        tempSource = sourceData[rowIndex]
        
        if len(tempSource) > 1:
            infoList = tempSource[1].split(" / ")
            #organizationList存放单位
            organizations = ""
            #info像这样: [McDougall, Matthew A.; Walsh, Michael; Water, Kristina; Knigge, Ryan; Miller, Lindsey; Steverrner, Michalene] Univ South Dakota, Sanford Sch Med, Dept Psychiat, Sioux Falls, SD USA.
            for info in infoList:
                #infoWithoutAuthor像这样: Univ South Dakota, Sanford Sch Med, Dept Psychiat, Sioux Falls, SD USA.
                infoWithoutAuthor = re.sub(r'\[.*?]', '', info).strip()
                #organization像这样: Univ South Dakota
                organization = infoWithoutAuthor.split(", ")[0]
                if organization not in organizations:
                    organizations += organization + " ; "
                #country像这样: USA
                country = infoWithoutAuthor.split(", ")[-1].strip(".")
                if 'USA' in country:
                    country = 'USA'
                
                if re.match(r"\[.*?]", info):
                    #authorList像这样: ["McDougall, Matthew A.", "Walsh, Michael", "Water, Kristina", "Knigge, Ryan", "Miller, Lindsey", "Steverrner, Michalene"]
                    authorList = re.findall( r"\[.*?]", info)[0].split("; ")   
                    #author像这样: McDougall, Matthew A.
                    for author in authorList:
                        author = author.replace("[", "").replace("]", "")
                        #格式1
                        tempFormat1 = [rowIndex, author, organization, country]
                        sheetFormat1.append(tempFormat1)
            
            #格式2
            tempFormat2 = [rowIndex]
            #单位字符串要去掉最后的分号" ; "
            tempFormat2.append(organizations[:-3])
            sheetFormat2.append(tempFormat2)

    excelData.update({u"格式1": sheetFormat1})      
    excelData.update({u"格式2": sheetFormat2})          

if __name__ == '__main__':
    start = time.clock()
    print("Start to extract data from " + path + inputFileName)
    #读取源数据
    excelData = getDataFromXLSX(path, inputFileName)
    print("Processing...")
    #提取数据
    extractData(excelData)
    #保存数据到文件
    saveDataToXLSX(path, ouputFileName, excelData)
    end = time.clock()
    print("Completed in " + str(end - start) + "s")