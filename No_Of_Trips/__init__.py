# -*- coding: utf-8 -*-
"""
/***************************************************************************
 No_Of_Trips
                                 A QGIS plugin
 This plugin find the number of MSRTC bus trips between a Source and destination based on ABC data
                             -------------------
        begin                : 2020-04-16
        copyright            : (C) 2020 by Anshul the great
        email                : anshulgoel032@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load No_Of_Trips class from file No_Of_Trips.

    :param iface: A QGIS interface instance.
    :type iface: QgisInterface
    """
    #
    from .No_Of_Trips import No_Of_Trips
    return No_Of_Trips(iface)
