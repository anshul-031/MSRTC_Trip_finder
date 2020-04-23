


# -*- coding: utf-8 -*-
"""
/***************************************************************************
 No_Of_Trips
                                 A QGIS plugin
 This plugin find the number of MSRTC bus trips between a Source and destination based on ABC data
                              -------------------
        begin                : 2020-04-16
        git sha              : $Format:%H$
        copyright            : (C) 2020 by Anshul the great
        email                : anshulgoel032@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import *
#from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import *
#from PyQt4.QtGui import QAction, QIcon
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from No_Of_Trips_dialog import No_Of_TripsDialog
import os.path
from qgis.core import QgsMessageLog


class No_Of_Trips:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgisInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'No_Of_Trips_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&No_Of_Trips')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'No_Of_Trips')
        self.toolbar.setObjectName(u'No_Of_Trips')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('No_Of_Trips', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = No_Of_TripsDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/No_Of_Trips/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'MSRTC Bus Trips FInder'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr(u'&No_Of_Trips'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
	#clearing all comboBox values 	
	self.dlg.User_Input_From_Hour.clear()
	self.dlg.User_Input_To_Hour.clear()	
	self.dlg.User_Input_From_Minute.clear()
	self.dlg.User_Input_To_Minute.clear()
	self.dlg.User_Input_Day.clear()	
	
	#setting all comboBox UI fields
	temp_list=[]
	for i in range(24):
		temp_list.append(str(i))
	self.dlg.User_Input_From_Hour.addItems(temp_list)
	self.dlg.User_Input_To_Hour.addItems(temp_list)	
	
	temp_list=[]
	for i in range(60):
		temp_list.append(str(i))
	self.dlg.User_Input_From_Minute.addItems(temp_list)
	self.dlg.User_Input_To_Minute.addItems(temp_list)
	

	Day_list=["Monday","Tuesday","Wednesday","Thrusday","Friday","Saturday", "Sunday"]
	self.dlg.User_Input_Day.addItems(Day_list)
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
	
	print "done"	

        if result:
	    import Plugin_codes_by_Anshul
	    Plugin_codes_by_Anshul.plugin_code_by_anshul_iitb(BusStopFrom = self.dlg.User_Input_Source.text(),BusStopTo =self.dlg.User_Input_Destination.text(),TimeFrom =str(str(self.dlg.User_Input_From_Hour.currentIndex())+':'+str(self.dlg.User_Input_From_Minute.currentIndex())), TimeTo=str(str(self.dlg.User_Input_To_Hour.currentIndex())+':'+str(self.dlg.User_Input_To_Minute.currentIndex())), Day=Day_list[self.dlg.User_Input_Day.currentIndex() ])
	    #plugin_code_by_anshul_iitb()
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
	    #QMessageBox.information(None,"Plugin non function by Anshul the great", "Abki baar anshul ki sarkar")
	   

	  
            pass
