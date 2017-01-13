import aprslib, sys, os, re, pprint
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from geoalchemy2 import Geometry
from setup_db import Base, APRS
import credentials

print "APRS Parser"

engine = create_engine('postgres://' + credentials.username + ':' + credentials.password + '@' + credentials.db_host + '/' + credentials.db_table)

print credentials.db_host
print credentials.db_table

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

def main(input):
	try:
		packet = aprslib.parse(input)
	
		pprint.pprint(packet)
		print "Lat:" + str(packet['latitude'])
		print "Lng:" + str(packet['longitude'])

		#insert into 
		the_geom = "SRID=4326;POINT(" + str(packet['longitude']) + " " + str(packet['latitude']) + ")"
		print the_geom
		new_aprs = APRS(latitude=packet['latitude'],
						longitude=packet['longitude'],
						packet_json=packet,
						geom=the_geom,
						srccallsign=packet['from'],
						dstcallsign=packet['to'],
						comment=packet['comment'],
						symbol=packet['symbol'],
						symboltable=packet['symbol_table']
						)

		session.add(new_aprs)
		session.commit()

	except:
		print "Unable to decode packet"
	
if __name__ == '__main__':

	print "APRS_Parser"
	
	#Collects packets from multimon-ng AFSK1200 demodulation
	
	while True:
		data = sys.stdin.readline()
		print "--PACKET DATA--"
		data = data.strip()
		data = re.sub(r"^(APRS:\s+)", "", data)
		print data
		print "--END OF PACKET DATA--"
		main(data)
	
	#this is a aprs packet from my TH-D74
	#data = 'KE8CRV-7>T2TQLZ,WIDE1-1,WIDE2-1:`p:El*C[/>^'
	
	#main(data)
	
