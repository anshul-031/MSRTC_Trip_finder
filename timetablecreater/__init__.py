# -*- coding: utf-8 -*-
"""
/***************************************************************************
 timetablecreater
                                 A QGIS plugin
 Creates MSRTC PHC Time Table of an Taluka
                             -------------------
        begin                : 2020-06-22
        copyright            : (C) 2020 by Anshul
        email                : anshulgoel031@gmail.com
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
    """Load timetablecreater class from file timetablecreater.

    :param iface: A QGIS interface instance.
    :type iface: QgisInterface
    """
    #
    from .CreateTimeTable import timetablecreater
    return timetablecreater(iface)
