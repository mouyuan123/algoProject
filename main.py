import Article  # Import the class we created here to create its instances
import AhoCorasick
import WordList
import plotlyDash
import pandas as pd  # Import the excel files
import distributionCentre
import probabilityCalculation
import plotly.graph_objects as go


# Build array of positive, negative and neutral words
def listofWords(sentiment, wordTxt):
    list = WordList.WordList(sentiment, wordTxt)
    return list.wordList()


# Process to extract words, filter out stop words and concatenate all the words into one text from each article using Article class
def preprocessArticle(country, URL, positiveList, negativeList, neutralList, dictionary):
    article = Article.Article(country)
    text = article.extract_words_from_url(URL)
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
    dictionary[country][3] = dictionary[country][3] + len(processedTxt)  # Accumulate length of each article
    print("The length of text (excluding stop words) in the article: " + str(len(processedTxt)))
    print("Total positive words in this article: " + str(
        positveNo) + "\n" + "Total negative words in this article: " + str(
        negativeNo) + "\n" + "Total neutral words in this article: " + str(neutralNo))
    if positveNo > negativeNo:
        print(
            "Since the positive words is more than the negative words, this article gives " + country + " a positive sentiment\n")
    elif positveNo < negativeNo:
        print(
            "Since the negative words is more than the positive words, this article gives " + country + " a negative sentiment\n")
    else:
        print(
            "Since the positive words and the negative words are equal, this article gives " + country + " a neutral sentiment\n")


# To find out the most appropriate country to have store expansion based on the positive sentiments among countries
def expandBranch(ranking):
    mostValuableCountry = ""
    leastDifference = 0
    for country, sentiments in ranking.items():
        print("For " + country + ", the overall positive words are " + str(
            sentiments[0]) + ", the overall negative words are " + str(
            sentiments[1]) + " and the overall neutral words are " + str(sentiments[2]))
        if sentiments[0] - sentiments[1] > leastDifference:
            mostValuableCountry = country
            leastDifference = sentiments[0] - sentiments[1]
    print(
        "As a result, " + mostValuableCountry + " is the worth having branch expansion as it has the least difference, " + str(
            leastDifference) + " between overall positive and negative words\n")


# To store the 5 countries in one array and the category in another array from a dictionary
def storeRanking(countryArray, categoryArray, ranking):
    i = 0
    for country, sentiments in ranking.items():
        countryArray[i] = country
        categoryArray[i] = sentiments[0] - sentiments[1]
        i = i + 1


# Sort the country based on different type of category
def partition(l, r, countryArray, categoryArray):
    # Assume first element as the pivot
    pivot = l
    pivotIndex = l
    for i in range(l + 1, r):
        if categoryArray[i] >= categoryArray[pivot]:
            # Swapping values larger than the pivot to the front (The greater value has higher priority)
            swap(categoryArray, pivotIndex + 1, i)
            swap(countryArray, pivotIndex + 1, i)
            pivotIndex += 1
    # Swap the pivot element to the pivot index ( the correct position of the pivot )
    swap(categoryArray, pivot, pivotIndex)
    swap(countryArray, pivot, pivotIndex)
    return pivotIndex


def swap(array, l, r):
    temp = array[l]
    array[l] = array[r]
    array[r] = temp


def quicksort(l, r, countryArray, categoryArray):
    if len(categoryArray) == 1:  # Terminating Condition for recursion.
        return categoryArray
    if l < r:
        pivotIndex = partition(l, r, countryArray, categoryArray)
        quicksort(l, pivotIndex, countryArray, categoryArray)  # Recursively sorting the left values
        quicksort(pivotIndex + 1, r, countryArray, categoryArray)  # Recursively sorting the right values
    return categoryArray


# Build an array of positive words using WordList class
positiveWordsList = listofWords("POSITIVE", "words\\Positive.txt")
# Build an array of negative words using WordList class
negativeWordsList = listofWords("NEGATIVE", "words\\Negative.txt")
# Build an array of negative words using WordList class
neutralWordsList = listofWords("NEUTRAL", "words\\Neutral.txt")
# Build a dictionary to store the overall number of positive and negative words of each country for ranking
# The index 0 store the amount of positive words & the index 1 store the amount of negative words
# the index 2 store the amount of neutral words & the index 3 store the length of articles
rank = {"Malaysia": [0, 0, 0, 0],
        "United States": [0, 0, 0, 0],
        "Singapore": [0, 0, 0, 0],
        "Taiwan": [0, 0, 0, 0],
        "Japan": [0, 0, 0, 0]
        }

# Store the 25 articles in an array before processing
articles = [
    ["Malaysia",
     "https://www.dosm.gov.my/v1/index.php?r=column/cthemeByCat&cat=124&bul_id=UEpPd3dKQkM2ZVRnVFZ3T0w1d1Zrdz09&menu_id=Tm8zcnRjdVRNWWlpWjRlbmtlaDk1UT09"],
    ["Malaysia", "https://internationalliving.com/countries/malaysia/is-malaysia-safe/"],
    ["Malaysia", "https://www.theedgemarkets.com/article/oecd-forecasts-malaysia-economy-grow-6-2022"],
    ["Malaysia",
     "https://www.malaymail.com/news/malaysia/2022/06/03/finance-ministry-tax-revenue-reforms-key-to-socio-economic-resilience/10520"],
    # ["Malaysia",
    #  "https://www.malaymail.com/news/malaysia/2022/01/04/socio-economic-research-centre-a-better-year-in-2022-for-malaysian-economy/2032924"],
    ["Malaysia", "https://www.worldbank.org/en/news/press-release/2019/07/01/malaysias-economy-to-see-continued-growth-but-downside-risks-are-elevated"],

    ["Singapore",
     "https://www.lowyinstitute.org/publications/getting-singapore-shape-economic-challenges-and-how-meet-them-0"],
    ["Singapore",
     "https://www.csc.gov.sg/articles/economic-development-and-social-integration-singapore-s-evolving-social-compact#notes"],
    ["Singapore",
     "https://www.cnbc.com/2020/07/16/singapore-economy-still-dire-amid-global-resurgence-in-coronavirus-mas-says.html"],
    ["Singapore", "https://www.cnbc.com/2021/08/11/singapore-updates-q2-gdp-full-year-2021-economic-forecasts.html"],
    ["Singapore", "https://www.csc.gov.sg/articles/singapore%27s-social-support-system-two-anomalies"],

    ["United States",
     "https://www.pewresearch.org/social-trends/2019/12/11/most-americans-say-the-current-economy-is-helping-the-rich-hurting-the-poor-and-middle-class/"],
    ["United States",
     "https://www.cnbc.com/2021/07/23/the-rapid-growth-the-us-economy-has-seen-is-about-to-hit-a-wall.html"],
    ["United States", "https://www.focus-economics.com/countries/united-states"],
    ["United States", "https://time.com/6130525/economy-doing-well-why-does-it-feel-like-a-disaster/"],
    ["United States", "https://www.bbc.com/news/business-61254160"],
    # ["United States", "https://www.mercatus.org/publications/regulation/economic-situation-march-2022"],

    ["Taiwan", "https://www.taiwannews.com.tw/en/news/4530057"],
    ["Taiwan", "https://focustaiwan.tw/business/202201240020"],
    ["Taiwan", "https://asiatimes.com/2020/08/taiwanese-economy-stands-out-globally/"],
    ["Taiwan", "https://www.reuters.com/world/asia-pacific/taiwan-revises-up-2022-gdp-forecast-2022-02-24/"],
    ["Taiwan", "https://www.focus-economics.com/country-indicator/taiwan/gdp"],

    ["Japan", "https://www.insidejapantours.com/blog/2020/08/12/the-societal-pressures-that-shape-japan/"],
    ["Japan", "https://www2.deloitte.com/us/en/insights/economy/asia-pacific/japan-economic-outlook.htm"],
    ["Japan", "https://www.nippon.com/en/in-depth/d00663/"],
    ["Japan", "https://santandertrade.com/en/portal/analyse-markets/japan/economic-political-outline"],
    ["Japan", "https://www.thebalance.com/japan-s-economy-recession-effect-on-u-s-and-world-3306007"]
]

# Process the 25 articles we found to find the most appropriate country to expan branch
for numOfArticle in range(len(articles)):
    preprocessArticle(articles[numOfArticle][0], articles[numOfArticle][1], positiveWordsList, negativeWordsList,
                      neutralWordsList, rank)

# Find out the most worth country to have the store expansion according to the positive & negative sentiment
expandBranch(rank)
print(
    "This algorithm is accurate to give you an overview on the overall positive and negative sentiment on each country so that you can determine the country to have your branch expansion.")
print(
    "When the length of article increase, the number of positive and negative words also increase. Hence, we use the difference to rank the country to increase accuracy.")
print("In a nutshell, This is the ranking based on the differences in the countries' positive and negative words:")
# Sort the ranking of the countries based on the difference between the positive and negative words
countryList = [None] * 5
categoryList = [None] * 5
storeRanking(countryList, categoryList, rank)
sortedCategoryList = quicksort(0, len(countryList), countryList, categoryList)
# Display the list from the most recommended to the least recommended country based on difference between positive and negative words
print(".............................................................")
for i in range(len(sortedCategoryList)):
    print(str(i + 1) + ". " + str(countryList[i]) + " => " + str(sortedCategoryList[i]))
print(".............................................................")
print(
    "However, we recommend you to read the article by yourself so that you can see some economical graphs for better visualization which is not found here.\n")

# ...................................................... Question 2 .......................................................
print(
    "Besides, it is also necessary for us to check the distributed geographical locations in the country\nto determine" + " the local distributed centre in the country to optimize the delivery cost if we want expand our stores in that country\n")

# Files of every targeted country to expand the business
targetFiles = [r'Moonbucks Expand Targets\MY.xlsx',
               r'Moonbucks Expand Targets\USEdited.xlsx',
               r'Moonbucks Expand Targets\SG.xlsx',
               r'Moonbucks Expand Targets\TW.xlsx',
               r'Moonbucks Expand Targets\JP.xlsx'
               ]

i = 0
finalResult = []
countryOptDist = {}  # Store the country with its shortest distance to be used in Question 3
for i in range(len(targetFiles)):
    data = pd.read_excel(targetFiles[i])
    des = data.Coordinates
    API_key = 'AIzaSyDEX3h2G60Jmz5aqAVGsqaggwKhic5dlZY'
    location, routeList = distributionCentre.findCentre(des, API_key, data)
    finalResult.append(location)  # Store all resulting distribution centre in each country into a list
    optPath, optDis = distributionCentre.find_shortest_path(routeList, des, location.index)
    countryOptDist[location.nation] = round(optDis, 1)
    distributionCentre.mapPlotter(optPath, location.coor, des, location.nation, optDis)
print("\nAll centres coordinates:")
print(f"{'Country' :<25} {'Distribution Centre Coordinates' :<40} Total Shortest Distance")
print("------------------------------------------------------------------------------------------")
for a in finalResult:
    print(f"{a.nation :<25} {a.coor :<40} {a.vecD :>13.2f}km")

# ...................................................... Question 3 .......................................................
pc = probabilityCalculation.probabilityCalculation()
rankingOfProb = pc.probGood_LEandSC(rank)
# Sort country ranking based on probability counted for the sentiments analysis
countryOrder1 = list(rankingOfProb.keys())
valueOrder1 = list(rankingOfProb.values())
pc.insertion_sort(valueOrder1, countryOrder1)
print("\nSorted Ranking of Country (local economic & social situation):")
print(f"{'No' :<10} {'Country' :<15} Probability")
print("------------------------------------------------------------------------------------------")
ranking1 = 1
for i in range(len(countryOrder1) - 1, -1, -1):
    print(f"{ranking1 :<10} {countryOrder1[i] :<15} {valueOrder1[i] :>8.4f}")
    ranking1 = ranking1 + 1
# Take into account of the diesel price in each country to calculate the running cost of logistics
dieselPrice = {'Japan': 4.74, 'Taiwan': 4.08, 'United States': 6.62, 'Singapore': 9.27, 'Malaysia': 2.15}
deliveryRate = pc.lowest_optimal_delivery(countryOptDist, dieselPrice)
countryOrder2 = list(deliveryRate.keys())
valueOrder2 = list(deliveryRate.values())
pc.insertion_sort(valueOrder2, countryOrder2)
ranking2 = 1
print("\nSorted Ranking of Country (running cost of logistic):")
print(f"{'No' :<10} {'Country' :<15} Delivery Fee (Distance travelled*Diesel Price)")
print("------------------------------------------------------------------------------------------")
for i in range(len(countryOrder2) - 1, -1, -1):
    print(f"{ranking2 :<10} {countryOrder2[i] :<15} {'RM ': >5} {valueOrder2[i] :.2f}")
    ranking2 = ranking2 + 1
# Sort the country ranking based on probability of the lowest optimal delivery
total_delivery = sum(valueOrder2)
ranking_lowest_optimal_delivery = pc.prob_lowest_optimal_delivery(countryOptDist, deliveryRate, total_delivery)
countryOrder4 = list(ranking_lowest_optimal_delivery.keys())
valueOrder4 = list(ranking_lowest_optimal_delivery.values())
pc.insertion_sort(valueOrder4, countryOrder4)
ranking4 = 1
print("\nSorted Ranking of Country (lowest optimal delivery):")
print(f"{'No' :<10} {'Country' :<15} Probability")
print("------------------------------------------------------------------------------------------")
for i in range(len(countryOrder4) - 1, -1, -1):
    print(f"{ranking4 :<10} {countryOrder4[i] :<15} {valueOrder4[i] :>8.4f}")
    ranking4 = ranking4 + 1
# Sort the country from the least recommended to the most recommended country to have expansion (sentiment analysis, running cost of logistics)
recommended_country = pc.prob_country_recommended(rankingOfProb, ranking_lowest_optimal_delivery)
countryOrder3 = list(recommended_country.keys())
valueOrder3 = list(recommended_country.values())
pc.insertion_sort(valueOrder3, countryOrder3)
ranking3 = 1
print("\nSorted Final Ranking of Countries from the most recommended to the least recommended to have an expansion:")
print(f"{'No' :<10} {'Country' :<15} Probability")
print("------------------------------------------------------------------------------------------")
for i in range(len(countryOrder3) - 1, -1, -1):
    print(f"{ranking3 :<10} {countryOrder3[i] :<15} {valueOrder3[i] :>8.4f}")
    ranking3 = ranking3 + 1
# Provide a final ranking line chart for better visualization
xAxis = list(rank.keys())
yAxisSentiment = [0] * len(xAxis)
yAxisLowestOptimal = [0] * len(xAxis)
yAxisFinalProb = [0] * len(xAxis)
for i in range(len(xAxis)):
    yAxisSentiment[i] = rankingOfProb[xAxis[i]]
for i in range(len(xAxis)):
    yAxisLowestOptimal[i] = ranking_lowest_optimal_delivery[xAxis[i]]
for i in range(len(xAxis)):
    yAxisFinalProb[i] = recommended_country[xAxis[i]]
fig = go.Figure()
# Final probability based on sentiment analysis
fig.add_trace(go.Scatter(x=xAxis, y=yAxisSentiment, name='Sentiment', mode='lines+markers',
                         line=dict(color='royalblue')))
# Final probability based on lowest optimal delivery cost
fig.add_trace(go.Scatter(x=xAxis, y=yAxisLowestOptimal, name='Delivery', mode='lines+markers',
                         line=dict(color='#AB63FA')))
# Final probability based on sentiment analysis & lowest optimal delivery cost
fig.add_trace(go.Scatter(x=xAxis, y=yAxisFinalProb, name='Final', mode='lines+markers',
                         line=dict(color='firebrick')))
# Edit the layout
fig.update_layout(title='Final Ranking of the 5 Countries',
                  title_x=0.5,
                  xaxis_title='Country',
                  yaxis_title='Probability')
fig.show()
print("In conclusion, " + countryOrder3[
    len(countryOrder3) - 1] + " is the best recommended for Moonbucks to have its branch expansion")

# ........................................................... Question 1 Plotly Dash Graphs ..........................................
print("\n\n")
plotlyDash.build_dataFrame(rank)
plotlyDash.build()

# ........................................................... End of project codes .................................................
print("\n\n")

# print("\nSorted Ranking of Country (local economic & social situation):")
# print(f"{'No' :<25} {'Country' :<40} Probability")
# print(*countryName)
