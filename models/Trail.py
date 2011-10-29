import logging

from google.appengine.ext import db
from django.utils import simplejson
from google.appengine.api.datastore_types import GeoPt

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
    
    
    def _parsePointText(self):
        result = []
        #the kml standard says that the coordinates are separated by a whitespace
        split = self.points.split(' ')
        
        for tuple in split:
            #Split each tuple
            coords = tuple.split(',')
            try:
                #Appends the data to the result. Each point is a tuple with the lat and lon
                result.append([coords[1],coords[0]])
            except:
                logging.warning("Could not insert coords:")
                logging.warning(coords) 
                
        return result
    
    def toJson(self):
        return simplejson.dumps({'key':str(self.key()), 'credentialNumber': self.credentialNumber, 'startPoint': [self.startPoint.lat, self.startPoint.lon],
                                 'title': self.title, 'extension': self.extension, 'slope': '%.2f' % self.slope,
                                 'extension': '%.2f' % self.extension, 'difficulty': self.difficulty, 'condition': self.condition,
                                 'region': self.region, 'nearestCity': self.nearestCity, 'rating': self.rating,
                                 'tags': self.tags, 'points': self._parsePointText(), 'creationDate': self.creationDate.isoformat()})
    
        