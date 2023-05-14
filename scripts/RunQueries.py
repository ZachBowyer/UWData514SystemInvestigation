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

#Extract routes

#Get route data


#function (doc) {
#  if(doc.doc_type == 'Route_direction') {
#    if(doc.direction_name == 'To Portland City Center') {
#        emit(doc._id, 1);
#    }
#  }
#}
#
##Get route by routeid
#http://127.0.0.1:5984/testdb/_design/designdoc/_view/testview?key=[12,3]
#http://localhost:5984/<database>/_design/<designdoc>/_view/<viewname>?key=<pid2>