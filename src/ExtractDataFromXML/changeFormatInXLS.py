#!/usr/bin/python
from pyexcel_xls import get_data
from pyexcel_xls import save_data

#读取excel内容
xls_data = get_data(r"E:\Users\lockon\Desktop\00.xls")

#要转化的内容放在excel的第一个表单，所以只循环一次就终止
for sheet_n in xls_data.keys():
    print(sheet_n, ":", xls_data[sheet_n])
    break
#第一个表单的内容:[[101, '喜欢', '讨厌', '热爱'], [102, '号', '大学'], [103, '得到', '啊啊', '啊']]
sheet_source = xls_data[sheet_n]

#初始化存放结果的表单
sheet_result = []
#表单内容是list格式，excel里面每一行作为一个元素,就是item_n, 如:[101, '喜欢', '讨厌', '热爱']
for item_n in sheet_source:
    #每一行也是list格式，这里只是遍历的方式不一样
    for i in range(len(item_n)): 
        #因为第一个放的是序号要跳过
        if i != 0 :
            #初始化每一行的内容，格式如: [101, '喜欢']
            row_data = [item_n[0], item_n[i]]
            #加入每一行的内容到结果表单里面
            sheet_result.append(row_data)
            #print只是打日志出来看一下，并不是修改excel的操作
            print(row_data)

#把转换后的结果保存在整个excel数据里面
xls_data.update({u"Result": sheet_result})  

# 保存成xls文件  
save_data(r"E:\Users\lockon\Desktop\00.xls", xls_data)  