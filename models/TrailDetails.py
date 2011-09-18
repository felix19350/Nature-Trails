import logging

from models.Trail import Trail
from google.appengine.ext import db
from django.utils import simplejson

class TrailDetails(db.Model):
    '''
    Models the additional information attached to a trail
    Parameters:
        - directions: Text field where the user can fill out some directions to reach the trail
        - recommendations: Text field that has recommendations for the users
        - recommendedSeason: Recommended season for that trail
        - links: A list of useful links related to that particular trail
    '''
    
    
    trail = db.ReferenceProperty(Trail)
    recommendedSeason = db.StringProperty(required=True, choices=set(["Any", "Winter", "Autumn", "Summer", "Spring"]))
    directions = db.TextProperty()
    recommendations = db.TextProperty()
    links = db.ListProperty(db.Link)
    creationDate = db.DateTimeProperty(auto_now_add=True)
      
    def toJson(self):
        return simplejson.dumps({'key':str(self.key()), 'trail': str(self.trail.key()),
                                 'recommendedSeason': self.recommendedSeason, 'directions': self.directions,
                                 'recommendations': self.recommendations, 'links': self.links})
    
        