#!/usr/bin/python
path = r"E:\Users\lockon\Desktop\\"
inputFileName = r"phone.txt"
ouputFileName = r"result.sql"

def readTXTFiles():
    f = open(path + inputFileName)
    lines = f.readlines()
    return lines

phoneList = readTXTFiles()

output = open(path + ouputFileName,'a', encoding='utf-8')
for phone in phoneList:
    phone = phone.strip()
    output.write('INSERT INTO ZQ_Target (Phone) VALUES (' + phone + ');\n')
output.close()