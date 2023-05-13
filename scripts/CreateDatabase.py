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

            #Insert row into database
            docName = str(doc_type) + str(counter)
            #print("Attempting to add", docName)
            x = requests.put("http://" + username + ":" + password + "@" + ip + ":" + port + "/gtfs/" + docName, json=json_data)
            #print("     ", x.content)
            counter += 1

#Add documents to table
print("Adding agency")
writetodbfromtxt("../data/gtfs/agency.txt", "Agency")
print("Adding calendar dates")
writetodbfromtxt("../data/gtfs/calendar_dates.txt", "Calendar_date")
print("Adding calendar")
writetodbfromtxt("../data/gtfs/calendar.txt", "Calendar")
print("Adding fare attributes")
writetodbfromtxt("../data/gtfs/fare_attributes.txt", "Fare_attribute")
print("Adding fare rules")
writetodbfromtxt("../data/gtfs/fare_rules.txt", "Fare_rule")
print("Adding route directions")
writetodbfromtxt("../data/gtfs/route_directions.txt", "Route_direction")
print("Adding routes")
writetodbfromtxt("../data/gtfs/routes.txt", "Route")
print("Adding shapes")
writetodbfromtxt("../data/gtfs/shapes.txt", "Shape")
print("Adding stop features")
writetodbfromtxt("../data/gtfs/stop_features.txt", "Stop_Feature")
print("Adding stop times")
writetodbfromtxt("../data/gtfs/stop_times.txt", "Stop_time")
print("Adding stops")
writetodbfromtxt("../data/gtfs/stops.txt", "Stop")
print("Adding transfers")
writetodbfromtxt("../data/gtfs/transfers.txt", "Transfer")
print("Adding trips")
writetodbfromtxt("../data/gtfs/trips.txt", "Trip")