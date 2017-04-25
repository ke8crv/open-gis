'''
Extract_feature_service.py
Author: Matt McCormick
Date 1/13/2017

Purpose:
ESRI Feature Service typically have a 1000 max record limit by default.

It is possible using REST to find out how many records are available and get all the objectids.

This script breaks the total into sets of 1000, submits queries, and saves the JSON to disk.

Notes:
In ArcMap, use the JSON_To_Features function to display the data on map or load into a geodatabase

ogr2ogr -f GeoJSON test.json <url to query> OGRGeoJSON

https://github.com/Esri/arcgis-to-geojson-utils
http://terraformer.io/

https://gist.github.com/migurski/3759608/


Todo:
DONE: Figure out how to successfully use POST requests.

DONE Figure out how to get the MAX Records and use that to make groups.
https://gisago.mcgi.state.mi.us/arcgis/rest/services/DNR/dnrTrails/MapServer/0?f=json

look for maxRecordCount


Figure out differences between ArcGIS server versions and what parameters exists


DONE How to download all layers within a mapservice, ie parse this
https://gisago.mcgi.state.mi.us/arcgis/rest/services/DNR/dnrTrails/MapServer?f=json

Add a timestamp to json files

DONE Add some random timer for sleep in between requests

Figure out how to merge json files
http://stackoverflow.com/questions/32307393/are-there-any-efficient-way-to-concatenate-two-json-files-in-python
import json
a = json.loads(open('js1.json').read())
b = json.loads(open('js2.json').read())

def combine_dicts(*dicts):
    return reduce(lambda dict1, dict2: dict(zip(dict1.keys() + dict2.keys(), dict1.values() + dict2.values())), dicts)

c = combine_dicts(a, b)



'''
import urllib2, urllib, csv, json, pprint  #, #itertools
import time, os
from random import randint

'''
buildHeader
this was written to handle WebEOC records that don't
all have the same attributes
'''
def buildHeader(data_list):

    tmp = {}

    for row in data_list:
        for k in row.keys():
            if k in tmp:
                tmp[k] += 1
            else:
                tmp[k] = 1

    return tmp

def saveCSV(filename, data_list):

	
	
    with open(filename, 'wb') as csvfile:

        for x in data_list:
            csvfile.write(str(x) + "\n")

def saveFile(filename, data):

    output_dir = "c:\Temp"
	
    with open(os.path.join(output_dir,filename), 'wb') as my_file:
        my_file.write(data)
        

def requestAndSave(query_url, params, filename, method):

    data = urllib.urlencode(params)

    if method == "GET":

        full_url = query_url + '?' + data

        try:
            request = urllib2.Request(full_url)
            response = urllib2.urlopen(request)
            content = response.read()
            saveFile(filename, content)
        except IOError as e:
            print "Error: ", e

    elif method == "POST":
        
        try:
            request = urllib2.Request(query_url, data)
            response = urllib2.urlopen(request)
            content = response.read()
            saveFile(filename, content)
            
        except IOError as e:
            print "Error: ", e

    return

def getLayers(mapserver_url):

    mapserver_url_json = mapserver_url + "?f=json"

    print "Mapserver json url: " + mapserver_url
    
    try:
        request = urllib2.Request(mapserver_url_json)
        response = urllib2.urlopen(request)
        content = response.read()

        my_json = json.loads(content)
        layers = []
        #print my_json['layers']
        for lyr in my_json['layers']:
            #print lyr['id']
            #print lyr['name']

            tmp = {"filename": lyr['name'].replace(' ', '_'),
                   "url": mapserver_url + "/" + str(lyr['id'])
                   }

            layers.append(tmp)
        
            
        return layers
        #saveFile(filename, content)
        
    except IOError as e:
        print "Error: ", e
            
    

    
def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    if l:
        for i in range(0, len(l), n):
            yield l[i:i + n]

def getMaxRecordCount(layer_url):

    maxRecordCount = 1000
    layer_info_url = layer_url + "?f=json"
    print layer_info_url

    try:
        request = urllib2.Request(layer_info_url)
        response = urllib2.urlopen(request)
        content = response.read()

        my_json = json.loads(content)

        if my_json['currentVersion'] >= 10.3:
            maxRecordCount = my_json['maxRecordCount']

        return maxRecordCount

    except IOError as e:
        print "Error: ", e
        return 0
    
    

def downloadLayer(layer_url, filename):

    params = {"text": "",
              "geometry":"",
              "geometryType":"esriGeometryEnvelope",
              "inSR":"",
              "spatialRel":"esriSpatialRelIntersects",
              "relationParam":"",
              "objectIds":"",
              "where":"1=1",
              "time":"",
              "returnIdsOnly":"true",
              "returnGeometry":"false",
              'maxAllowableOffset':0,
              "outSR":"",
              "outFields":"",
              "f":"json"
              }

    data = urllib.urlencode(params)

    #print json.dumps(data)

    maxRecordCount = getMaxRecordCount(layer_url)
    
    #rest_url = r"http://gis.fema.gov/REST/services/NSS/FEMA_NSS/MapServer/5/query"
    query_url = layer_url + "/query"

    print query_url
    
    try:
        request = urllib2.Request(query_url, data)
        response = urllib2.urlopen(request)
        content = response.read()
        #saveFile("fema_nss_post.json", content)
        #saveFile(filename + ".json", content)

        my_json = json.loads(content)
        requests = list(chunks(my_json['objectIds'], maxRecordCount))

        #print "Length:" + str(len(requests))
        ctr = 0
        for i in requests:
            ctr += 1
            #print "Len:" + str(len(i))
            tmp_params = params
            tmp_params['where'] = "OBJECTID IN(" + ','.join(str(e) for e in i)+ ")"
            tmp_params['outFields'] = "*"
            tmp_params['returnIdsOnly'] = "false"
            tmp_params['returnGeometry'] = "true"
            tmp_filename = filename + "_" + str(ctr) + ".json"
            print tmp_filename
            print "Working...",
            requestAndSave(query_url, params, tmp_filename, "POST")
            print "Done"
            #this is to throttle the requests
            #throttle in between 1 sec and 10 sec the layer downloads to hopefully not get blocked
            sleep_delay = randint(1,10)
            print "Delay: " + str(sleep_delay)
            time.sleep(sleep_delay)
            #pause = raw_input("hit enter to continue")

        #print "OBJECTID IN(" + ','.join(str(e) for e in requests[0])+ ")"
            
    except IOError as e:
        print "Error: ", e

def test():
    mapserver_url = r"http://gisago.mcgi.state.mi.us/arcgis/rest/services/DNR/dnrTrails/MapServer"
    #mapserver_url = r"https://gisp.mcgi.state.mi.us/arcgis/rest/services/DNR/Wildfire/MapServer"
    #mapserver_url = r"https://gisago.mcgi.state.mi.us/arcgis/rest/services/BaseMap/StreetMap/MapServer"
    
    output_dir = r"c:\Temp\DNR"
	
    print "Mapserver:" + mapserver_url
    layers  = getLayers(mapserver_url)
    for layer in layers:
        print layer['filename'],'\t',layer['url']

        downloadLayer(layer['url'], layer['filename'])
        #throttle in between 5 sec and 60 sec the layer downloads to hopefully not get blocked
        sleep_delay = randint(5,60)
        print "Delay: " + str(sleep_delay)
        time.sleep(sleep_delay)
  
def test2():

    #rest_url = r"http://gis.fema.gov/REST/services/NSS/FEMA_NSS/MapServer/5/query"
    #layer_url = r"http://gis.fema.gov/REST/services/NSS/FEMA_NSS/MapServer/5"
    #filename = "fema_nss_post.json"
    #layer_url = r"http://gisago.mcgi.state.mi.us/arcgis/rest/services/DNR/dnrTrails/MapServer/13"
    #filename = "mdnr_designated_snowmobile_trails"
    #layer_url = r"https://gisp.mcgi.state.mi.us/arcgis/rest/services/MEDC/PureMichigan_MapService/MapServer/0"
    #filename = "mdec_pure_michigan_properties"
    layer_url = r"http://gisago.mcgi.state.mi.us/arcgis/rest/services/BaseMap/StreetMap/MapServer/1"
    filename = "great_lakes"
    downloadLayer(layer_url, filename)
    
    #print getMaxRecordCount(layer_url)
    
if __name__ == "__main__":

    start_time = time.time()
    #main()
    test2()
    #test()
    end_time = time.time()
    print("--- %s seconds ---" % (time.time() - start_time))
    
    
