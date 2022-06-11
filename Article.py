import string
import requests
from bs4 import BeautifulSoup
import WordList


class Article:
    articleCount = 0  # Define the number of articles used for the project
    list = WordList.WordList("STOP", "words\\Stop.txt")
    stopWordsList = list.wordList()

    #  Create instance of article
    def __init__(self, country):
        self.country = country
        Article.articleCount += 1
        Article.toString(self)

    def extract_words_from_url(self, url):
        # Retrieve the complete HTML codes from the website
        articleHTML = requests.get(url).text
        # html.parser feature allows us to create instance of BeautifulSoup and carry out certain functions
        soup = BeautifulSoup(articleHTML, 'html.parser')
        # Remove the punctuation and stop words from the article word array and join back as a long text string
        articleText = ''.join(Article.replace_all_stop_words(self, soup.get_text().translate(
            str.maketrans('', '', string.punctuation)).lower().split(), Article.stopWordsList))
        # print(articleText)
        return articleText

    def replace_all_stop_words(self, articleWords, stopWordList):
        for i in range(len(articleWords)):
            if articleWords[i] in stopWordList:
                articleWords[i] = ""
        return articleWords

    # Format and print out the article's sequence, country and title
    def toString(self):
        print(
            "Article: %d%3s Country: %s%3s" % (Article.articleCount, " ", self.country, " "))
