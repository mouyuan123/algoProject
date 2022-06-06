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
        # Remove all the punctuation from the article and make the words to lowercase (consistency)
        word_list = soup.get_text().translate(str.maketrans('', '', string.punctuation)).lower().split()
        # print(word_list)
        # Filter out all the stop words before making it a long text
        Article.replace_all_stop_words(self, word_list, Article.stopWordsList)
        # Combine the article as a long text before finding the positive and negative words
        articleText = ''.join(word_list)
        # print(articleText)
        return articleText

    def replace_all_stop_words(self, articleWords, stopWordList):
        for i in range(len(articleWords)):
            if articleWords[i] in stopWordList:
                articleWords[i] = ""

    # Format and print out the article's sequence, country and title
    def toString(self):
        print(
            "Article: %d%3s Country: %s%3s" % (Article.articleCount, " ", self.country, " "))
