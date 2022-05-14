import Article  # Import the class we created here to create its instances
import CompressedTrie
import WordList

list1 = WordList.WordList("POSITIVE", "Positive.txt")
positiveWordsList = list1.wordList()
print(positiveWordsList)
list2 = WordList.WordList("NEGATIVE", "Negative.txt")
negativeWordsList = list2.wordList()
print(negativeWordsList)
list3 = WordList.WordList("STOP", "Stop.txt")
stopWordsList = list3.wordList()
print(stopWordsList)
# article1 = Article.Article("Singapore", "SG-1.txt", "Getting Singapore in shape: Economic challenges and how to meet them")
# print(article1.extractWords())
# print(len(article1.extractWords()))
# article2 = Article.Article("Singapore", "SG-2.txt", "Economic Development and Social Integration: Singapore’s Evolving Social Compact")
# article1.toString()
# article2.toString()
compressedTrie = CompressedTrie.CompressedTrie()
for i in range(0, len(positiveWordsList)):
    compressedTrie.insert(positiveWordsList[i], "+")
for i in range(0, len(negativeWordsList)):
    compressedTrie.insert(negativeWordsList[i], "-")
for i in range(0, len(positiveWordsList)):
    print(compressedTrie.search(positiveWordsList[i]))
for i in range(0, len(negativeWordsList)):
    print(compressedTrie.search(negativeWordsList[i]))
# compressedTrie.insert('dog', '+')
# compressedTrie.insert('dock', '+')
# compressedTrie.insert('doggie', '-')
# # compressedTrie.insert('dock')
# # compressedTrie.insert('dead')
# print(compressedTrie._data)
# print(compressedTrie.search('dog'))
# print(compressedTrie.search('dock'))
# print(compressedTrie.search('doggie'))

