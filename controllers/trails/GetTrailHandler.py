import os
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.api import users

from models.Trail import Trail

'''
Gets the trail's basic info. The response is the object encoded as json, or a 404 if the id does not exist.
'''

class GetTrailHandler(webapp.RequestHandler):
    def get(self): 
        trail = Trail.get(self.request.get('id'))
        if(trail is not None):
            self.response.headers["Content-Type"] = "application/json"
            self.response.out.write(trail.toJson())
        else:
            self.error(404)
        

