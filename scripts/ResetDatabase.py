"""
Deletes database entirely as a reset mechanism if needed
"""
import requests

CREDENTIALSFILEPATH = '../credentials.txt'
with open(CREDENTIALSFILEPATH, 'r', encoding="utf8") as credentialFileObject:
    username = credentialFileObject.readline().strip()
    password = credentialFileObject.readline().strip()
    ip = credentialFileObject.readline().strip()
    port = credentialFileObject.readline().strip()
    credentialFileObject.close()
    url = "http://" + username + ":" + password + "@" + ip + ":" + port

#Delete database
x = requests.delete(url + "/gtfs", timeout=600)
print(x.text)

#Show all databases
x = requests.get(url + "/_all_dbs", timeout=600)
print(x.text)
