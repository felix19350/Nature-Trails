import os
import logging

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.api import users

from models.Trail import Trail
from models.ActivityLog import ActivityLog

'''
Entry point for the desktop application.
'''

#default open id providers. For each of these a link should be created
openIdProviders = (
    'Google.com/accounts/o8/id', # shorter alternative: "Gmail.com"
    'Yahoo.com',
    'MySpace.com',
    'AOL.com',
    'MyOpenID.com',
    # add more here
)

class TrailsHandler(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__) + '/../../templates/default/', 'trails.html')
        
        #get the last 10 trails and show them
        trails = Trail.all().order('creationDate').fetch(20)
        uploadUrl = blobstore.create_upload_url('/trails/new')
        logging.warning("Upload url: " + self.request.get('link'))
        self.response.out.write(template.render(path, {'trails': trails, 'uploadUrl': uploadUrl, 'dialogId': "newTrailDialog", 'formId': "newTrailForm" }))
        
    '''def createProviderLinks(self):
        links = []
        for p in openIdProviders:
            p_name = p.split('.')[0] # take "AOL" from "AOL.com"
            p_url = p.lower()        # "AOL.com" -> "aol.com"
            links.append({"name": p_name, "url": users.create_login_url(federated_identity=p_url)})
            
        return links'''
