""" 
This file automatically creates and populates a CouchDB database from the data stored in /data.
In order, the file does the following:
1. Create Database called 'gtfs'.
2. Creates documents from files in /data.
3. Creates design document for the database. (With views) 
To run this file, use the command 'python RunQueries.py', you will need to have ./credentials.txt
"""
# Import libraries
import csv
import requests

# Read in credentials
CREDENTIALSFILEPATH = '../credentials.txt'
with open(CREDENTIALSFILEPATH, 'r', encoding="utf8") as credentialFileObject:
    username = credentialFileObject.readline().strip()
    password = credentialFileObject.readline().strip()
    ip = credentialFileObject.readline().strip()
    port = credentialFileObject.readline().strip()
    credentialFileObject.close()
    url = "http://" + username + ":" + password + "@" + ip + ":" + port + "/gtfs"

# Create database instance
print("Attempting to create database: ")
x = requests.put(url, timeout=60)
print("     ", x.text)

def writetodbfromtxt(filepath, doc_type):
    """
    Creates documents from each line of the supplied
    .txt file. Supply a doc_type to differentiate between
    files for the CouchDB database. 
    """
    with open(filepath, "r", encoding="utf8") as csvfile:
        csvreader = csv.reader(csvfile)

        #Extract fields
        fields = next(csvreader)

        #Insert doc_type field so database can tell difference between files
        fields.insert(0, "doc_type")

        bulkdocs = []
        counter = 0
        for row in csvreader:
            data = row

            #Insert doc_type
            data.insert(0, doc_type)

            #Change all rows that have: "" to "null"
            for i, value in enumerate(data):
                if value == "":
                    data[i] = "null"

            #Create json from fields and data
            json_data = dict(zip(fields, data))
            bulkdocs.append(json_data)

            #Send batches of 100000
            if len(bulkdocs) >= 100000:
                json_bulk = {"docs": bulkdocs}
                requests.post(url + "/_bulk_docs", json=json_bulk, timeout=600)
                bulkdocs = []
            counter += 1

        #Final batch (remaining data)
        json_bulk = {"docs": bulkdocs}
        requests.post(url + "/_bulk_docs", json=json_bulk, timeout=600)
        print("For: ", doc_type, "sent a total of", counter, "rows")

#Add documents to table
writetodbfromtxt("../data/gtfs/agency.txt", "Agency")
writetodbfromtxt("../data/gtfs/calendar_dates.txt", "Calendar_date")
writetodbfromtxt("../data/gtfs/calendar.txt", "Calendar")
writetodbfromtxt("../data/gtfs/fare_attributes.txt", "Fare_attribute")
writetodbfromtxt("../data/gtfs/fare_rules.txt", "Fare_rule")
writetodbfromtxt("../data/gtfs/route_directions.txt", "Route_direction")
writetodbfromtxt("../data/gtfs/routes.txt", "Route")
writetodbfromtxt("../data/gtfs/shapes.txt", "Shape")
writetodbfromtxt("../data/gtfs/stop_features.txt", "Stop_Feature")
writetodbfromtxt("../data/gtfs/stop_times.txt", "Stop_time")
writetodbfromtxt("../data/gtfs/stops.txt", "Stop")
writetodbfromtxt("../data/gtfs/transfers.txt", "Transfer")
writetodbfromtxt("../data/gtfs/trips.txt", "Trip")

#Create design document and views
print("Creating design document...")
jsondata = {
        "id": "_design/queries", 
        "language": "javascript",
        "views": 
        {
            "getPCCDirections": 
            {
                "map": """function(doc) {if(doc.doc_type == 'Route_direction') 
                {if(doc.direction_name == 'To Portland City Center') {emit(doc._id, doc);}}}"""
            },
            "getRouteByID":
            {
                "map": "function(doc) {if(doc.doc_type == 'Route'){emit(doc.route_id, doc);}}"
            },
            "getMLR_routes":
            {
                "map": """function(doc){if(doc.doc_type == 'Route') 
                       {if(doc.route_long_name == 'MAX Red Line') {emit(doc);}}}"""
            },
            "getTripsByRouteID":
            {
                "map": "function(doc) {if(doc.doc_type == 'Trip'){emit(doc.route_id, doc);}}"
            },
            "getTripsByTripID":
            {
                "map": "function(doc) {if(doc.doc_type == 'Trip'){emit(doc.trip_id, doc);}}"
            },
            "getCalendarDatesBySID":
            {
                "map": """function(doc) {if(doc.doc_type == 'Calendar_date')
                {emit(doc.service_id, doc);}}"""
            },
            "getStopTimesByTripID":
            {
                "map": "function(doc) {if(doc.doc_type == 'Stop_time'){emit(doc.trip_id, doc);}}"
            },
            "get_PSUUC_stops": 
            {
                "map": """function(doc) {if(doc.doc_type == 'Stop') 
                {if(doc.stop_name == 'PSU Urban Center') {emit(doc._id, doc);}}}"""
            },
            "getStopTimesByStopID":
            {
                "map": "function(doc) {if(doc.doc_type == 'Stop_time'){emit(doc.stop_id, doc);}}"
            },
            "getRouteDirectionsByRouteID":
            {
                "map": """function(doc) {if(doc.doc_type == 'Route_direction')
                {emit(doc.route_id, doc);}}"""
            }
        }
    }
x = requests.put(url + "/_design/queriesdesigndocument", json=jsondata, timeout=60)
print("     ", x.text)
