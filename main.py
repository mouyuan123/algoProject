import Article  # Import the class we created here to create its instances
import re

article1 = Article.Article("Singapore", "SG-1.txt", "Getting Singapore in shape: Economic challenges and how to meet them")
print(article1.extractWords())
print(len(article1.extractWords()))
article2 = Article.Article("Singapore", "SG-2.txt", "Economic Development and Social Integration: Singapore’s Evolving Social Compact")
article1.toString()
article2.toString()


#
# array2 = []
# with open("Positive.txt", "r", encoding="utf-8") as file:
#     textLine = file.readline()
#     while textLine:
#         splitting = re.split(r",\s+", textLine)
#         array2 = array2 + splitting
#         textLine = file.readline()
# print(array2)
# count = 0
# for i in range(0, len(array2)):
#     count += len(array2[i].split())
# print(count)
#
# array3 = []
# with open("Stop.txt", "r", encoding="utf-8") as file:
#     textLine = file.readline()
#     while textLine:
#         splitting = textLine.split();
#         array3 = array3 + splitting
#         textLine = file.readline()
# print(array3)
# print(len(array3))
