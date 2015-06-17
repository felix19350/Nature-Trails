import os
import sys
import logging
import webapp2

from webapp2_extras import jinja2
from controllers.trails.BaseHandler import BaseHandler
from google.appengine.ext import blobstore
from google.appengine.api import users
from models.Trail import Trail
from django.utils import simplejson

'''
Entry point for the desktop application.

'''

class TrailsHandler(BaseHandler):

    defaultNum = 20

    def get(self):
        #Get the latest N trails
        numTrails = self.request.get("n") if self.request.get("n") else self.defaultNum
        trails = Trail.query().order(Trail.creationDate)
        
        if(self.request.get("remote") and self.request.get("callback")):
            #JSONP request. Render the content as json and wrap it in a function call
            trails = map(self._jsonEncoder, trails)
            jsonpContent = self.request.get("callback") + "(" + simplejson.dumps(trails) + ")"
            self.response.headers["Content-Type"] = "text/javascript"
            self.response.out.write(jsonpContent)    		
        elif(self.request.headers['accept'] in ["application/json", "text/json"]):
            #Ajax request. Dump the list as json
            trails = map(self._jsonEncoder, trails)
            self.response.headers["Content-Type"] = "application/json"
            self.response.out.write(trails)
        else:
            #render the default view
            path = os.path.join('default/', 'trails.html')
            uploadUrl = blobstore.create_upload_url('/trail')
            logging.warning("Upload url: " + self.request.get('link'))
            context = {'trails': trails, 'uploadUrl': uploadUrl, 'logoutUrl': users.create_logout_url("/"), 'dialogId': "newTrailDialog", 'formId': "newTrailForm" }
            self.render_template(path, **context)

    def _jsonEncoder(self, trail):
        return trail.toMap(False)


