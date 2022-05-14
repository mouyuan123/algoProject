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
        if sentiment == "POSITIVE" or sentiment == "NEGATIVE":
            with open(self.textFile, "r", encoding="utf-8") as file:
                textLine = file.readline().lower()
                splitting = re.split(r",\s+", textLine)
                array = array + splitting
                if sentiment == "POSITIVE":
                    # Append all the positive words with "+"
                    for i in range(0, len(array)):
                        array[i] = array[i] + "+"
                else:
                    # Append all the negative words with "-"
                    for i in range(0, len(array)):
                        array[i] = array[i] + "-"
        elif sentiment == "STOP":
            with open(self.textFile, "r", encoding="utf-8") as file:
                textLine = file.readline().lower()
                splitting = textLine.split()
                array = array + splitting
        else:
            print("Please insert valid input (POSITIVE / NEGATIVE / STOP)")
        return array
