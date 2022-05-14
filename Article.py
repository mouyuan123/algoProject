import re


class Article:
    articleCount = 0  # Define the number of articles used for the project

    #  Create instance of article
    def __init__(self, country, textFile, title):
        self.country = country
        self.textFile = textFile
        self.title = title
        Article.articleCount += 1

    # To extract all the words from the article and store inside an array
    # Time Complexity  = O(N) , where N = number of lines in an article
    def extractWords(self):
        array = []
        with open(self.textFile, "r", encoding="utf-8") as file:
            textLine = file.readline()
            while textLine:
                textLine = re.sub(r'http\S+', '', textLine)  # Remove all the URL found inside the articles
                splitting = re.findall("[a-zA-Z']+", textLine)  # Extracts all the "words only" from the article
                array = array + splitting
                textLine = file.readline()
        unique = Article.removeRedundantWords(self, array)
        return unique

    # To remove all the repeated words extracted from the article (e.g., no 2 words, "good" occur in the array
    # Time Complexity = O(N+1), where N = length of the array and 0(1) is when we search an element using "not in" in a set
    def removeRedundantWords(self, array):
        constArrayWord = []
        unique = set()
        for i in range(0, len(array)):
            if array[i] not in unique:
                unique.add(array[i])
                constArrayWord.append(array[i])
        return constArrayWord

    # Format and print out the article's sequence, country and title
    def toString(self):
        print("Article: %d%3s Country: %s%3s \nTitle => %s\n" % (Article.articleCount, " ", self.country, " ", self.title))
