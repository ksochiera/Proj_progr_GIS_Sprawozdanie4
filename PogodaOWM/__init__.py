# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PogodaOWM
                                 A QGIS plugin
 Dodaje warstwę wektorową z informacjami pogodowymi
                             -------------------
        begin                : 2015-01-06
        copyright            : (C) 2015 by Krzysztof Sochiera
        email                : krzsoch@gmail.com
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
    """Load PogodaOWM class from file PogodaOWM.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .PogodaOWM import PogodaOWM
    return PogodaOWM(iface)
