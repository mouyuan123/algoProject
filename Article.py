import re
import WordList


class Article:
    articleCount = 0  # Define the number of articles used for the project
    list = WordList.WordList("STOP", "Stop.txt")
    stopWordsList = list.wordList()

    #  Create instance of article
    def __init__(self, country, textFile, title):
        self.country = country
        self.textFile = textFile
        self.title = title
        Article.articleCount += 1
        Article.toString(self)

    # To extract all the words from the article and store inside an array
    # Time Complexity  = O(N) , where N = number of lines in an article
    def extractWords(self):
        array = []
        with open(self.textFile, "r", encoding="utf-8") as file:
            textLine = file.readline().lower()
            text = ""
            while textLine:
                textLine = re.sub(r'http\S+', '', textLine)  # Remove all the URL found inside the articles
                splitting = re.findall("[a-zA-Z'-]+", textLine)  # Extracts all the "words only" from the article (e.g., "you've" / "one-pointedness" are also acceptable)
                array = array + splitting
                textLine = file.readline().lower()
        Article.replace_all_stop_words(self, array, Article.stopWordsList)
        for i in range(len(array)):
            text += array[i]
        return text

    def replace_all_stop_words(self, articleWords, stopWordList):
        for i in range(len(articleWords)):
            if articleWords[i] in stopWordList:
                articleWords[i] = ""

    # Format and print out the article's sequence, country and title
    def toString(self):
        print("Article: %d%3s Country: %s%3s \nTitle => %s" % (Article.articleCount, " ", self.country, " ", self.title))
