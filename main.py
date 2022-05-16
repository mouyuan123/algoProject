import re
import Article  # Import the class we created here to create its instances
import CompressedTrie
import AhoCorasick
import WordList


# Build array of positive, negative and neutral words
def listofWords(sentiment, wordTxt):
    list = WordList.WordList(sentiment, wordTxt)
    return list.wordList()


# Process to extract words, filter out stop words and concatenate all the words into one text from each article using Article class
def preprocessArticle(country, articleTxt, articleTitle, positiveList, negativeList, neutralList, dictionary):
    article = Article.Article(country, articleTxt, articleTitle)
    text = article.extractWords()
    justifySentiment(country, text, positiveList, negativeList, neutralList, dictionary)


# Check how many positive & negative & neutral words in each article using AHO-CORASICK algorithm
def justifySentiment(country, processedTxt, positiveList, negativeList, neutralList, dictionary):
    positveNo = AhoCorasick.process(positiveList, processedTxt)
    AhoCorasick.clear_Trie()
    negativeNo = AhoCorasick.process(negativeList, processedTxt)
    AhoCorasick.clear_Trie()
    neutralNo = AhoCorasick.process(neutralList, processedTxt)
    AhoCorasick.clear_Trie()
    dictionary[country][0] = dictionary[country][0] + positveNo  # Accumulate the positive words of the country
    dictionary[country][1] = dictionary[country][1] + negativeNo  # Accumulate the negative words of the country
    print("The length of text (excluding stop words) in the article: " + str(len(processedTxt)))
    print("Total positive words in this article: " + str(positveNo) + "\n" + "Total negative words in this article: " + str(negativeNo)+"\n" + "Total neutral words in this article: " + str(neutralNo))
    if positveNo > negativeNo:
        print("Since the positive words is more than the negative words, this article gives "+country+" a positive sentiment\n")
    elif positveNo < negativeNo:
        print("Since the negative words is more than the positive words, this article gives " + country + " a negative sentiment\n")
    else:
        print("Since the positive words and the negative words are equal, this article gives " + country + " a neutral sentiment\n")


# To find out the most appropriate country to have store expansion based on the positive sentiments among countries
def expandBranch(ranking):
    mostValuableCountry = ""
    mostPositiveWords = 0
    for country, sentiments in ranking.items():
        print("For "+country+", the overall positive words are "+str(sentiments[0])+" while the overall negative words are "+str(sentiments[1]))
        if sentiments[0] > mostPositiveWords:
            mostValuableCountry = country
            mostPositiveWords = sentiments[0]
    print("In conclusion, " + mostValuableCountry + " is the worth having branch expansion as it has total of " + str(mostPositiveWords) + " positive words (the most positive sentiment)\n")


# Build an array of positive words using WordList class
positiveWordsList = listofWords("POSITIVE", "Positive.txt")
# Build an array of negative words using WordList class
negativeWordsList = listofWords("NEGATIVE", "Negative.txt")
# Build an array of negative words using WordList class
neutralWordsList = listofWords("NEUTRAL", "Neutral.txt")
# Build a dictionary to store the overall number of positive and negative words of each country for ranking
# The index 0 store the amount of positive words & the index 1 store the amount of negative words
rank = {"Malaysia": [0, 0],
        "United States": [0, 0],
        "Singapore": [0, 0],
        "Taiwan": [0, 0],
        "Japan": [0, 0]
        }
# Store the 25 articles in an array before processing
articles = [
    ["Singapore", "SG-1.txt", "Getting Singapore in shape: Economic challenges and how to meet them"],
    ["Singapore", "SG-2.txt", "Economic Development and Social Integration: Singapore’s Evolving Social Compact"],
    ["Singapore", "SG-3.txt", "Singapore’s economic situation is ‘dire’ as global coronavirus resurgence looms, central bank says"],
    ["Singapore", "SG-4.txt", "Singapore economy grows 3.4% in Q1, slower than previous quarter"],
    ["Singapore", "SG-5.txt", "Singapore's economic growth to hit 3% to 5% in 2022; inflation still a pressing concern"]
]
# Process the 25 articles we found to find the most appropriate country to expan branch
for numOfArticle in range(len(articles)):
    preprocessArticle(articles[numOfArticle][0], articles[numOfArticle][1], articles[numOfArticle][2], positiveWordsList, negativeWordsList, neutralWordsList, rank)

# Find out the most worth country to have the store expansion according to the positive & negative sentiment
expandBranch(rank)

print("However, it is also necessary for us to check the distributed geographical locations in the country\nto determine" +
      " the local distributed centre in the country to optimize the delivery cost if we want expand our stores in that country")

# compressedTrie = CompressedTrie.CompressedTrie()
# for i in range(0, len(positiveWordsList)):
#     compressedTrie.insert(positiveWordsList[i], "+")
# for i in range(0, len(negativeWordsList)):
#     compressedTrie.insert(negativeWordsList[i], "-")
# for i in range(0, len(positiveWordsList)):
#     print(compressedTrie.search(positiveWordsList[i]))
# for i in range(0, len(negativeWordsList)):
#     print(compressedTrie.search(negativeWordsList[i]))
# compressedTrie.insert('dog', '+')
# compressedTrie.insert('dock', '+')
# compressedTrie.insert('doggie', '-')
# # compressedTrie.insert('dock')
# # compressedTrie.insert('dead')
# print(compressedTrie._data)
# print(compressedTrie.search('dog'))
# print(compressedTrie.search('dock'))
# print(compressedTrie.search('doggie'))
