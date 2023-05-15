"""
Runs query1
Runs query2
Runs query3
"""
import requests
import json
from datetime import date
from datetime import time

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
starttime = time(4,0,0)
endtime = time(9,0,0)

#Get routes that have "MAX Red line" as a long name
routes_MRL = requests.get("http://" + username + ":" + password + "@" + ip + ":" + port + "/gtfs/_design/queriesdesigndocument/_view/getMLR_routes").json()["rows"]
MRL_route_ids = []
for x in routes_MRL: MRL_route_ids.append(x["key"]["route_id"])
print("     ", "Routes associated with MAX Red Line ", MRL_route_ids)

#Get trips associated with the routes
keystr = stringfromlist(MRL_route_ids)
trips_MLR = requests.get("http://" + username + ":" + password + "@" + ip + ":" + port + "/gtfs/_design/queriesdesigndocument/_view/getTripsByRouteID?keys="+keystr).json()["rows"]
MRL_tripids = []
for x in trips_MLR: 
    MRL_tripids.append(x["value"]["trip_id"])
print("     ", "There are", len(MRL_tripids), "trips associated with the routes")

#Out of the trips we have so far, keep only the trips that fall between the start and end time
validStopTimeTripIDS = []
for tripid in MRL_tripids:
    tripStopTimes = requests.get("http://" + username + ":" + password + "@" + ip + ":" + port + "/gtfs/_design/queriesdesigndocument/_view/getStopTimesByTripID?keys=[\"" + tripid + "\"]").json()["rows"]
    #print(tripid, tripStopTimes)
    for x in tripStopTimes:
        arrivalTime = x["value"]["arrival_time"]
        tid = x["value"]["trip_id"]
        arrivalHour = int(arrivalTime[0:2])
        if(arrivalHour >= 24): arrivalHour -= 24
        arrivalMinute = int(arrivalTime[3:5])
        arrivalSecond = int(arrivalTime[6:8])
        arrivalTime = time(arrivalHour, arrivalMinute, arrivalSecond)
        if(arrivalTime > starttime and arrivalTime < endtime):
            validStopTimeTripIDS.append(tid)
validStopTimeTripIDS = list(set(validStopTimeTripIDS))
print("     ", "There are", len(validStopTimeTripIDS), "trip ids that have at least 1 stop which falls in the time range")

#Get all the serviced associated with the remaining trips
keystr = stringfromlist(validStopTimeTripIDS)
services_MLR = requests.get("http://" + username + ":" + password + "@" + ip + ":" + port + "/gtfs/_design/queriesdesigndocument/_view/getTripsByTripID?keys="+keystr).json()["rows"]
MRL_service_ids = []
for x in services_MLR: MRL_service_ids.append(x["value"]["service_id"])
MRL_service_ids = list(set(MRL_service_ids))
print("     ", "Service ids associated with the trips", MRL_service_ids)

#Get the calendar_dates associated with services
keystr = stringfromlist(MRL_service_ids)
dates_MLR = requests.get("http://" + username + ":" + password + "@" + ip + ":" + port + "/gtfs/_design/queriesdesigndocument/_view/getCalendarDatesBySID?keys="+keystr).json()["rows"]
MRL_dates = []
for x in dates_MLR: MRL_dates.append(x["value"]["date"])
MRL_dates = list(set(MRL_dates))
print("     ", "There are", len(MRL_dates), "dates associated with the services")

#Get the day of each calendar_date
daysofweek = []
for d in MRL_dates:
    year = int(d[0:4])
    month = int(d[4:6])
    day = int(d[6:8])
    dateobject = date(int(year), int(month), int(day))
    daysofweek.append(dateobject.strftime('%A'))
daysofweek = list(set(daysofweek))
print("     ", "The days of the week that MAX Red Line runs between", starttime, endtime, "is", daysofweek)

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