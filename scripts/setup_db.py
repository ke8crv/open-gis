import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Text, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from geoalchemy2 import Geometry
import credentials
Base = declarative_base()

class APRS(Base):
	__tablename__ = 'APRS'
	# Here we define columns for the table person
	# Notice that each column is also a normal Python instance attribute.
	id = Column(Integer, primary_key=True)
	srccallsign = Column(String(255))
	dstcallsign = Column(String(255))
	symbol = Column(String(20))
	symboltable = Column(String(20))
	comment = Column(String(255))
	latitude = Column(Float)
	longitude = Column(Float)
	packet_json = Column(JSON)
	geom = Column(Geometry(geometry_type='POINT', srid=4326))
	
#engine = create_engine('sqlite:///test.sqlite')
engine = create_engine('postgres://' + credentials.username + ':' + credentials.password +'@' + credentials.db_host +'/' + credentials.db_table)
#engine = create_engine('postgres://geonode:geonode@192.168.100.123/geonode_data')
#db = create_engine('postgres+psycopg2://' + username + ':' + geonode +'@' + db_host + '/' + db_table')

Base.metadata.create_all(engine)
