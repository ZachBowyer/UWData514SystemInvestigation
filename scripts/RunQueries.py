"""
Runs query1
Runs query2
Runs query3
"""
import requests
import json

#Read in credentials
credentialsFilePath = '../credentials.txt'
credentialFileObject = open(credentialsFilePath, 'r')
username = credentialFileObject.readline().strip()
password = credentialFileObject.readline().strip()
ip = credentialFileObject.readline().strip()
port = credentialFileObject.readline().strip()
credentialFileObject.close()

#Creates string from list data
def stringfromlist(data):
    keystr = "["
    for i in range(len(data)):
        keystr += "\"" + str(data[i]) + "\""
        if(i < len(data)-1): keystr += (",")
    keystr += ("]")
    return keystr

####################################################################################
#Query 1: List routes that go ‘To Portland City Center’
print("Query 1: List routes that go to 'Portland City Center'")

#Get directions to Portland city center
directionstoPCC = requests.get("http://" + username + ":" + password + "@" + ip + ":" + port + "/gtfs/_design/queriesdesigndocument/_view/getPCCDirections")
routeIDS = []
directionsRows = directionstoPCC.json()["rows"]
for row in directionsRows:
    routeIDS.append(row["value"]["route_id"])

#From the routeIDS extracted, get all routes with matching ids
keystr = stringfromlist(routeIDS)

routesToPCC = requests.get("http://" + username + ":" + password + "@" + ip + ":" + port + "/gtfs/_design/queriesdesigndocument/_view/getRouteByID?keys="+keystr)
for row in routesToPCC.json()["rows"]:
    print("     ", row["value"]["route_id"], row["value"]["agency_id"], row["value"]["route_long_name"])

####################################################################################
#Query 2: On which days does the MAX Red Line run within the given time range?
#Routes.txt - route_long_name
# join via routeid
# on to trips.txt
# Then get all trips
#  Join trips on service_id to calendar.txt
# Calendar days are all 0??????????
# Maybe join on calendar_dates.txt and get the days it is added..... 
print("Query 2: On which days does the MAX Red Line run within the given time range?")
routes_MRL = requests.get("http://" + username + ":" + password + "@" + ip + ":" + port + "/gtfs/_design/queriesdesigndocument/_view/getMLR_routes").json()["rows"]
MRL_route_ids = []
for x in routes_MRL: MRL_route_ids.append(x["key"]["route_id"])
keystr = stringfromlist(MRL_route_ids)

MRL_trips = requests.get("http://" + username + ":" + password + "@" + ip + ":" + port + "/gtfs/_design/queriesdesigndocument/_view/getTripsByRouteID?keys="+keystr).json()["rows"]
MRL_service_ids = []
for x in MRL_trips: MRL_service_ids.append(x["value"]["service_id"])
MRL_service_ids = set(MRL_service_ids)
print(MRL_service_ids)

####################################################################################
#Query 3: 
# Which modes of public transport (routes) are available near ‘PSU Urban Center’ at the latest possible time before 9.00 AM (ignore date)? 
# Display stops around PSU Urban Center, type of stop location, type of transportation (route), it’s time of arrival and direction (direction name)

#For the first part, 
#Stops.txt join (Filter stop_name = 'PSU Urban Center')
#   Stop_times on stop_id join (Filter departure_time > 0:00:00 and < 09:00:00)
#       Trips on trip_id
#           Join routes on route_id
#               Now get all unique route_types from the final join

#For the second part,
#Stops.txt join (Filter stop_name = 'PSU Urban Center') (Keep stop_name, location_type)
#   Stop_times on stop_id join (Keep arrival_time)
#       Trips on trip_id (Keep direction_id)
#           Join routes on route_id (keep route_types)
#               

print("Query 3: asdasdasdasdasd")