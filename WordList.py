import re


class WordList:

    # Create instance of wordlist
    def __init__(self, sentiment, textFile):
        self.sentiment = sentiment
        self.textFile = textFile

    # Check whether it is a positive words list / negative words list / stop words list & return the array of words depending on their type
    def wordList(self):
        sentiment = self.sentiment
        array = []
        # If the text file contains positive / negative words, the dealing method is same
        if sentiment == "POSITIVE" or sentiment == "NEGATIVE" or sentiment == "NEUTRAL":
            with open(self.textFile, "r", encoding="utf-8") as file:
                textLine = file.readline().lower()
                splitting = re.split(r",\s+", textLine)
                array = array + splitting
            for i in range(len(array)):
                array[i] = array[i].replace(" ", "")
        elif sentiment == "STOP":
            with open(self.textFile, "r", encoding="utf-8") as file:
                textLine = file.readline().lower()
                while textLine:
                    splitting = textLine.split()
                    array = array + splitting
                    textLine = file.readline().lower()
        else:
            print("Please insert valid input (POSITIVE / NEGATIVE / STOP)")
        uniqueWordList = set(array)  # So that we can retrieve the word in 0(1) instead of O(n) if array is used
        return uniqueWordList
