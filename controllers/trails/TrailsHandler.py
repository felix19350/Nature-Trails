import os
import logging

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.api import users
from models.Trail import Trail

'''
Entry point for the desktop application.
'''

class TrailsHandler(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__) + '/../../templates/default/', 'trails.html')
        
        #get the last 10 trails and show them
        trails = Trail.all().order('creationDate').fetch(20)
        uploadUrl = blobstore.create_upload_url('/trails/new')
        logging.warning("Upload url: " + self.request.get('link'))
        self.response.out.write(template.render(path, {'trails': trails, 'uploadUrl': uploadUrl, 'logoutUrl': users.create_logout_url("/"), 'dialogId': "newTrailDialog", 'formId': "newTrailForm" }))
        

