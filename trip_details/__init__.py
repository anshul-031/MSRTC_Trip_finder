# -*- coding: utf-8 -*-
"""
/***************************************************************************
 trip_details
                                 A QGIS plugin
 This plugin would diplay a MSRTC bus trip details along with its path 
                             -------------------
        begin                : 2020-06-03
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
    """Load trip_details class from file trip_details.

    :param iface: A QGIS interface instance.
    :type iface: QgisInterface
    """
    #
    from .trip_details import trip_details
    return trip_details(iface)
