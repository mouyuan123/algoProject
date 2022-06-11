class probabilityCalculation():

    def probGood_LEandSC(self, dictionaryRank):
        ratio = []
        for country, sentiments in dictionaryRank.items():
            ratio.append(sentiments[0] / sentiments[1])

        total_ratio = sum(ratio)

        rankingProb = {}
        for country, sentiments in dictionaryRank.items():
            rankingProb[country] = ((sentiments[0] / sentiments[1]) / total_ratio)
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

    def lowest_optimal_delivery(self, countryJourney, countryDieselPrice):
        optimal_delivery = {}
        for country, distance in countryJourney.items():
            optimal_delivery[country] = (distance * countryDieselPrice[country])
        return optimal_delivery

    # function to calculate probability of local economic & social situation with the lowest optimal delivery
    def prob_country_recommended(self, rankingOfProb, total_delivery, deliveryRate):
        recommended_country = {}

        for country, value in rankingOfProb.items():
            recommended_country[country] = (
                        (rankingOfProb[country] * 0.4) + ((1 - (deliveryRate[country] / total_delivery)) * 0.6))
        return recommended_country
