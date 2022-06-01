import pandas as pd
import requests
import gmplot

#Files of every targeted country to expand the business
targetFiles = [r'C:\Users\user\Documents\Moonbucks Expand Targets\MY.xlsx',
               r'C:\Users\user\Documents\Moonbucks Expand Targets\US.xlsx',
               r'C:\Users\user\Documents\Moonbucks Expand Targets\SG.xlsx',
               r'C:\Users\user\Documents\Moonbucks Expand Targets\TW.xlsx',
               r'C:\Users\user\Documents\Moonbucks Expand Targets\JP.xlsx'
               ]

#An object class used to store the information of the distribution centre
class distributionCentres:
    def __init__(self, nation, addr, coor, vecD):
        self.nation = nation
        self.addr = addr
        self.coor = coor
        self.vecD = vecD

    def result(self):
        print("Suitable Distribution center in ", self.nation, ": \n", self.addr, "\nCoordinate : \n [",self.coor, "]", "\nVector distance : \n [", "%.1f" % self.vecD, "km ]")

def distanceSum(des, API_key):
    sum = 0
    min = 99999
    i = 0

    while i < des.size:
        for destination in des:
            url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins="+ str(des[i].split(", ")[0])+ "%2C" + str(des[i].split(", ")[1]) + \
                  "&destinations=" + str(destination.split(", ")[0]) + "%2C" + str(destination.split(", ")[1]) + "&key=" + API_key

            url2 = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + str(destination.split(", ")[0]) + "%2C" + str(destination.split(", ")[1]) + \
                  "&destinations=" + str(des[i].split(", ")[0]) + "%2C" + str(des[i].split(", ")[1]) + "&key=" + API_key

            payload = {}
            headers = {}

            response = requests.request("GET", url, headers=headers, data=payload)
            distance = response.json().get("rows")[0].get("elements")[0].get("distance").get("text") #Retrieve only the required distance data

            response2 = requests.request("GET", url2, headers=headers, data=payload)
            bckDistance = response2.json().get("rows")[0].get("elements")[0].get("distance").get("text")

            value = distance.split(" ")
            value2 = bckDistance.split(" ")
            sum += float(value[0].replace(',', '')) + float(value2[0].replace(',', '')) #Sum up to find the vector distance for each location

        if sum < min:
            min = sum
            min_coor = des[i]
            centreAddr = response.json().get("origin_addresses")

        i+=1
        sum = 0
    selectedCentre = distributionCentres(data.Nationality[0], centreAddr, min_coor, min)
    return selectedCentre

i = 0
finalResult = []
for i in range(len(targetFiles)):
    data = pd.read_excel(targetFiles[i])
    des = data.Coordinates
    API_key = 'AIzaSyBAeA4z6IoKc5uU_--TTQ0HWBHCFvDpf5g'
    location = distanceSum(des, API_key)
    gmap1 = gmplot.GoogleMapPlotter(float(location.coor.split(", ")[0]), float(location.coor.split(", ")[1]), zoom=13,
                                    apikey=API_key)
    for destination in des:
        gmap1.directions(origin=(float(location.coor.split(", ")[0]), float(location.coor.split(", ")[1])),
                         destination=(float(location.coor.split(", ")[0]), float(location.coor.split(", ")[1])),
                         waypoints=[(float(destination.split(", ")[0]), float(destination.split(", ")[1]))],
                         color='red')
    gmap1.draw(location.nation + '.html')
    finalResult.append(location) #Store all resulting distribution centre in each country into a list

print("All centres coordinates : \n")
print(f"{'Country' :<20} Coordinates")
print("---------------------------------------------")
for a in finalResult:
    print(f"{a.nation :<20} {a.coor}")
