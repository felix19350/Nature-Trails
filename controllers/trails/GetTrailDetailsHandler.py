import os
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.api.datastore_types import Key

from models.TrailDetails import TrailDetails

'''
Gets the trail's details. The response is the object encoded as json, or a 404 if the id does not exist.
'''

class GetTrailDetailsHandler(webapp.RequestHandler):
    def get(self):
        q = db.GqlQuery("SELECT * FROM TrailDetails " +
                "WHERE trail = :1", Key(self.request.get('id')))
        trailDetails = q.fetch(1)[0]
        if(trailDetails is not None):
            self.response.headers["Content-Type"] = "application/json"
            self.response.out.write(trailDetails.toJson())
        else:
            self.error(404)