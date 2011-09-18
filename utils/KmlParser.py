import logging
import math
import sys

from xml.etree.ElementTree import ElementTree
from google.appengine.api.datastore_types import GeoPt

class KmlParser:
    '''
        Implements a Kml parser.
    '''
    THRESHOLD = 0.000
    
    '''
        Parses a string containing KML and returns the text for those coordinates.
    '''
    def parseKml(self, kmlFile):
        result = {'points': None, 'extension': 0.0, 'slope': 0.0}
        xml = ElementTree()      
        xml = xml.parse(kmlFile)
        
        ns = "http://www.opengis.net/kml/2.2"
        query = '{%(ns)s}Document/{%(ns)s}Placemark/{%(ns)s}LineString/{%(ns)s}coordinates' % {'ns': ns}
        
        coordinates = xml.find(query)
        if coordinates is not None :
            nodeText = coordinates.text
            numberCrunching = self.analizeKml(nodeText)
            result['extension'] = numberCrunching['extension']
            result['slope'] = numberCrunching['slope']
            result['points'] = numberCrunching['filteredPoints']
            
        return result
    
    '''
        In KML the coordinates are stored as triplets of latitude, longitude and altitude
    '''
    def analizeKml(self, nodeText):
        #the kml standard says that the coordinates are separated by a whitespace
        split = nodeText.split(' ')
        logging.warning("Num points: ")
        logging.warning(len(split))
        
        lastPoint = None
        lastPointToCalc = None
        slope = 0.0
        extension = 0.0
        pointSet = ""
        numFiltered = 0
        
        for tuple in split:
            #Split each tuple
            coords = tuple.split(',')
            try:
                #create a GeoPt and do calculations
                currentPoint = GeoPt(float(coords[1]), float(coords[0])) 
                filter = 0.0
                
                #Calculate the total distance, and accumulated slope
                if(lastPointToCalc is not None):
                    d = self.calculateDistance(currentPoint, lastPointToCalc)
                    extension += d

                lastPointToCalc = currentPoint
                logging.warning("distance %.8f", d)
                
                curHeight = float(coords[2])
                slope += curHeight - slope
                
                #Filter out points that are near each other in order to reduce the database size
                if(lastPoint is not None):
                    filter = self.calculateDistance(currentPoint, lastPoint)
                 
                if(filter > self.THRESHOLD):
                    pointSet += " %s" % tuple
                    lastPoint = currentPoint
                    numFiltered = numFiltered + 1
                    
                if(lastPoint is None):
                    lastPoint = currentPoint
                    
            except:
                logging.error("Unexpected error: %s", sys.exc_info()[0])
        
        logging.warning("Num filtered points: %d", numFiltered)
          
        return {'slope': slope, 'extension': extension, 'filteredPoints': pointSet}
    
    '''
    Calculate the distance between two points (in kms) using the haversine method
    '''
    def calculateDistance(self, pointA, pointB):
                 
        earthRadius = 6371 #km
        dLat = self.toRad(pointB.lat - pointA.lat)
        dLon = self.toRad(pointB.lon - pointA.lon)
        lat1 = self.toRad(pointA.lat)
        lat2 = self.toRad(pointB.lat)
        
        a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.sin(dLon / 2) * math.sin(dLon / 2) * math.cos(lat1) * math.cos(lat2); 
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)); 
        return earthRadius * c;
 
    '''
    Converts degrees to radians
    '''   
    def toRad(self, deg):
        return (deg * math.pi) / 180
                    
    

