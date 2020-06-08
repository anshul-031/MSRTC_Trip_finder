#!/usr/bin/env python
# coding: utf-8

# In[1]:
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import resources
import os.path
from qgis.core import QgsMessageLog
from qgis.core import QgsVectorLayer, QgsDataSourceURI, QgsMapLayerRegistry, QgsRasterLayer 
from qgis.utils import *


#Initially Day parameter in the below function is not used anywhere.  
def plugin_code_by_anshul_iitb(trip_number):
	trip_number=trip_number.upper()
	import pandas
	import psycopg2
	import pandas.io.sql as psql
	QgsMessageLog.logMessage(trip_number)
	try:
	    conn=psycopg2.connect("dbname='MTP_transportation' user='postgres' host='localhost' password='anshuL@iitb'")
	    print "DB connected"
	except Exception as e:
	    QMessageBox.information(None,"Error","Database not connected")
	    return
	    print (e)
	
	try:
	    cur=conn.cursor()
	    sql='DROP TABLE IF EXISTS output;'
	    cur.execute(sql)
	    sql = """
	CREATE TABLE output AS (

	SELECT 
	   *
	FROM 
	  public.abc_july_final
	  where trip_numbe = '""" + trip_number +"')"
	    cur.execute(sql)
	    conn.commit()
	    cur.close()
	except Exception as e:
	    print (e)


	#Removing all layer if any present 		
	QgsMapLayerRegistry.instance().removeAllMapLayers()

	
	#loading BaseLayer as OSM
	uri="url=http://a.tile.openstreetmap.org/{z}/{x}/{y}.png&zmax=19&zmin=0&type=xyz"
	osm_layer=QgsRasterLayer(uri,'OSM','wms')
	if not osm_layer.isValid():
    	    print ("Layer failed to load!")
	QgsMapLayerRegistry.instance().addMapLayer(osm_layer)
	print 'Finished'

	uri = QgsDataSourceURI()
	uri.setConnection("localhost", "5432", "MTP_transportation", "postgres", "anshuL@iitb")
	uri.setDataSource ("public", "output", "geom")
	vlayer=QgsVectorLayer (uri .uri(False), 'output', "postgres")
	QgsMapLayerRegistry.instance().addMapLayer(vlayer)
	
	#setting the color of output layer named 'vlayer'
	vlayer.selectAll()
	iface.mapCanvas().setSelectionColor( QColor("blue") )
	iface.mapCanvas().zoomToSelected()
	print 'color changed'


	#setting line width of output layer named 'vlayer'  
	symbols = vlayer.rendererV2().symbols()
	for symbol in symbols:
	    symbol.setWidth(1)
	print 'Linewidth changed'

	# Refresh in order the see the changes
	iface.mapCanvas().refreshAllLayers()
	print 'Linewidth and color changed'

#	iface.zoomToActiveLayer()
	canvas = iface.mapCanvas()
	extent = vlayer.extent()
	canvas.setExtent(extent)
	



