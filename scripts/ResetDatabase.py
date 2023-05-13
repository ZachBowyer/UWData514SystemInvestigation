"""
Deletes database entirely as a reset mechanism if needed
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

#Delete database
x = requests.delete("http://" + username + ":" + password + "@" + ip + ":" + port + "/gtfs")
print(x.text)

#Show all databases
x = requests.get("http://" + username + ":" + password + "@" + ip + ":" + port + "/_all_dbs")
print(x.text)