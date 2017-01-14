# open-gis
Open Source GIS

This project uses several technologies including:

* [Geoserver](http://geoserver.org)
* [PostGRESQL](https://www.postgresql.org/)
* [Post GIS Extension](http://www.postgis.net/)
* [OpenLayers](http://openlayers.org/)
* [QGIS](http://www.qgis.org/en/site/)
* Raspberry Pi
* Ubuntu Server
* Oracle Virtualbox
* RTL-2832U Software Defined Radio

##Purpose

Build a geographic information system (GIS) that can be quickly setup and deployed in an offline environment.  The GIS will be updated over the air using digital modes and python script to parse and insert geospatial objects.  The GIS can be updated over the air or by using desktop GIS software such as QQIS.   The  database will allow automated map production.

##Components

###Webserver

* ODroid C2
* Ubuntu Server
* Geoserver
* Apache2
* Python support via CGI-BIN
* OpenLayers 

###Database

* ODroid C2
* Ubuntu Server
* PostgreSQL
* Post GIS Extension
* Data

###Radio

* [RTL-2832U](https://www.amazon.com/gp/product/B00QFCNNV0/ref=oh_aui_detailpage_o04_s00?ie=UTF8&psc=1)
* [Osmocom RTL-SDR](http://sdr.osmocom.org/trac/wiki/rtl-sdr)
* [multimon-ng](https://github.com/EliasOenal/multimon-ng)
* georeceiver.py - custom python script to parse output of multimon-ng
* aprs_parser.py - custom script to decode packets
* [fldigi](http://www.w1hkj.com/)
* ODroid C2

###Miscellaneous Software

* arecord
* sox
* GNURadio 
* git

###Miscellaneous Parts

* [Raspberry Pi Official 7" Touchscreen](https://www.element14.com/community/docs/DOC-78156/l/raspberry-pi-7-touchscreen-display)
* [DS3231 Real Time Clock](https://www.amazon.com/gp/product/B00HF4NUSS/ref=oh_aui_detailpage_o00_s00?ie=UTF8&psc=1)
* [Touchscreen Case](https://www.amazon.com/gp/product/B01HKWAJ6K/ref=oh_aui_detailpage_o02_s00?ie=UTF8&psc=1)
* [Copper Heatsinks for Pi](https://www.amazon.com/gp/product/B00RKJG2HY/ref=oh_aui_detailpage_o04_s00?ie=UTF8&psc=1)
* [Headphone Splitter](https://www.amazon.com/gp/product/B0151G0LB0/ref=oh_aui_detailpage_o09_s00?ie=UTF8&psc=1)
* [Mini Keyboard](https://www.amazon.com/gp/product/B00I5SW8MC/ref=oh_aui_detailpage_o04_s00?ie=UTF8&psc=1)

