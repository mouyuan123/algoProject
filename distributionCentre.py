import googlemaps
import requests
import gmplot

gmaps = googlemaps.Client(key='AIzaSyAQrB5JB26LImIMUIWYkYNyDaWVbvudRoc')


# An object class used to store the information of the distribution centre
class distributionCentres:
    def __init__(self, nation, addr, coor, vecD, index):
        self.nation = nation
        self.addr = addr
        self.coor = coor
        self.vecD = vecD
        self.index = index

    def result(self):
        print("Suitable Distribution center in ", self.nation, ": \n", self.addr, "\nCoordinate : \n [", self.coor, "]",
              "\nVector distance : \n [", "%.1f" % self.vecD, "km ]")


def findCentre(des, API_key, data):
    sum = 0
    min = 99999
    i = 0
    DisNodetoENodes = [[]]

    while i < des.size:
        listofDis = []
        for destination in des:
            url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + str(
                des[i].split(", ")[0]) + "%2C" + str(des[i].split(", ")[1]) + \
                  "&destinations=" + str(destination.split(", ")[0]) + "%2C" + str(
                destination.split(", ")[1]) + "&key=" + API_key

            url2 = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + str(
                destination.split(", ")[0]) + "%2C" + str(destination.split(", ")[1]) + \
                   "&destinations=" + str(des[i].split(", ")[0]) + "%2C" + str(
                des[i].split(", ")[1]) + "&key=" + API_key

            payload = {}
            headers = {}

            response = requests.request("GET", url, headers=headers, data=payload)
            distance = response.json().get("rows")[0].get("elements")[0].get("distance").get(
                "text")  # Retrieve only the required distance data

            response2 = requests.request("GET", url2, headers=headers, data=payload)
            bckDistance = response2.json().get("rows")[0].get("elements")[0].get("distance").get("text")

            value = distance.split(" ")
            value2 = bckDistance.split(" ")
            floatValue = float(value[0].replace(',', ''))
            floatValue2 = float(value2[0].replace(',', ''))
            sum += floatValue + floatValue2  # Sum up to find the vector distance for each location

            if des[i] != destination:
                listofDis.append(floatValue)
            else:
                listofDis.append(0)

        if sum < min:
            min = sum
            min_coor = des[i]
            min_index = i
            centreAddr = response.json().get("origin_addresses")

        DisNodetoENodes.insert(i, listofDis)
        i += 1
        sum = 0
    selectedCentre = distributionCentres(data.Nationality[0], centreAddr, min_coor, min, min_index)
    DisNodetoENodes = DisNodetoENodes[:-1]
    return selectedCentre, DisNodetoENodes


def find_shortest_path(DisNodetoENodes, Nodes, centIdx):
    from sys import maxsize
    from itertools import permutations
    l = Nodes.size

    def shortestRoute(DisNodetoENodes, centIdx):
        vertex = []
        for i in range(l):
            if i != centIdx:
                vertex.append(i)

        minTravelPath = maxsize
        next_permutation = permutations(vertex)
        for i in next_permutation:
            current_pathweight = 0
            a = centIdx
            for b in i:
                current_pathweight += DisNodetoENodes[a][b]
                a = b
            current_pathweight += DisNodetoENodes[a][centIdx]
            if current_pathweight < minTravelPath:
                best = i
                shortestDis = current_pathweight
            minTravelPath = min(minTravelPath, current_pathweight)
        return best, shortestDis

    route, resultMinDis = shortestRoute(DisNodetoENodes, centIdx)
    return route, resultMinDis


def mapPlotter(pathlist, centrelist, des, nation, optdis):
    waypoints = []
    stopCount = 1
    gmap1 = gmplot.GoogleMapPlotter(centrelist.split(", ")[0], centrelist.split(", ")[1], 13,
                                    apikey='AIzaSyAQrB5JB26LImIMUIWYkYNyDaWVbvudRoc')

    for i in pathlist:
        waypoints.append(des[i])

    gmap1.marker(lat=float(centrelist.split(", ")[0]),
                 lng=float(centrelist.split(", ")[1]),
                 label='C')
    gmap1.directions(origin=(float(centrelist.split(", ")[0]), float(centrelist.split(", ")[1])),
                     destination=(float(waypoints[0].split(", ")[0]), float(waypoints[0].split(", ")[1])))
    gmap1.marker(lat=float(waypoints[0].split(", ")[0]),
                 lng=float(waypoints[0].split(", ")[1]),
                 label='1')
    originAdd = gmaps.reverse_geocode((float(centrelist.split(", ")[0]), float(centrelist.split(", ")[1])))[0]["formatted_address"]
    desAdd = gmaps.reverse_geocode((float(waypoints[0].split(", ")[0]), float(waypoints[0].split(", ")[1])))[0]["formatted_address"]
    print(nation)
    print("Start:", originAdd)
    print ("Stop:", stopCount,
           "==> ",
           desAdd)
    stopCount = stopCount+1

    for desIndx in range(1, len(waypoints)):
        gmap1.directions(
            origin=(float(waypoints[desIndx - 1].split(", ")[0]), float(waypoints[desIndx - 1].split(", ")[1])),
            destination=(float(waypoints[desIndx].split(", ")[0]), float(waypoints[desIndx].split(", ")[1])))
        gmap1.marker(lat=float(waypoints[desIndx].split(", ")[0]),
                     lng=float(waypoints[desIndx].split(", ")[1]),
                     label=str(desIndx+1))

        desAdd = gmaps.reverse_geocode((float(waypoints[desIndx].split(", ")[0]), float(waypoints[desIndx].split(", ")[1])))[0][
            "formatted_address"]
        print("Stop:", stopCount,
              "==> ",
              desAdd)
        stopCount = stopCount + 1

    gmap1.directions(origin=(float(waypoints[len(waypoints) - 1].split(", ")[0]), float(waypoints[len(waypoints) - 1].split(", ")[1])),
                     destination=(float(centrelist.split(", ")[0]), float(centrelist.split(", ")[1])))
    desAdd = gmaps.reverse_geocode((float(centrelist.split(", ")[0]), float(centrelist.split(", ")[1])))[0][
        "formatted_address"]
    print("Stop:", stopCount,
          "==> ",
          desAdd)
    print("Optimized distance (km): ", "%.1f" % optdis)
    print()



    gmap1.draw(nation + ".html")

    map_string = gmap1.get().replace('DirectionsRenderer({map: map', 'DirectionsRenderer({map: map, suppressMarkers: '
                                                                     'true')
    with open(nation+".html", "w") as f:
        f.write(map_string)


