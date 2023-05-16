"""
This file combines calling views and client operations to answer the three questions specified by the project instructions
The three questions are:
1. List routes that go to 'Portland City Center'
2. On which days does the MAX Red Line run within the given time range?"
3. Which modes of public transport (routes) are available near ‘PSU Urban Center’ at the latest possible time before 9.00 AM (ignore date)?
   Display stops around PSU Urban Center, type of stop location, type of transportation (route), it’s time of arrival and direction (direction name)
To run this file, use the command 'python RunQueries.py', you will need to have ./credentials.txt
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
url = "http://" + username + ":" + password + "@" + ip + ":" + port + "/gtfs"

#Creates string from list data that fits the HTTP format
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
directionstoPCC = requests.get(url + "/_design/queriesdesigndocument/_view/getPCCDirections")
routeIDS = []
directionsRows = directionstoPCC.json()["rows"]
for row in directionsRows:
    routeIDS.append(row["value"]["route_id"])

#From the routeIDS extracted, get all routes with matching ids
keystr = stringfromlist(routeIDS)

routesToPCC = requests.get(url + "/_design/queriesdesigndocument/_view/getRouteByID?keys="+keystr)
for row in routesToPCC.json()["rows"]:
    print("     ", row["value"]["route_id"], row["value"]["agency_id"], row["value"]["route_long_name"])

#####################################################################################
#Query 2: On which days does the MAX Red Line run within the given time range?
print("Query 2: On which days does the MAX Red Line run within the given time range?")
starttime = time(4,0,0)
endtime = time(9,0,0)

#Get routes that have "MAX Red line" as a long name
routes_MRL = requests.get(url + "/_design/queriesdesigndocument/_view/getMLR_routes").json()["rows"]
MRL_route_ids = []
for x in routes_MRL: MRL_route_ids.append(x["key"]["route_id"])
print("     ", "Routes associated with MAX Red Line ", MRL_route_ids)

#Get trips associated with the routes
keystr = stringfromlist(MRL_route_ids)
trips_MLR = requests.get(url + "/_design/queriesdesigndocument/_view/getTripsByRouteID?keys="+keystr).json()["rows"]
MRL_tripids = []
for x in trips_MLR: MRL_tripids.append(x["value"]["trip_id"])
print("     ", "There are", len(MRL_tripids), "trips associated with the routes")

#Out of the trips we have so far, keep only the trips that fall between the start and end time
validStopTimeTripIDS = []
for tripid in MRL_tripids:
    tripStopTimes = requests.get(url + "/_design/queriesdesigndocument/_view/getStopTimesByTripID?keys=[\"" + tripid + "\"]").json()["rows"]
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
services_MLR = requests.get(url + "/_design/queriesdesigndocument/_view/getTripsByTripID?keys="+keystr).json()["rows"]
MRL_service_ids = []
for x in services_MLR: MRL_service_ids.append(x["value"]["service_id"])
MRL_service_ids = list(set(MRL_service_ids))
print("     ", "Service ids associated with the trips", MRL_service_ids)

#Get the calendar_dates associated with services
keystr = stringfromlist(MRL_service_ids)
dates_MLR = requests.get(url + "/_design/queriesdesigndocument/_view/getCalendarDatesBySID?keys="+keystr).json()["rows"]
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
print("""Query 3: Which modes of public transport (routes) are available near ‘PSU Urban Center’ at the latest possible time before 9.00 AM (ignore date)?
         Display stops around PSU Urban Center, type of stop location, type of transportation (route), it’s time of arrival and direction (direction name)
     """)
starttime = time(8,30,0)
endtime = time(9,0,0)
#List of dictionaries of our final data, should be able to add, remove, and modify entries based on views
info = []

#Get all stops from stops.txt that have stop_name 'PSU Urban Center'; keep stop_id, stop_name, and location_type
stops = requests.get(url + "/_design/queriesdesigndocument/_view/get_PSUUC_stops").json()["rows"]
stopInfo = []
stopids = []
for x in stops:
    stop_id = x["value"]["stop_id"]
    stop_name = x["value"]["stop_name"]
    stop_location_type = x["value"]["location_type"]
    stopInfo.append([stop_id, stop_name, stop_location_type])
    stopids.append(stop_id)

#Get all stop_times (with the stop_id and all arrival_time between 8:30 and 9:00) (keep stop_id and arrival_time and trip_id)
keystr = stringfromlist(stopids)
stop_times = requests.get(url + "/_design/queriesdesigndocument/_view/getStopTimesByStopID?keys="+keystr).json()["rows"]
for x in stop_times:
    stop_id = x["value"]["stop_id"]
    stop_arrival = x["value"]["arrival_time"]
    trip_id = x["value"]["trip_id"]
    arrivalTime = x["value"]["arrival_time"]
    arrivalHour = int(arrivalTime[0:2])
    if(arrivalHour >= 24): arrivalHour -= 24
    arrivalMinute = int(arrivalTime[3:5])
    arrivalSecond = int(arrivalTime[6:8])
    arrivalTime = time(arrivalHour, arrivalMinute, arrivalSecond)
    if(arrivalTime > starttime and arrivalTime < endtime):
        #print(stop_id, stop_arrival, trip_id)
        for s in stopInfo:
            if(s[0] == stop_id):
                stop_name = s[1]
                stop_location_type = s[2]
                info.append({"stop_id": stop_id, "arrival_time": stop_arrival, "trip_id": trip_id, "stop_name": stop_name, "stop_location_type": stop_location_type})

#From the resulting trip_ids, get all routes ids, then route_types, then directions
for x in info:
    tid = x["trip_id"]
    trip = requests.get(url + "/_design/queriesdesigndocument/_view/getTripsByTripID?keys=[\"" + tid + "\"]").json()["rows"]
    rid = trip[0]["value"]["route_id"]
    route = requests.get(url + "/_design/queriesdesigndocument/_view/getRouteByID?keys=[\"" + rid + "\"]").json()["rows"]
    route_type = route[0]["value"]["route_type"]
    route_directions = requests.get(url + "/_design/queriesdesigndocument/_view/getRouteDirectionsByRouteID?keys=[\"" + rid + "\"]").json()["rows"]
    route_direction_name = route_directions[0]["value"]["direction_name"]
    x["route_id"] = rid
    x["route_type"] = route_type
    x["route_direction_name"] = route_direction_name

#Print only the necessary fields to answer to the question
for i in info:
    print("     Stopid:", i["stop_id"], "   Stop_name:", i["stop_name"], "   Stop_location_type:", i["stop_location_type"], "   route_type:", i["route_type"], "   arrival_time:", i["arrival_time"], "   direction_name:", i["route_direction_name"])