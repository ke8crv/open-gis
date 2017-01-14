'''
georeceiver.py

Purpose: to receive digital mode transmissions, parse coordinates, and submit
to database

'''
import sys, re, os
import sqlite3
import readchar
#from mgrspy import mgrs

def buildSqliteTest(data):

    db = sqlite3.connect(os.path.join(os.getcwd(), "testdb.sqlite"))


    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE geodata(id INTEGER PRIMARY KEY, latitude REAL,
                           longitude REAL, email TEXT, date_rx DATETIME,
                           msg TEXT)
    ''')
    db.commit()

    db.close()

def insertSqliteTest(lat1, lng1, email1, date1, msg1):
                     
    #http://pythoncentral.io/introduction-to-sqlite-in-python/
    db = sqlite3.connect(os.path.join(os.getcwd(), "testdb.sqlite"))
                     
    cursor = db.cursor()

    #at1 = 44.2134
    #lng1 = -88.3434
    #email1 = "ke8crv@gmail.com"
    
    # Insert user 1
    cursor.execute('''INSERT INTO geodata(latitude, longitude, email, date_rx, msg)
                  VALUES(?,?,?,?,?)''', (lat1,lng1,email1,date1,msg1))

    #print('First user inserted')

    db.commit()

    db.close()

def retrieveSqliteTest(data):
                     
    db = sqlite3.connect(os.path.join(os.getcwd(), "testdb.sqlite"))
                     
    cursor = db.cursor()

    cursor.execute('''SELECT latitude, longitude, email, date_rx FROM geodata''')
                     
    users = cursor.fetchall() #retrieve the first row
    for row in users:
        print('{0},{1} : {2} {3}'.format(row[0], row[1], row[2], row[3]))
    
    db.close()
                     
def createPointFromXY(data):

    print "Creating point data from xy"

    '''
    INSERT INTO table(the_geom, the_name)
    VALUES(GeomFromEWKT('SRID=312;POINT(-126.4 45.32)'),'A Place')

    SRID=32632;POINT(0 0)
    SRID=4326 for WGS 84
    SRID=3785 for Web Mercator    
    '''
    

def getDate(item):
    d = None
    
    p = re.compile('(\d\d\d\d-\d\d-\d\d)')
    m = p.search(item)
 
    if m:
        d = m.group(1)

    return d

def getLatLng(item):
    lat = None
    lng = None
    
    p = re.compile('(-?\d+\.\d+),(-?\d+\.\d+)')
    m = p.search(item)
 
    if m:
        lat = m.group(1)
        lng = m.group(2)
    return lat,lng

'''
def getEmail(item):
    email = None

    p = re.compile('([\w\-\.]+@(\w[\w\-]+\.)+[\w\-]+)')
    m = p.search(item)

    if m:
        email = m.group(1)

    return email
'''

def getEmail(item):

    email = None

    p = re.compile('MY (NEIGHBORHOOD)')
    m = p.search(item)

    if m:
        email = m.group(1)
        
    return email

def checkData(data):

    #Get all data items between []
    items_pattern = re.compile('\[(.*?)\]')
    matches = items_pattern.findall(data)
    
    params ={}
    params['lat'] = None
    params['lng'] = None
    params['email'] = None
    params['date_rx'] = None
    
    for item in matches:
        
        lat,lng = getLatLng(item)
        if lat is not None and lng is not None:
            #print "Lat/Lng: " + str(lat) + " " + str(lng)
            params['lat'] = lat
            params['lng'] = lng

        d = getDate(item)
        if d is not None:
            #print "Date: " + str(d)
            params['date_rx'] = d

        email = getEmail(item)
        if email is not None:
            #print "Email: " + str(email)
            params['email'] = email

    print matches
        
    #print "insert(" + params['lat'] + "," + params['lng'] + "," + params['email'] + "," + params['date_rx'] + ")"
    
    insertSqliteTest(params['lat'],params['lng'],params['email'],params['date_rx'])

def checkData2(item):
    print item
    params ={}
    params['lat'] = None
    params['lng'] = None
    params['email'] = None
    params['date_rx'] = None
    params['msg'] = None

    lat,lng = getLatLng(item)
    if lat is not None and lng is not None:
        #print "Lat/Lng: " + str(lat) + " " + str(lng)
        params['lat'] = lat
        params['lng'] = lng

    d = getDate(item)
    if d is not None:
        #print "Date: " + str(d)
        params['date_rx'] = d

    email = getEmail(item)
    if email is not None:
        #print "Email: " + str(email)
        params['email'] = email

    params['msg'] = item

    print params

    #Make sure at least one of the params has data before
    #running an insert statement
    submit = False
    for k,v in params.iteritems():
        if v is not None:
            submit = True
        
    if submit:
        insertSqliteTest(params['lat'],params['lng'],params['email'],params['date_rx'], params['msg'])
        #print "insert(" + str(params['lat']) + "," + str(params['lng']) + "," + str(params['email']) + "," + str(params['date_rx']) + "," +str(params['msg']) + ")"
        print "\n"
        
def main(data):

    #print "------------------------"
    #print "Georeceiver.py"
    #print "------------------------\n\n"
    #print data
    #checkData(data)
    checkData2(data)

    #buildSqliteTest(data)
    #insertSqliteTest(data)
    #retrieveSqliteTest(data)
    
    
    #print "Done"
    #print "------------------------\n\n"

if __name__ == "__main__":
   
    data = "start"
    word_array=[]
    while True:
        #data = sys.stdin.readline(1)
        print data
        data = readchar.readchar()
        if data == " ":
            print "".join(word_array)
            word_array=[]
        elif data == "q":
            sys.exit(0)
        else:
            word_array.append(data)
        
        #main(data)

       
