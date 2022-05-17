import os
import re
import Article  # Import the class we created here to create its instances
import CompressedTrie
import AhoCorasick
import WordList
import plotlyGraph


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
    dictionary[country][2] = dictionary[country][2] + neutralNo  # Accumulate the neutral words of the country
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
    leastDifference = 0
    for country, sentiments in ranking.items():
        print("For "+country+", the overall positive words are "+str(sentiments[0])+" while the overall negative words are "+str(sentiments[1]))
        if sentiments[0] - sentiments[1] > leastDifference:
            mostValuableCountry = country
            leastDifference = sentiments[0] - sentiments[1]
    print("In conclusion, " + mostValuableCountry + " is the worth having branch expansion as it has the least difference, " + str(leastDifference) + " between overall positive and negative words\n")


# Build an array of positive words using WordList class
positiveWordsList = listofWords("POSITIVE", "words\\Positive.txt")
# Build an array of negative words using WordList class
negativeWordsList = listofWords("NEGATIVE", "words\\Negative.txt")
# Build an array of negative words using WordList class
neutralWordsList = listofWords("NEUTRAL", "words\\Neutral.txt")
# Build a dictionary to store the overall number of positive and negative words of each country for ranking
# The index 0 store the amount of positive words & the index 1 store the amount of negative words & the index 2 store the amount of neutral words
rank = {"Malaysia": [0, 0, 0],
        "United State": [0, 0, 0],
        "Singapore": [0, 0, 0],
        "Taiwan": [0, 0, 0],
        "Japan": [0, 0, 0]
        }
# Store the 25 articles in an array before processing
articles = [
    ["Singapore", "articles\\SG-1.txt", "Getting Singapore in shape: Economic challenges and how to meet them"],
    ["Singapore", "articles\\SG-2.txt", "Economic Development and Social Integration: Singapore’s Evolving Social Compact"],
    ["Singapore", "articles\\SG-3.txt", "Singapore’s economic situation is ‘dire’ as global coronavirus resurgence looms, central bank says"],
    ["Singapore", "articles\\SG-4.txt", "Singapore economy grows 3.4% in Q1, slower than previous quarter"],
    ["Singapore", "articles\\SG-5.txt", "Singapore's economic growth to hit 3% to 5% in 2022; inflation still a pressing concern"],

    ["Malaysia", "articles\\MY-1.txt", "Key Statistics of Labour Force in Malaysia, January 2022"],
    ["Malaysia", "articles\\MY-2.txt", "A Full Guide on Safety in Malaysia"],
    ["Malaysia", "articles\\MY-3.txt", "OECD forecasts Malaysia economy to grow 6% in 2022"],
    ["Malaysia", "articles\\MY-4.txt", "Malaysia's economy to grow strongly in 2022, says Amro"],
    ["Malaysia", "articles\\MY-5.txt", "Socio-Economic Research Centre: A better year in 2022 for Malaysian economy"],

    ["United State", "articles\\US-1.txt", "Most Americans Say the Current Economy Is Helping the Rich, Hurting the Poor and Middle Class"],
    ["United State", "articles\\US-2.txt", "The rapid growth the U.S. economy has seen is about to hit a wall"],
    ["United State", "articles\\US-3.txt", "U.S. Economic Outlook"],
    ["United State", "articles\\US-4.txt", "If the Economy Is Doing So Well, Why Does It Feel Like a Disaster?"],
    ["United State", "articles\\US-5.txt", "The Economic Situation, March 2022"],

    ["Taiwan", "articles\\TW-1.txt", "Taiwan’s inflation rate reaches 3.38% in April"],
    ["Taiwan", "articles\\TW-2.txt", "Food/beverage sales for 2021 affected by COVID-19, down over 6%"],
    ["Taiwan", "articles\\TW-3.txt", "Taiwan Faces Largest COVID-19 Outbreak Yet"],
    ["Taiwan", "articles\\TW-4.txt", "Taiwan will not 'cruelly' lock down like China: premier"],
    ["Taiwan", "articles\\TW-5.txt", "Taiwan Economics in Brief – May 2022"],

    ["Japan", "articles\\JP-1.txt", "The societal pressures that shape Japan"],
    ["Japan", "articles\\JP-2.txt", "Japan headed for uneven recovery in the first half"],
    ["Japan", "articles\\JP-3.txt", "3 Economic Challenges Facing Japan in 2022"],
    ["Japan", "articles\\JP-4.txt", "JAPAN: ECONOMIC AND POLITICAL OUTLINE"],
    ["Japan", "articles\\JP-5.txt", "Japan's Economy and Its Impact on the U.S. Economy"]
]
# Process the 25 articles we found to find the most appropriate country to expan branch
for numOfArticle in range(len(articles)):
    preprocessArticle(articles[numOfArticle][0], articles[numOfArticle][1], articles[numOfArticle][2], positiveWordsList, negativeWordsList, neutralWordsList, rank)

# Find out the most worth country to have the store expansion according to the positive & negative sentiment
expandBranch(rank)

# Import the data of positive, negative and neutral words as .csv file to build chart
#  Data needed in sequence: country name, overall positive words, overall negative words, overall neutral words
for i, j in rank.items():
    plotlyGraph.buil_csv_file(i, j[0], j[1], j[2])

print("However, it is also necessary for us to check the distributed geographical locations in the country\nto determine" +
      " the local distributed centre in the country to optimize the delivery cost if we want expand our stores in that country")
