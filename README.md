# UWData514SystemInvestigation
Final project for UW MSDS Data 514 course
This repository was made to store the code for my database implementation and to answer three questions about a dataset.
I implemented Apache CouchDB: https://couchdb.apache.org/
I used the dataset: http://developer.trimet.org/GTFS.shtml 
I answered the three questions:
1. List routes that go to 'Portland City Center'
2. On which days does the MAX Red Line run within the given time range?"
3. Which modes of public transport (routes) are available near ‘PSU Urban Center’ 
   at the latest possible time before 9.00 AM (ignore date)?
   Display stops around PSU Urban Center, type of stop location, type of transportation (route), 
   it’s time of arrival and direction (direction name)

# Files
/data/gtfs/agency.txt - From GTFS dataset  
/data/gtfs/calendar_dates.txt - From GTFS dataset   
/data/gtfs/calendar.txt - From GTFS dataset  
/data/gtfs/fare_attributes.txt - From GTFS dataset  
/data/gtfs/fare_rules.txt - From GTFS dataset  
/data/gtfs/feed_info.txt - From GTFS dataset  
/data/gtfs/linked_datasets.txt - From GTFS dataset  
/data/gtfs/route_directions.txt - From GTFS dataset  
/data/gtfs/routes.txt - From GTFS dataset  
/data/gtfs/shapes.txt - From GTFS dataset  
/data/gtfs/stop_features.txt - From GTFS dataset  
/data/gtfs/stop_times.txt - From GTFS dataset  
/data/gtfs/stops.txt - From GTFS dataset  
/data/gtfs/transfers.txt - From GTFS dataset  
/data/gtfs/trips.txt - From GTFS dataset  
/data/DATA.md - Description and profile of the GTFS dataset  
/scripts/createdatabase.py - Creates database, appends documents, creates design document, creates views  
/scripts/resetdatabase.py - Deletes database  
/scripts/runqueries.py - Combines client code and view calls to answer the three questions  
.gitignore - Excludes data and credentials files (.txt)  
CouchDBInvestigation.pdf - High level overview of Apache CouchDB  
credentials.txt (hidden) - Contains username, password, port, and ip for the couchDB server  
Presentation.pptx - Slides that describe the project  
README.md - This file, high level overview  
setup.py - Downloads and unzips GTFS dataset into /data/gtfs  
