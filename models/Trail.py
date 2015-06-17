import logging
#import json
from google.appengine.ext import ndb
from django.utils import simplejson

class Trail(ndb.Model):
    '''
    Models a trail in the map
    Parameters:
        - title
        - extension
        - slope
        - nearestCity
        - points
        - startPoint
        - creationDate
        - timeDurationHours
        - militaryMap
        Points are stored as a TextProperty, because they cannot be indexed. 
    '''
    
    title = ndb.StringProperty(required=True)
    extension = ndb.FloatProperty(required=True)
    slope = ndb.FloatProperty(required=True)
    timeDurationHours = ndb.StringProperty(required=True)
    nearestCity = ndb.StringProperty(required=True)
    startPoint = ndb.GeoPtProperty(required=True)
    militaryMap = ndb.StringProperty(required=True)
    points = ndb.TextProperty()
    creationDate = ndb.DateTimeProperty(auto_now_add=True)
    
    def __str__(self) :
        return "%s, %s - %f" % (self.title, self.nearestCity, self.extension)
    
    
    def toMap(self, showPoints = True):
        result = {'key':self.key.id(), 'militaryMap': self.militaryMap, 'startPoint': [self.startPoint.lat, self.startPoint.lon],
                  'title': self.title, 'slope': '%.2f' % self.slope,
                  'extension': '%.2f' % self.extension, 'nearestCity': self.nearestCity, 'timeDurationHours': self.timeDurationHours,
                  'creationDate': self.creationDate.isoformat()} 

        if(showPoints):
            result["points"] = self._parsePointText()
            
        return result

    def toJson(self, showPoints = True):
        return simplejson.dumps(self.toMap(showPoints))
    
    def _parsePointText(self):
        result = []
        #the kml standard says that the coordinates are separated by a whitespace
        split = self.points.split(' ')
        t = None
        
        for t in split:
            #Split each tuple
            coords = t.split(',')
            logging.warning(coords)
            try:
                #Appends the data to the result. Each point is a tuple with the lat, lon and altitude
                result.append([coords[1], coords[0]])
            except:
                logging.warning("Could not insert coords:")
                logging.warning(coords) 
        #Hack due to badly un-escaped string        
        if(len(result) > 0):
            result.pop()
            
        return result
  
    
        