
import os
import sys
import json
import re
from pymongo import MongoClient
from math import atan2, radians
from numpy import math
from cmath import sqrt, sin, cos


def FindBusinessBasedOnCity(cityToSearch, saveLocation1, collection):
    cur = collection.find( {'city':  re.compile(cityToSearch, re.IGNORECASE)})
    file = open(saveLocation1,"w")
    for i in cur:
            City = str(i['city'])
            State = str(i['state'])
            Name = str(i['name'])
            Address = str((i['full_address'])).replace("\n", ", ");
            file.write( Name.upper() + "$" + Address.upper() + "$" + City.upper() + "$" + State.upper() + "\n")
    file.close()

def FindBusinessBasedOnLocation(categoriesToSearch, myLocation, maxDistance, saveLocation2, collection):
    temp = []
    for i in categoriesToSearch:
	     temp.append(i.title());
    abc = collection.find({"categories": {"$all": temp}})
    latit = float (myLocation[0])
    longi = float (myLocation[1])
    source_lat = radians(latit)
    source_long = radians(longi)
    R=3959
    file=open(saveLocation2,"w")
    for i in abc:
        dest_lat = radians(i['latitude'])
        dest_long = radians(i['longitude'])
	dist_lat = (dest_lat - source_lat)
        dist_long = (dest_long - source_long)
        a = math.sin(dist_lat / 2) * math.sin(dist_lat / 2)  + math.cos(source_lat) * math.cos(dest_lat) * math.sin(dist_long / 2) * math.sin(dist_long / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c
        if (distance <= maxDistance):
            file.write(i['name'].encode("utf-8").upper() + "\n")
    file.close()
    
