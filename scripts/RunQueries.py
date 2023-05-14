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
keystr = "["
for i in range(len(routeIDS)):
    keystr += "\"" + str(routeIDS[i]) + "\""
    if(i < len(routeIDS)-1): keystr += (",")
keystr += ("]")

routesToPCC = requests.get("http://" + username + ":" + password + "@" + ip + ":" + port + "/gtfs/_design/queriesdesigndocument/_view/getRouteByID?keys="+keystr)
for row in routesToPCC.json()["rows"]:
    print("     ", row["value"]["route_id"], row["value"]["agency_id"], row["value"]["route_long_name"])

####################################################################################
#Query 2: On which days does the MAX Red Line run within the given time range? 

####################################################################################
#Query 3: 
# Which modes of public transport (routes) are available near ‘PSU Urban Center’ at the latest possible time before 9.00 AM (ignore date)? 
# Display stops around PSU Urban Center, type of stop location, type of transportation (route), it’s time of arrival and direction (direction name)