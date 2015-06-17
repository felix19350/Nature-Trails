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
        
        namespaces = ["http://www.opengis.net/kml/2.2"]
        for ns in namespaces: 
            query = '{%(ns)s}Document/{%(ns)s}Folder/{%(ns)s}Placemark/{%(ns)s}Point/{%(ns)s}coordinates' % {'ns': ns}
            
            coordinates = xml.findall(query)
            if coordinates is not None :
                logging.warning(len(coordinates))
                numberCrunching = self.analizeKml(coordinates)
                result['startPoint']= numberCrunching['startPoint']
                result['extension'] = numberCrunching['extension']
                result['slope'] = numberCrunching['slope']
                result['points'] = numberCrunching['filteredPoints']
                break
            else:
                logging.warning("No points for %s", ns) 
              
        return result
    
    '''
        In KML the coordinates are stored as triplets of latitude, longitude and altitude
    '''
    def analizeKml(self, coordinates):
        #the kml standard says that the coordinates are separated by a whitespace
        #Just in case we transform any linebreaks we find into spaces (some devices
        #generate KMLs with \n separating each point)
        #nodeText = nodeText.replace('\n', ' ')
        #split = nodeText.split(' ')
        #logging.warning("Num points: ")
        
        startPoint = None
        lastPoint = None
        lastPointToCalc = None
        slope = 0.0
        extension = 0.0
        pointSet = ""
        numFiltered = 0
        
        for coord in coordinates:
            #Split each tuple
            coords = coord.text.split(',')
            logging.warning(coords)
            try:
                #create a GeoPt and do calculations
                currentPoint = GeoPt(float(coords[1]), float(coords[0])) 
                filter = 0.0
                
                if(lastPointToCalc is not None):
                    #Calculate the total distance, and accumulated slope
                    d = self.calculateDistance(currentPoint, lastPointToCalc)
                    extension += d
                else:
                    #Set the start point
                    startPoint = currentPoint

                lastPointToCalc = currentPoint
                #logging.warning("distance %.8f", d)
                
                curHeight = float(coords[2])
                slope += curHeight - slope
                
                #Filter out points that are near each other in order to reduce the database size
                if(lastPoint is not None):
                    filter = self.calculateDistance(currentPoint, lastPoint)
                 
                if(filter > self.THRESHOLD or lastPoint is None):
                    pointSet += " %s,%s" % (coords[0],coords[1])
                    lastPoint = currentPoint
                    numFiltered = numFiltered + 1
            except:
                logging.error("Unexpected error: %s", sys.exc_info()[0])
        
        logging.warning("Num filtered points: %d", numFiltered)
          
        return {'slope': slope, 'extension': extension, 'filteredPoints': pointSet, 'startPoint': startPoint}
    
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
                    
    

