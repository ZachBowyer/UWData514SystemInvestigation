"""
This python file installs data to your machine and puts it in the /data folder.
"""
import gdown
import zipfile
import os

#Download GTFS transit data as a .zip (This link may not work forever)
URL1 = 'http://developer.trimet.org/schedule/gtfs.zip'
gdown.download(URL1, 'data/gtfs.zip', quiet=False)

#Unzip the data
with zipfile.ZipFile('data/gtfs.zip', 'r') as zip_ref:
    zip_ref.extractall('data/gtfs')

#Remove old zip file
os.remove('data/gtfs.zip')