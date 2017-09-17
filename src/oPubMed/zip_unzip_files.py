# -*- encoding: utf-8 -*-

import os

# 从zip文件解包
import zipfile

for root, dir, files in os.walk(r'E:\Datasets\Dataset_Medical\Dataset - PubMed'):
# for root, dir, files in os.walk(r'/home/titan/Documents/Tony/PubMed/Dataset_PubMed'):
    for f in files:
        if f.endswith(".zip"):
            fdin = os.path.join(root, f)
            zfile = zipfile.ZipFile(fdin, 'r')
            for filename in zfile.namelist():
                data = zfile.read(filename)
                file = open(filename, 'w+b')
                file.write(data)
                file.close()

# 把整个文件夹内的文件打包
# import zipfile
#
# f = zipfile.ZipFile('archive.zip', 'w', zipfile.ZIP_DEFLATED)
# startdir = "c:\\mydirectory"
# for dirpath, dirnames, filenames in os.walk(startdir):
#     for filename in filenames:
#         f.write(os.path.join(dirpath, filename))
# f.close()
