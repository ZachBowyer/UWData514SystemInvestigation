""" 
Create Database
Fill information in database
Create design document
Create views
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

#Get database information
x = requests.get("http://" + username + ":" + password + "@" + ip + ":" + port)
print(x.text)

#Create database instance
x = requests.put("http://" + username + ":" + password + "@" + ip + ":" + port + "/gtfs")
print(x.text)