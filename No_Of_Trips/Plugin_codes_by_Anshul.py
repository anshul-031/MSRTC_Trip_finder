#!/usr/bin/env python
# coding: utf-8

# In[1]:
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import resources
from No_Of_Trips_dialog import No_Of_TripsDialog
import os.path
from qgis.core import QgsMessageLog
from qgis.core import QgsVectorLayer, QgsDataSourceURI, QgsMapLayerRegistry, QgsRasterLayer 
from qgis.utils import *


#Initially Day parameter in the below function is not used anywhere.  
def plugin_code_by_anshul_iitb(BusStopFrom,BusStopTo,TimeFrom, TimeTo, Day ):

	#QMessageBox.information(None,"Plugin function by Anshul the great","\nSource: "+ BusStopFrom+"\nDestination: "+ BusStopTo+ "\nTime:  " +TimeFrom+" to "+ TimeTo+"\nDay"+ Day)
	import pandas
	import psycopg2
	import pandas.io.sql as psql
	QgsMessageLog.logMessage(	"\nUser_Input_Source-"+ BusStopFrom+\
					"\nUser_Input_Destination-"+ BusStopTo+\
					"\nUser_Input_From-"+ TimeFrom+\
					"\nUser_Input_To-"+ TimeTo +\
					"\nUser_Input_Day-"+ Day )
	try:
	    conn=psycopg2.connect("dbname='MTP_transportation' user='postgres' host='localhost' password='anshuL@iitb'")
	    #QMessageBox.information(None,"Plugin stage process","DB connected")
	    print "DB connected"
	except Exception as e:
	    QMessageBox.information(None,"Error","Database not connected")
	    return
	    print (e)

	#The mentioned below file contained the Nashik Bus stop Route Sequence with respective Route no.. This file has been derieved from Nashik All route Master file recieved 
	RouteSequenceFile = psql.read_sql("SELECT * FROM route_seq", conn)

	#The mentioned below file contains Route no. to Trip No. Mapping. This file has been derieved by Sinnar August 2019 ETIM data with Following query "Select distinct Trip_no, Route_no from ETIM_File"  
	RouteNoToTripNoFile=psql.read_sql('SELECT * FROM route_to_trip',conn)

	#ABC data of Sinner recieved of July month
	# ABCSinnarJul19File=pandas.read_csv('/home/anshulgoel031gmailcom/Desktop/MTP2/MTP/ABCJuly19_filtered.csv')
	ABCSinnarJul19File=psql.read_sql('SELECT * FROM ABCJuly19_filtered',conn)

	#This mentioned below file contains the Nashik Bus stop Route sequences Master file as recieved by Nashik depot   
	# RouteSequenceMasterFile= pandas.read_csv('/home/anshulgoel031gmailcom/Desktop/MTP2/MTP/All_Routes_Stops_Master_of_Nashik_Division.csv')
	RouteSequenceMasterFile=psql.read_sql('SELECT * FROM All_Routes_Stops_Master_of_Nashik_Division',conn)
	
	#Closing the databse
	conn.close()

	#Converting Bus Stop code to upper case so that we can comapre with database values with considering case sensitivity 
	BusStopFrom=BusStopFrom.upper()
	BusStopTo=BusStopTo.upper()

	#Assuming bus speed to be 30km/hour, We dont have Bus arrrival time and departure time on a particular bus stop, so based on route length and average speed expected time has been calculated 
	Bus_speed=30





	def abc(BusStopFrom, BusStopTo, TimeFrom, TimeTo):
	    #print (BusStopFrom)
	    #print (BusStopTo)
	    Required_Route_Sequence=[]
	    Required_From_KM=[]
	    for i in range(0,len(RouteSequenceFile)):
		if (RouteSequenceFile['Route_seq'][i].find(BusStopFrom)>-1 and             RouteSequenceFile['Route_seq'][i].find(BusStopTo)>-1 and             RouteSequenceFile['Route_seq'][i].find(BusStopFrom)<RouteSequenceFile['Route_seq'][i].find(BusStopTo)):
		    Required_Route_Sequence.append(RouteSequenceFile['Route_no'][i])
	#             Required_From_KM.append(RouteSequenceFile['KM'][i])
	    print len(Required_Route_Sequence)
	    print Required_Route_Sequence
	    QMessageBox.information(None,"All Possible Routes","Total No.of all possible routes are "+str(len(Required_Route_Sequence))+'\n\n Routes are '+ str(Required_Route_Sequence))
	    return Required_Route_Sequence
		


	# In[4]:


	Required_Route_Sequence=abc(BusStopFrom,BusStopTo, TimeFrom, TimeTo)


	# In[5]:


	# This functions return a DataFrame which contains Trip Numbers and Respective Route Numbers which have routes NSKCBS to SNNR without considering time
	# This Functions required inputs a 'list' which contains all route no. having routes from NSKCBS to SNNR irrespective of time
	def Route_to_trip(Required_Route_Sequence):
	    Required_Trips=[]
	    Required_Routes=[]
	    for i in range(0,len(Required_Route_Sequence)):
		for j in range(0,len(RouteNoToTripNoFile)):
		    if(Required_Route_Sequence[i]== RouteNoToTripNoFile['Route_no'][j]):
		        Required_Trips.append(RouteNoToTripNoFile['trip_no'][j])
		        Required_Routes.append(RouteNoToTripNoFile['Route_no'][j])
		        
	#   This 'dict' variable contains Trip Numbers and Respective Route Numbers which have routes NSKCBS to SNNR
	    dict ={'Trips':Required_Trips,'Routes': Required_Routes}
	#   print(len(Required_Trip_Sequence))
	#   Converting this Dict into DataFrame and returning via function 
	    df=pandas.DataFrame(dict)
	    print (len(df))
	    print(df)
	   
	    QMessageBox.information(None,"All possible Trips", "Total number of all possible Trips are "+str(len(df['Trips'].tolist()))+"\n\nTrips are "+ str([str(i) for i in df['Trips'].tolist()]))
	    return df

	#     return Required_Trip_Sequence


	# In[6]:


	# This Required_Trip_Route is the 'Dataframe' which contain Trip_no and Route_no having Bus Stops from NSKCBS to SNNR   
	Required_Trip_Route =Route_to_trip(Required_Route_Sequence)


	# In[7]:


	# This function return the list containinf "trip no." under Sinnar jurisdiction in month Oct 19 which provide NSKCBS to SNNR irrespective of time
	#Input of the function are two Dataframe one contians ABC Analysis of Sinnar Taluka For month Oct 2019
	#Second Dataframe contains all the (Trips, Route No.) pair under Nashik Jurisdiction which provide NSKCBS TO SNNR Service 
	def ReturnABCTripsIrrespectiveTime(Required_Trip_Route,ABCSinnarJul19File):
	    Trips=[]
	    Routes=[]
	    Trip_start_time=[]
	    for i in Required_Trip_Route.index:
		for j in ABCSinnarJul19File.index:
		    if (Required_Trip_Route['Trips'][i]==ABCSinnarJul19File['Trip'][j]):
		        Trips.append(Required_Trip_Route['Trips'][i])
		        Routes.append(Required_Trip_Route['Routes'][i])
		        Trip_start_time.append(ABCSinnarJul19File['Dept Time'][j])
	    dict= {'Trips':Trips, 'Routes':Routes,'Trip Start Time' :Trip_start_time }
	#     for i in Trips:
	#         for j in ABCSinnarJul19File.index:
	    df=pandas.DataFrame(dict)
	#     print len(df)
	#     print df
	    
	    return df


		


	# In[8]:



	ABCTripsIrrespectiveTime=ReturnABCTripsIrrespectiveTime(Required_Trip_Route,ABCSinnarJul19File)
	print ABCTripsIrrespectiveTime


	# In[9]:


	list_Route_no=list(dict.fromkeys(ABCTripsIrrespectiveTime['Routes'].tolist()))
	print list_Route_no
	list_Route_KM=[]
	# for i in ABCTripsIrrespectiveTime.index:
	#     for j in ABCSinnarJul19File.index:
	#         if ABCTripsIrrespectiveTime['Trips'][i].upper()==ABCSinnarJul19File['Trip'][j].upper():
	#             for k in RouteSequenceMasterFile.index:
	#                 if ABCTripsIrrespectiveTime['Routes'][i]==RouteSequenceMasterFile['ROUTE_NO'][k] and RouteSequenceMasterFile['BUS_STOP_CD'][k]==BusStopFrom:
	#                     print RouteSequenceMasterFile['KM'][k]
	#                     break
	list_Route_KM2=[]
	for i in list_Route_no:
	    for j in RouteSequenceMasterFile.index:
		if i==RouteSequenceMasterFile['ROUTE_NO'][j] and RouteSequenceMasterFile['BUS_STOP_CD'][j]==BusStopFrom:
		    print i, RouteSequenceMasterFile['KM'][j]
		    list_Route_KM.append(RouteSequenceMasterFile['KM'][j])
	#             break
		if i==RouteSequenceMasterFile['ROUTE_NO'][j] and RouteSequenceMasterFile['BUS_STOP_CD'][j]==BusStopTo:
		    print i, RouteSequenceMasterFile['KM'][j]
		    list_Route_KM2.append(RouteSequenceMasterFile['KM'][j])
		    break
	# df_Final=pandas.DataFrame()
	print list_Route_KM
	list_km=[]
	list_km2=[]
	for i in ABCTripsIrrespectiveTime['Routes'].tolist():
	    for j in list_Route_no:
		if i==j:
	#             df_final=df_final.append({'Route no.':ABCTripsIrrespectiveTime['Routes'][i],'Trip Start time':ABCTripsIrrespectiveTime['Trip Start time '][i],'Trips':ABCTripsIrrespectiveTime['Trips'][i] })
		    list_km.append(list_Route_KM[list_Route_no.index(j)])
		    list_km2.append(list_Route_KM2[list_Route_no.index(j)])
	print list_km
	ABCTripsIrrespectiveTime['Start KM']=list_km
	ABCTripsIrrespectiveTime['End KM']=list_km2
	ABCTripsIrrespectiveTime['Expected Time in hour']=(ABCTripsIrrespectiveTime['End KM']-ABCTripsIrrespectiveTime['Start KM'])/Bus_speed
	ABCTripsIrrespectiveTime.sort_values(by='Trip Start Time',ascending=True, inplace=True )
	ABCTripsIrrespectiveTime.reset_index(drop=True, inplace=True)

	print ABCTripsIrrespectiveTime


	# In[10]:


	#this function has been used to compare time
	def time_in_hour(t):
	    return float(t.split(':')[0])+float(t.split(':')[1])/60
	list_Final_output_index=[]

	for i in ABCTripsIrrespectiveTime.index:
	  #  print i
	    #converting time into hours and then comparing
	    if time_in_hour(ABCTripsIrrespectiveTime['Trip Start Time'][i])>=time_in_hour(TimeFrom) and    time_in_hour(ABCTripsIrrespectiveTime['Trip Start Time'][i])<=time_in_hour(TimeTo):
		list_Final_output_index.append(i)



		


	# In[11]:



	ABCTripsIrrespectiveTime.iloc[list_Final_output_index]


	# In[12]:

	
	l= ABCTripsIrrespectiveTime['Trips'][list_Final_output_index].tolist()
	l=str([str(r) for r in l])
	l='('+l[1:len(l)-1]+')'
	print l

	ABCTripsIrrespectiveTime['Trips'][list_Final_output_index].tolist()
#	QMessageBox.information(None,"Final output","No. of Bus Trips are "+str(len(ABCTripsIrrespectiveTime['Trips'][list_Final_output_index].tolist()))+"\n Final Trips betweeen provided bus stops and Time are :"+ l[1:len(l)-1])
	
	try:
	    conn=psycopg2.connect("dbname='MTP_transportation' user='postgres' host='localhost' password='anshuL@iitb'")
	    #QMessageBox.information(None,"Final output","DB connected")
	    print "DB connected"
	except:
	    QMessageBox.information(None,"Error","Database not connected")
	    print 'DB Not connected'
	str1=''
	for i in ABCTripsIrrespectiveTime['Trips'][list_Final_output_index].tolist():
		cur=conn.cursor()
		sql="select distinct abc_status from abc_july_final where trip_numbe='"+i+"'"	
		cur.execute(sql)
		temp=str(cur.fetchone())
		str1=str1+i+' , '+temp[2:len(temp)-1]+'\n'
	

	msg = QMessageBox()
	msg.setText("Final Number of Bus Trips are "+str(len(ABCTripsIrrespectiveTime['Trips'][list_Final_output_index].tolist()))+"\n Final Trips betweeen provided bus stops and Time are :"+ l[1:len(l)-1])

	msg.setInformativeText("ABC Details of trips")
	msg.setWindowTitle("Final Output")
	msg.setDetailedText("ABC details:\n"+str1)
	retval = msg.exec_()

	
	# In[13]:



	try:
	    conn=psycopg2.connect("dbname='MTP_transportation' user='postgres' host='localhost' password='anshuL@iitb'")
	    #QMessageBox.information(None,"Final output","DB connected")
	    print "DB connected"
	except:
	    QMessageBox.information(None,"Error","Database not connected")
	    print 'DB Not connected'
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
	  where trip_numbe in """ + l +')'
	# Here variable 'l' above in the above SQL query is the list containing all the required bus trips to be displayed  
	    if len(ABCTripsIrrespectiveTime['Trips'][list_Final_output_index].tolist())!=0:
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



	
	#if len(ABCTripsIrrespectiveTime['Trips'][list_Final_output_index].tolist())!=0:

	uri = QgsDataSourceURI()
	uri.setConnection("localhost", "5432", "MTP_transportation", "postgres", "anshuL@iitb")
	uri.setDataSource ("public", "output", "geom")
	vlayer=QgsVectorLayer (uri .uri(False), 'output', "postgres")
	QgsMapLayerRegistry.instance().addMapLayer(vlayer)

	#zooming to the output layer	
	vlayer.selectAll()
	mCanvas = iface.mapCanvas()
	mCanvas.zoomToSelected()
	vlayer.removeSelection()

	iface.mapCanvas().refreshAllLayers()
	print 'Linewidth and color changed'

	#setting the color of output layer named 'vlayer'
	vlayer.selectAll()
	iface.mapCanvas().setSelectionColor( QColor("blue") )
	
	print 'color changed'


	#setting line width of output layer named 'vlayer'  
	symbols = vlayer.rendererV2().symbols()
	for symbol in symbols:
	    symbol.setWidth(1)
	print 'Linewidth changed'

	# Refresh in order the see the changes
	iface.mapCanvas().refreshAllLayers()
	print 'Linewidth and color changed'

		#hiding layer Panel for bigger user dashboard  
#		from PyQt4.QtGui import QDockWidget 
#		for x in iface.mainWindow().findChildren(QDockWidget): 
#		    if x.objectName() == 'Layers': 
#			x.hide()
		
#zooming to the output layer	
#	vlayer.selectAll()
#	mCanvas = iface.mapCanvas()
#	mCanvas.zoomToSelected()
#	vlayer.removeSelection()







	
