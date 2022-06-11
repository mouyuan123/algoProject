positiveWords = [941, 2029, 1887, 706, 1611]
negativeWords = [843, 1986, 1846, 716, 1725]
countryName = ["MY", "US", "SG", "TW", "JP"]
totalJourney = [1473.60, 2812.80, 96.20, 761.60, 2693.50]
dieselPrice = [4.74, 4.08, 6.62, 9.27, 2.15]


def probGood_LEandSC(positiveWords, negativeWords, countryName):

    ratio = []
    for i in range(0, len(positiveWords)):
        ratio.append(positiveWords[i] / negativeWords[i])

    total_ratio = sum(ratio)

    rankingProb = []

    for i in range(0, len(positiveWords)):

        rankingProb.append((positiveWords[i]/negativeWords[i])/total_ratio)
        print("\nProbability of ", countryName[i], " have good local economic and social situation: ", end=" ")
        print(format(rankingProb[i], ".4f"))
    return rankingProb

rankingOfProb = probGood_LEandSC(positiveWords, negativeWords, countryName)


# Function to do insertion sort
def insertion_sort(arr, key_arr=None):
    # Traverse through 1 to len(arr)
    for i in range(1, len(arr)):

        key = arr[i]
        if key_arr:
            curr_key = key_arr[i]

        # Move elements of arr[0..i-1], that are
        # greater than key, to one position ahead
        # of their current position
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            if key_arr:
                key_arr[j + 1] = key_arr[j]
            j -= 1
        arr[j + 1] = key
        if key_arr:
            key_arr[j+1] = curr_key


# Sort Total Journey
insertion_sort(totalJourney)
print("\nSorted Total Journey: ", end= "")
for distance in totalJourney:
    print(distance, "km ", end=" ")
print()


# Sort country ranking based on probability counted
insertion_sort(rankingOfProb, countryName)
print("\nSorted Ranking of Country (local economic & social situation): ", end=" ")
print(*countryName)

# display sorted country name with its probability
# for i in range(0, len(countryName)):
#     print("\nProbability of ", countryName[i], " have good local economic and social situation: ", end=" ")
#     print(format(rankingOfProb[i], ".4f"))

# function to calculate optimal delivery

journey=[2693.50, 761.60, 2812.80, 96.20, 1473.60]
# function to calculate the lowest optimal delivery based on diesel price
def lowest_optimal_delivery(journey, dieselPrice, countryName):

    optimal_delivery = []

    for i in range(0, len(journey)):

        optimal_delivery.append(journey[i]*dieselPrice[i])
        print("\nLowest optimal delivery of", countryName[i], " is: RM", end=" ")
        print(format(optimal_delivery[i], ".2f"))
    return optimal_delivery

deliveryRate = lowest_optimal_delivery(journey, dieselPrice, countryName)

insertion_sort(deliveryRate, countryName)
print("\nSorted delivery rate: ", end=" ")
print(*deliveryRate)

total_delivery = []
total_delivery = sum(deliveryRate)
# print(total_delivery)

# function to calculate probability of local economic & social situation with the lowest optimal delivery
def prob_country_recommended(rankingOfProb, total_delivery, deliveryRate):

    recommended_country=[]

    for i in range(0, len(rankingOfProb)):

        recommended_country.append((rankingOfProb[i]*0.4)+((1-(deliveryRate[i]/total_delivery))*0.6))
        print("\nThe probability of", countryName[i]," to be recommended country to have an expansion is:", end=" ")
        print(format(recommended_country[i], ".4f"))
    return recommended_country

most_recommended_country = prob_country_recommended(rankingOfProb, total_delivery, deliveryRate)

# Sort the country from the least recommended to the most recommended country to have expansion
insertion_sort(most_recommended_country, countryName)
print("\nSorted Final Ranking of Countries from the least recommended to the most recommended to have an expansion:", end=" ")
print(*countryName)