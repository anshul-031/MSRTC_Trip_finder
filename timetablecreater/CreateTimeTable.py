# -*- coding: utf-8 -*-
"""
/***************************************************************************
 timetablecreater
                                 A QGIS plugin
 Creates MSRTC PHC Time Table of an Taluka
                              -------------------
        begin                : 2020-06-22
        git sha              : $Format:%H$
        copyright            : (C) 2020 by Anshul
        email                : anshulgoel031@gmail.com
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
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from CreateTimeTable_dialog import timetablecreaterDialog
import os.path


class timetablecreater:
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
            'timetablecreater_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&MSRTC PHC Time Table Creater')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'timetablecreater')
        self.toolbar.setObjectName(u'timetablecreater')

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
        return QCoreApplication.translate('timetablecreater', message)


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
        self.dlg = timetablecreaterDialog()

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
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/timetablecreater/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u''),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&MSRTC PHC Time Table Creater'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
	#clearing all comboBox values 	
	self.dlg.comboBox.clear()
	self.dlg.comboBox_2.clear()	
	self.dlg.comboBox_3.clear()

	#setting all comboBox UI fields
	self.dlg.comboBox.addItems(['Maharashtra'])
	self.dlg.comboBox_2.addItems(['Nashik'])	
	self.dlg.comboBox_3.addItems(['Nashik','Sinnar', 'Igatpuri','Trimbak','Niphad','Yeola','Peth','Dindori','Chandwad','Baglan', 'Deola', 'Kalwan','Malegaon','Nandgaon','Surgana'])


        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
	    print "State ",self.dlg.comboBox.currentIndex()
	    print "District ",self.dlg.comboBox_2.currentIndex()
	    print "Taluka ",self.dlg.comboBox_3.currentIndex()
	    from qgis.core import QgsMessageLog
	    from PyQt4.QtCore import *
	    from PyQt4.QtGui import *
	    from qgis.core import QgsMessageLog
	    from qgis.core import QgsVectorLayer, QgsDataSourceURI, QgsMapLayerRegistry, QgsRasterLayer 
	    from qgis.utils import *
		
	    if self.dlg.comboBox.currentIndex()!=0 or self.dlg.comboBox_2.currentIndex()!=0 or self.dlg.comboBox_3.currentIndex()!=1:
		QMessageBox.information(None,"Error", "Data Not Found for selected Taluka ")
	    else:
		import pandas
		df=pandas.read_csv('~/.qgis2/python/plugins/timetablecreater/abc.csv')
		import time
		time.sleep(2)		
		df.to_csv('~/Desktop/form4.csv', index=False)
		df=pandas.read_csv('~/.qgis2/python/plugins/timetablecreater/bcd.csv')
		df.to_csv('~/Desktop/PHCTimeTable.csv', index=False)
		QMessageBox.information(None,"Operation completed", "Form4 and PHCTimeTable has been created and saved to Form4.csv, PHCTimeTable.csv respectively on Desktop")
		pass


	    


            #pass
