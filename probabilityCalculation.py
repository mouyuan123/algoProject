class probabilityCalculation():

    # Function to calculate the probability of a country to have good local economic & social situation
    def probGood_LEandSC(self, dictionaryRank):

        rankingProb = {}
        for country, sentiments in dictionaryRank.items():
            rankingProb[country] = (sentiments[0] / (sentiments[0]+sentiments[1]))
        return rankingProb

    # Function to do insertion sort
    def insertion_sort(self, arr, key_arr=None):
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
                key_arr[j + 1] = curr_key

    # Function to calculate the lowest optimal delivery of each country
    def lowest_optimal_delivery(self, countryJourney, countryDieselPrice):
        optimal_delivery = {}
        for country, distance in countryJourney.items():
            optimal_delivery[country] = (distance * countryDieselPrice[country])
        return optimal_delivery

    # Function to calculate the probability of the lowest optimal delivery of each country
    def prob_lowest_optimal_delivery(self, countryJourney, optimal_delivery, total_delivery):
        ranking_delivery = {}
        for country, distance in countryJourney.items():
            ranking_delivery[country] = 1-(optimal_delivery[country]/total_delivery)
        return ranking_delivery

    # Function to calculate probability of a country to be recommended
    def prob_country_recommended(self, rankingOfProb, ranking_delivery):
        recommended_country = {}

        for country, value in rankingOfProb.items():
            recommended_country[country] = ((rankingOfProb[country] * 0.4) + (ranking_delivery[country] * 0.6))
        return recommended_country
