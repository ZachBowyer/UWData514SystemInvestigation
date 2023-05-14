"""
Runs query1
Runs query2
Runs query3
"""
import requests

#Read in credentials
credentialsFilePath = '../credentials.txt'
credentialFileObject = open(credentialsFilePath, 'r')
username = credentialFileObject.readline().strip()
password = credentialFileObject.readline().strip()
ip = credentialFileObject.readline().strip()
port = credentialFileObject.readline().strip()
credentialFileObject.close()

#List routes that go ‘To Portland City Center’
# Route_direcitons.txt, routes.txt 
#
# direction_id is the direction of travel for a trip. 0 is trevel in one direction, 1 is travel in opposite direction
#

#On which days does the MAX Red Line run within the given time range? 

#Which modes of public transport (routes) are available near ‘PSU Urban Center’ at the latest possible time before 9.00 AM (ignore date)? 
# Display stops around PSU Urban Center, type of stop location, type of transportation (route), it’s time of arrival and direction (direction name)

####################################################################################
#Query 1: List routes that go ‘To Portland City Center’

#Get directions to Portland city center
directionstoPCC = requests.get("http://" + username + ":" + password + "@" + ip + ":" + port + "/gtfs/_design/queriesdesigndocument/_view/getPCCDirections")
print(directionstoPCC.text)
#print(directionstoPCC.json())
#directionsRows = directionstoPCC.json()["rows"]
#for row in directionsRows:
#    print(row[])

#Extract routes
test = requests.get("http://" + username + ":" + password + "@" + ip + ":" + port + "/gtfs/_design/queriesdesigndocument/_view/getRouteByID?key=\"2\"")
print(test.text)

test = requests.get("http://" + username + ":" + password + "@" + ip + ":" + port + "/gtfs/_design/queriesdesigndocument/_view/getRouteByID?keys=[\"1\", \"2\"]")
print(test.text)

#Combine the entries
