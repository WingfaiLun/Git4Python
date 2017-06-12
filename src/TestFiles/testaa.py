firstRow = [1, 2, 3, 5, 6]
row = ["a", "b", "c", "e"]
rod = ["a", "b", "c", "d", "e", "f", "g"]
filePath = r'E:\Users\lockon\Desktop\'
sheet = []
sheet.append(row)
sheet.append(row)
sheet.append(rod)

changedIndex = 0
while len(row) < len(rod):
    for i in range(len(row)):
        if row[i] != rod[i]:
            changedIndex = i
            break
    if changedIndex != 0:
        row.insert(changedIndex, rod[changedIndex])
    else:
        row.append(rod[-1])
    changedIndex = 0   
    print(row) 
print(sheet)

aa = ["a", "b", "c", "e"]
aa.insert(len(aa), "f")
print(aa)
