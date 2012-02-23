import logging

from google.appengine.ext import db
from django.utils import simplejson

class Trail(db.Model):
    '''
    Models a trail in the map
    Parameters:
        - title
        - credentialNumber
        - extension
        - slope
        - difficulty
        - condition
        - region
        - nearestCity
        - rating
        - tags
        - points
        - startPoint
        - creationDate
        Points are stored as a TextProperty, because they cannot be indexed. 
    '''
    
    title = db.StringProperty(required=True)
    credentialNumber = db.StringProperty(required=True)
    extension = db.FloatProperty(required=True)
    slope = db.FloatProperty(required=True)
    difficulty = db.StringProperty(required=True, choices=set(["easy", "moderate", "hard"]))
    condition = db.StringProperty(required=True, choices=set(["excellent", "good", "moderate", "bad", "impossible"]))
    region = db.StringProperty(required=True, choices=set(["north", "center", "south"]))
    nearestCity = db.StringProperty(required=True)
    rating = db.RatingProperty(required=True)
    startPoint = db.GeoPtProperty(required=True)
    tags = db.ListProperty(str)
    points = db.TextProperty()
    creationDate = db.DateTimeProperty(auto_now_add=True)
    
    def __str__(self) :
        return "%s (%s): %s (%s): %f" % (self.title, self.credentialNumber, self.region, self.nearestCity, self.extension)
    
    
    def toMap(self, showPoints = True):
        result = {'key':str(self.key()), 'credentialNumber': self.credentialNumber, 'startPoint': [self.startPoint.lat, self.startPoint.lon],
                  'title': self.title, 'extension': self.extension, 'slope': '%.2f' % self.slope,
                  'extension': '%.2f' % self.extension, 'difficulty': self.difficulty, 'condition': self.condition,
                  'region': self.region, 'nearestCity': self.nearestCity, 'rating': self.rating,
                  'tags': self.tags, 'creationDate': self.creationDate.isoformat()} 
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
            try:
                #Appends the data to the result. Each point is a tuple with the lat, lon and altitude
                result.append([coords[1], coords[0], coords[2]])
            except:
                logging.warning("Could not insert coords:")
                logging.warning(coords) 
        #Hack due to badly un-escaped string        
        if(len(result) > 0):
            result.pop()
            
        return result
  
    
        