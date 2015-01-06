# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PogodaOWM
                                 A QGIS plugin
 Dodaje warstwę wektorową z informacjami pogodowymi
                              -------------------
        begin                : 2015-01-06
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Krzysztof Sochiera
        email                : krzsoch@gmail.com
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
import resources_rc
# Import the code for the dialog
from PogodaOWM_dialog import PogodaOWMDialog
import os.path


class PogodaOWM:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
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
            'PogodaOWM_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = PogodaOWMDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&PogodaOWM')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'PogodaOWM')
        self.toolbar.setObjectName(u'PogodaOWM')

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
        return QCoreApplication.translate('PogodaOWM', message)


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

        icon_path = ':/plugins/PogodaOWM/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'PogodaOWM'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&PogodaOWM'),
                action)
            self.iface.removeToolBarIcon(action)


    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
#Programowanie w GIS
#Sprawozdanie nr 4
#Krzysztof Sochiera
from qgis.core import QgsVectorLayer, QgsField, QgsMapLayerRegistry  
from PyQt4.QtCore import QVariant  
import urllib, json, os, time, datetime
from pprint import pprint
warstwa=QgsVectorLayer("Point?crs=epsg:4326", "Pogoda", "memory")  
warstwa.startEditing()
warstwa.LayerData=warstwa.dataProvider()
ncrs=QgsCoordinateReferenceSystem(4326)
warstwa.LayerData.addAttributes([QgsField("Miasto", QVariant.String), QgsField("Temperatura", QVariant.Int), QgsField("maxTemperatura", QVariant.Int), QgsField("minTemperatura", QVariant.Int), QgsField("Cisnienie", QVariant.Int),  QgsField("Wilgotnosc", QVariant.Int), QgsField("PredkoscWiatru", QVariant.Int), QgsField("KierunekWiatru", QVariant.Int),  QgsField("Zachmurzenie", QVariant.Int),  QgsField("Opad", QVariant.String)])#
warstwa.commitChanges()
'show Layer in QGIS'  
QgsMapLayerRegistry.instance().addMapLayer(warstwa) 

if os.path.exists("current.json"):
    now=datetime.datetime.now()
    print "[Obecna data:] ", now
    mtimesys=os.path.getmtime("current.json")
    mtime=datetime.datetime.fromtimestamp(mtimesys)
    print "[Data zapisu/modyfikacji pliku:] ", mtime
    diff=(now-mtime).seconds
    print "[Czas od modyfikacji pliku w sekundach:] ", diff
    if diff< 600:
        print "Zaimportowano z pliku"
        with open("current.json", "r") as current:
            myfile=json.load(current)
            
    else:
        print "Zaimportowano z sieci"
        link = "http://api.openweathermap.org/data/2.5/group?id=3082707,3093692,3081368,3097257,7533404,3096053,3103096,7530806,3102987,7533042,3096576&units=metric&APPID=1016fe2f1e51cb209c94920d91243bd1"

        f = urllib.urlopen(link)
        myfile = json.load(f)
        with open("current.json","w") as update:
            myfilestr=json.dump(myfile,update)
else:
    print "Zaimportowano z sieci"
    link ="http://api.openweathermap.org/data/2.5/group?id=3082707,3093692,3081368,3097257,7533404,3096053,3103096,7530806,3102987,7533042,3096576&units=metric&APPID=1016fe2f1e51cb209c94920d91243bd1"

    f = urllib.urlopen(link)
    myfile = json.load(f)
    with open("current.json","w") as update:
        myfilestr=json.dump(myfile,update)
        
weather=myfile["list"]

wroclaw= weather[2]
wroclawcoord=wroclaw["coord"]
wroclawmain=wroclaw["main"]
wroclawwind=wroclaw["wind"]
wroclawclouds=wroclaw["clouds"]
wroclawwe=wroclaw["weather"]
wroclawWeather=wroclawwe[0]
wroclawDesc=wroclawWeather["description"]
wroclawName=wroclaw["name"]
wroclawTemp=wroclawmain["temp"]
wroclawTempMin=wroclawmain["temp_min"]
wroclawTempMax=wroclawmain["temp_max"]
wroclawPressure=wroclawmain["pressure"]
wroclawHumidity=wroclawmain["humidity"]
wroclawWindSp=wroclawwind["speed"]
wroclawWindDir=wroclawwind["deg"]
wroclawClouds=wroclawclouds["all"]
valWroclaw=[wroclawName,wroclawTemp,wroclawTempMin,wroclawTempMax,wroclawPressure,wroclawHumidity,wroclawWindSp,wroclawWindDir,wroclawClouds,wroclawDesc]
wroclawLat=wroclawcoord["lat"]
wroclawLon=wroclawcoord["lon"]
print "Wroclaw ... OK"
legnica=weather[1]
legnicacoord=legnica["coord"]
legnicamain=legnica["main"]
legnicawind=legnica["wind"]
legnicaclouds=legnica["clouds"]
legnicawe=legnica["weather"]
legnicaWeather=legnicawe[0]
legnicaDesc=legnicaWeather["description"]
legnicaName=legnica["name"]
legnicaTemp=legnicamain["temp"]
legnicaTempMin=legnicamain["temp_min"]
legnicaTempMax=legnicamain["temp_max"]
legnicaPressure=legnicamain["pressure"]
legnicaHumidity=legnicamain["humidity"]
legnicaWindSp=legnicawind["speed"]
legnicaWindDir=legnicawind["deg"]
legnicaClouds=legnicaclouds["all"]
valLegnica=[legnicaName,legnicaTemp,legnicaTempMin,legnicaTempMax,legnicaPressure,legnicaHumidity,legnicaWindSp,legnicaWindDir,legnicaClouds,legnicaDesc]
legnicaLat=legnicacoord["lat"]
legnicaLon=legnicacoord["lon"]
print "Legnica ... OK"

walbrzych=weather[0]
walbrzychcoord=walbrzych["coord"]
walbrzychmain=walbrzych["main"]
walbrzychwind=walbrzych["wind"]
walbrzychclouds=walbrzych["clouds"]
walbrzychwe=walbrzych["weather"]
walbrzychWeather=walbrzychwe[0]
walbrzychDesc=walbrzychWeather["description"]
walbrzychName=walbrzych["name"]
walbrzychTemp=walbrzychmain["temp"]
walbrzychTempMin=walbrzychmain["temp_min"]
walbrzychTempMax=walbrzychmain["temp_max"]
walbrzychPressure=walbrzychmain["pressure"]
walbrzychHumidity=walbrzychmain["humidity"]
walbrzychWindSp=walbrzychwind["speed"]
walbrzychWindDir=walbrzychwind["deg"]
walbrzychClouds=walbrzychclouds["all"]
valwalbrzych=[walbrzychName,walbrzychTemp,walbrzychTempMin,walbrzychTempMax,walbrzychPressure,walbrzychHumidity,walbrzychWindSp,walbrzychWindDir,walbrzychClouds,walbrzychDesc]
walbrzychLat=walbrzychcoord["lat"]
walbrzychLon=walbrzychcoord["lon"]
print "Walbrzych ... OK"
jelenia=weather[3]
jeleniacoord=jelenia["coord"]
jeleniamain=jelenia["main"]
jeleniawind=jelenia["wind"]
jeleniaclouds=jelenia["clouds"]
jeleniawe=jelenia["weather"]
jeleniaWeather=jeleniawe[0]
jeleniaDesc=jeleniaWeather["description"]
jeleniaName=jelenia["name"]
jeleniaTemp=jeleniamain["temp"]
jeleniaTempMin=jeleniamain["temp_min"]
jeleniaTempMax=jeleniamain["temp_max"]
jeleniaPressure=jeleniamain["pressure"]
jeleniaHumidity=jeleniamain["humidity"]
jeleniaWindSp=jeleniawind["speed"]
jeleniaWindDir=jeleniawind["deg"]
jeleniaClouds=jeleniaclouds["all"]
valjelenia=[jeleniaName,jeleniaTemp,jeleniaTempMin,jeleniaTempMax,jeleniaPressure,jeleniaHumidity,jeleniaWindSp,jeleniaWindDir,jeleniaClouds,jeleniaDesc]
jeleniaLat=jeleniacoord["lat"]
jeleniaLon=jeleniacoord["lon"]
print "Jelenia Gora ... OK"

milicz=weather[4]
miliczcoord=milicz["coord"]
miliczmain=milicz["main"]
miliczwind=milicz["wind"]
miliczclouds=milicz["clouds"]
miliczwe=milicz["weather"]
miliczWeather=miliczwe[0]
miliczDesc=miliczWeather["description"]
miliczName=milicz["name"]
miliczTemp=miliczmain["temp"]
miliczTempMin=miliczmain["temp_min"]
miliczTempMax=miliczmain["temp_max"]
miliczPressure=miliczmain["pressure"]
miliczHumidity=miliczmain["humidity"]
miliczWindSp=miliczwind["speed"]
miliczWindDir=miliczwind["deg"]
miliczClouds=miliczclouds["all"]
valmilicz=[miliczName,miliczTemp,miliczTempMin,miliczTempMax,miliczPressure,miliczHumidity,miliczWindSp,miliczWindDir,miliczClouds,miliczDesc]
miliczLat=miliczcoord["lat"]
miliczLon=miliczcoord["lon"]
print "Milicz ... OK"
klodzko=weather[5]
klodzkocoord=klodzko["coord"]
klodzkomain=klodzko["main"]
klodzkowind=klodzko["wind"]
klodzkoclouds=klodzko["clouds"]
klodzkowe=klodzko["weather"]
klodzkoWeather=klodzkowe[0]
klodzkoDesc=klodzkoWeather["description"]
klodzkoName=klodzko["name"]
klodzkoTemp=klodzkomain["temp"]
klodzkoTempMin=klodzkomain["temp_min"]
klodzkoTempMax=klodzkomain["temp_max"]
klodzkoPressure=klodzkomain["pressure"]
klodzkoHumidity=klodzkomain["humidity"]
klodzkoWindSp=klodzkowind["speed"]
klodzkoWindDir=klodzkowind["deg"]
klodzkoClouds=klodzkoclouds["all"]
valklodzko=[klodzkoName,klodzkoTemp,klodzkoTempMin,klodzkoTempMax,klodzkoPressure,klodzkoHumidity,klodzkoWindSp,klodzkoWindDir,klodzkoClouds,klodzkoDesc]
klodzkoLat=klodzkocoord["lat"]
klodzkoLon=klodzkocoord["lon"]
print "Klodzko ... OK"
bogatynia=weather[6]
bogatyniacoord=bogatynia["coord"]
bogatyniamain=bogatynia["main"]
bogatyniawind=bogatynia["wind"]
bogatyniaclouds=bogatynia["clouds"]
bogatyniawe=bogatynia["weather"]
bogatyniaWeather=bogatyniawe[0]
bogatyniaDesc=bogatyniaWeather["description"]
bogatyniaName=bogatynia["name"]
bogatyniaTemp=bogatyniamain["temp"]
bogatyniaTempMin=bogatyniamain["temp_min"]
bogatyniaTempMax=bogatyniamain["temp_max"]
bogatyniaPressure=bogatyniamain["pressure"]
bogatyniaHumidity=bogatyniamain["humidity"]
bogatyniaWindSp=bogatyniawind["speed"]
bogatyniaWindDir=bogatyniawind["deg"]
bogatyniaClouds=bogatyniaclouds["all"]
valbogatynia=[bogatyniaName,bogatyniaTemp,bogatyniaTempMin,bogatyniaTempMax,bogatyniaPressure,bogatyniaHumidity,bogatyniaWindSp,bogatyniaWindDir,bogatyniaClouds,bogatyniaDesc]
bogatyniaLat=bogatyniacoord["lat"]
bogatyniaLon=bogatyniacoord["lon"]
print "Bogatynia ... OK"
glogow=weather[7]
glogowcoord=glogow["coord"]
glogowmain=glogow["main"]
glogowwind=glogow["wind"]
glogowclouds=glogow["clouds"]
glogowwe=glogow["weather"]
glogowWeather=glogowwe[0]
glogowDesc=glogowWeather["description"]
glogowName=glogow["name"]
glogowTemp=glogowmain["temp"]
glogowTempMin=glogowmain["temp_min"]
glogowTempMax=glogowmain["temp_max"]
glogowPressure=glogowmain["pressure"]
glogowHumidity=glogowmain["humidity"]
glogowWindSp=glogowwind["speed"]
glogowWindDir=glogowwind["deg"]
glogowClouds=glogowclouds["all"]
valglogow=[glogowName,glogowTemp,glogowTempMin,glogowTempMax,glogowPressure,glogowHumidity,glogowWindSp,glogowWindDir,glogowClouds,glogowDesc]
glogowLat=glogowcoord["lat"]
glogowLon=glogowcoord["lon"]
print "Glogow ... OK"
boleslawiec=weather[8]
boleslawieccoord=boleslawiec["coord"]
boleslawiecmain=boleslawiec["main"]
boleslawiecwind=boleslawiec["wind"]
boleslawiecclouds=boleslawiec["clouds"]
boleslawiecwe=boleslawiec["weather"]
boleslawiecWeather=boleslawiecwe[0]
boleslawiecDesc=boleslawiecWeather["description"]
boleslawiecName=boleslawiec["name"]
boleslawiecTemp=boleslawiecmain["temp"]
boleslawiecTempMin=boleslawiecmain["temp_min"]
boleslawiecTempMax=boleslawiecmain["temp_max"]
boleslawiecPressure=boleslawiecmain["pressure"]
boleslawiecHumidity=boleslawiecmain["humidity"]
boleslawiecWindSp=boleslawiecwind["speed"]
boleslawiecWindDir=boleslawiecwind["deg"]
boleslawiecClouds=boleslawiecclouds["all"]
valboleslawiec=[boleslawiecName,boleslawiecTemp,boleslawiecTempMin,boleslawiecTempMax,boleslawiecPressure,boleslawiecHumidity,boleslawiecWindSp,boleslawiecWindDir,boleslawiecClouds,boleslawiecDesc]
boleslawiecLat=boleslawieccoord["lat"]
boleslawiecLon=boleslawieccoord["lon"]
print "Boleslawiec ... OK"
strzelin=weather[9]
strzelincoord=strzelin["coord"]
strzelinmain=strzelin["main"]
strzelinwind=strzelin["wind"]
strzelinclouds=strzelin["clouds"]
strzelinwe=strzelin["weather"]
strzelinWeather=strzelinwe[0]
strzelinDesc=strzelinWeather["description"]
strzelinName=strzelin["name"]
strzelinTemp=strzelinmain["temp"]
strzelinTempMin=strzelinmain["temp_min"]
strzelinTempMax=strzelinmain["temp_max"]
strzelinPressure=strzelinmain["pressure"]
strzelinHumidity=strzelinmain["humidity"]
strzelinWindSp=strzelinwind["speed"]
strzelinWindDir=strzelinwind["deg"]
strzelinClouds=strzelinclouds["all"]
valstrzelin=[strzelinName,strzelinTemp,strzelinTempMin,strzelinTempMax,strzelinPressure,strzelinHumidity,strzelinWindSp,strzelinWindDir,strzelinClouds,strzelinDesc]
strzelinLat=strzelincoord["lat"]
strzelinLon=strzelincoord["lon"]
print "Strzelin ... OK"
karpacz=weather[10]
karpaczcoord=karpacz["coord"]
karpaczmain=karpacz["main"]
karpaczwind=karpacz["wind"]
karpaczclouds=karpacz["clouds"]
karpaczwe=karpacz["weather"]
karpaczWeather=karpaczwe[0]
karpaczDesc=karpaczWeather["description"]
karpaczName=karpacz["name"]
karpaczTemp=karpaczmain["temp"]
karpaczTempMin=karpaczmain["temp_min"]
karpaczTempMax=karpaczmain["temp_max"]
karpaczPressure=karpaczmain["pressure"]
karpaczHumidity=karpaczmain["humidity"]
karpaczWindSp=karpaczwind["speed"]
karpaczWindDir=karpaczwind["deg"]
karpaczClouds=karpaczclouds["all"]
valkarpacz=[karpaczName,karpaczTemp,karpaczTempMin,karpaczTempMax,karpaczPressure,karpaczHumidity,karpaczWindSp,karpaczWindDir,karpaczClouds,karpaczDesc]
karpaczLat=karpaczcoord["lat"]
karpaczLon=karpaczcoord["lon"]
print "Karpacz ... OK"

#Utworzenie obiektow z geometria i atrybutami
wroclaw=QgsFeature()
wroclaw.setGeometry(QgsGeometry.fromPoint(QgsPoint(wroclawLon,wroclawLat)))
wroclaw.setAttributes(valWroclaw)
legnica=QgsFeature()
legnica.setGeometry(QgsGeometry.fromPoint(QgsPoint(legnicaLon,legnicaLat)))
legnica.setAttributes(valLegnica)
walbrzych=QgsFeature()
walbrzych.setGeometry(QgsGeometry.fromPoint(QgsPoint(walbrzychLon,walbrzychLat)))
walbrzych.setAttributes(valwalbrzych)
jelenia=QgsFeature()
jelenia.setGeometry(QgsGeometry.fromPoint(QgsPoint(jeleniaLon,jeleniaLat)))
jelenia.setAttributes(valjelenia)
milicz=QgsFeature()
milicz.setGeometry(QgsGeometry.fromPoint(QgsPoint(miliczLon,miliczLat)))
milicz.setAttributes(valmilicz)
klodzko=QgsFeature()
klodzko.setGeometry(QgsGeometry.fromPoint(QgsPoint(klodzkoLon,klodzkoLat)))
klodzko.setAttributes(valklodzko)
bogatynia=QgsFeature()
bogatynia.setGeometry(QgsGeometry.fromPoint(QgsPoint(bogatyniaLon,bogatyniaLat)))
bogatynia.setAttributes(valbogatynia)
glogow=QgsFeature()
glogow.setGeometry(QgsGeometry.fromPoint(QgsPoint(glogowLon,glogowLat)))
glogow.setAttributes(valglogow)
boleslawiec=QgsFeature()
boleslawiec.setGeometry(QgsGeometry.fromPoint(QgsPoint(boleslawiecLon,boleslawiecLat)))
boleslawiec.setAttributes(valboleslawiec)
strzelin=QgsFeature()
strzelin.setGeometry(QgsGeometry.fromPoint(QgsPoint(strzelinLon,strzelinLat)))
strzelin.setAttributes(valstrzelin)
karpacz=QgsFeature()
karpacz.setGeometry(QgsGeometry.fromPoint(QgsPoint(karpaczLon,karpaczLat)))
karpacz.setAttributes(valkarpacz)

#Dodanie obiektow w trybie edycji do warstwy
warstwa.startEditing()
warstwa.addFeature(wroclaw,True)
warstwa.addFeature(legnica,True)
warstwa.addFeature(walbrzych,True)
warstwa.addFeature(jelenia,True)
warstwa.addFeature(milicz,True)
warstwa.addFeature(klodzko,True)
warstwa.addFeature(bogatynia,True)
warstwa.addFeature(glogow,True)
warstwa.addFeature(boleslawiec,True)
warstwa.addFeature(strzelin,True)
warstwa.addFeature(karpacz,True)
warstwa.commitChanges()
print "Zaladowano pomyslnie"