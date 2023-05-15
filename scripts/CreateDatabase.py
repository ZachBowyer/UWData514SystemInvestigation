""" 
Create Database
Fill information in database
Create design document
Create views
"""
import requests
import csv 
import json

#Read in credentials
credentialsFilePath = '../credentials.txt'
credentialFileObject = open(credentialsFilePath, 'r')
username = credentialFileObject.readline().strip()
password = credentialFileObject.readline().strip()
ip = credentialFileObject.readline().strip()
port = credentialFileObject.readline().strip()
credentialFileObject.close()

#Create database instance
print("Attempting to create database: ")
x = requests.put("http://" + username + ":" + password + "@" + ip + ":" + port + "/gtfs")
print("     ", x.text)

#Populate database
def writetodbfromtxt(filePath, doc_type):
    with open(filePath, "r") as csvfile:
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
            for i in range(len(data)): 
                if(data[i] == ""): data[i] = "null"

            #Create json from fields and data
            json_data = dict(zip(fields, data))
            bulkdocs.append(json_data)

            #Send batches of 100000 or less
            if(len(bulkdocs) >= 100000):
                json_bulk = {"docs": bulkdocs}
                x = requests.post("http://" + username + ":" + password + "@" + ip + ":" + port + "/gtfs/" + "_bulk_docs", json=json_bulk)
                bulkdocs = []
            counter += 1

        #Final batch (remaining data)
        json_bulk = {"docs": bulkdocs}
        x = requests.post("http://" + username + ":" + password + "@" + ip + ":" + port + "/gtfs/" + "_bulk_docs", json=json_bulk)
        print("For: ", doc_type, "sent a total of", counter, "rows")

#Add documents to table
#writetodbfromtxt("../data/gtfs/agency.txt", "Agency")
#writetodbfromtxt("../data/gtfs/calendar_dates.txt", "Calendar_date")
#writetodbfromtxt("../data/gtfs/calendar.txt", "Calendar")
#writetodbfromtxt("../data/gtfs/fare_attributes.txt", "Fare_attribute")
#writetodbfromtxt("../data/gtfs/fare_rules.txt", "Fare_rule")
#writetodbfromtxt("../data/gtfs/route_directions.txt", "Route_direction")
#writetodbfromtxt("../data/gtfs/routes.txt", "Route")
#writetodbfromtxt("../data/gtfs/shapes.txt", "Shape")
#writetodbfromtxt("../data/gtfs/stop_features.txt", "Stop_Feature")
#writetodbfromtxt("../data/gtfs/stop_times.txt", "Stop_time")
#writetodbfromtxt("../data/gtfs/stops.txt", "Stop")
#writetodbfromtxt("../data/gtfs/transfers.txt", "Transfer")
#writetodbfromtxt("../data/gtfs/trips.txt", "Trip")

#Create design document and views
print("Creating design document...")
data = {
        "id": "_design/queries", 
        "language": "javascript",
        "views": 
        {
            "getPCCDirections": 
            {
                "map": "function(doc) {if(doc.doc_type == 'Route_direction') {if(doc.direction_name == 'To Portland City Center') {emit(doc._id, doc);}}}"
            },
            "getRouteByID":
            {
                "map": "function(doc) {if(doc.doc_type == 'Route'){emit(doc.route_id, doc);}}"
            },
            "getMLR_routes":
            {
                "map": "function(doc){if(doc.doc_type == 'Route') {if(doc.route_long_name == 'MAX Red Line') {emit(doc);}}}"
            },
            "getTripsByRouteID":
            {
                "map": "function(doc) {if(doc.doc_type == 'Trip'){emit(doc.route_id, doc);}}"
            }
        }
    }
x = requests.put("http://" + username + ":" + password + "@" + ip + ":" + port + "/gtfs/_design/queriesdesigndocument", json=data)
print("     ", x.text)