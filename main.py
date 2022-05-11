import re

array = []
with open("testing.txt", "r", encoding="utf-8") as file:
    textLine = file.readline()
    while textLine:
        splitting = re.findall("[a-zA-Z']+", textLine)
        array = array + splitting
        textLine = file.readline()
print(array)
print(len(array))

array2 = []
with open("testing2(positive).txt", "r", encoding="utf-8") as file:
    textLine = file.readline()
    while textLine:
        splitting = re.split(r",\s+", textLine)
        array2 = array2 + splitting
        textLine = file.readline()
print(array2)
count = 0
for i in range(0, len(array2)):
    count += len(array2[i].split())
print(count)

array3 = []
with open("stop-words.txt", "r", encoding="utf-8") as file:
    textLine = file.readline()
    while textLine:
        splitting = textLine.split();
        array3 = array3 + splitting
        textLine = file.readline()
print(array3)
print(len(array3))
