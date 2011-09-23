import logging
import sys

from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import users

from models.Trail import Trail
from models.TrailDetails import TrailDetails
from models.ActivityLog import ActivityLog
from utils.KmlParser import KmlParser
from django.utils import simplejson

class NewTrailHandler(blobstore_handlers.BlobstoreUploadHandler):
    '''
        Only allows for post method to add a location to the database.
        The form is expected to have the following fields:
        title, credentialNumber, difficulty, condition, region, nearestCity, tags.
        
        If the following parameters are present, a TrailDetails entry is added:
        recommendedSeason, recommendations, directions, links 
    '''
    def post(self):
        logging.warning("Arg: " + self.request.get('link'))
        
        upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
        blobInfo = upload_files[0]
        blobReader = blobInfo.open()
        
        parser = KmlParser()
        trailInfo = parser.parseKml(blobReader)
        
        blobInfo.delete()
        
        #parse tags, if any. It is assumed that they are separated by commas.
        tags = self.request.get('tags').split(',')
            
        #store entry
        entry = Trail(title = self.request.get('title'),
                        credentialNumber = self.request.get('credentialNumber'),
                        extension = trailInfo['extension'], #generated when the file is parsed
                        slope = trailInfo['slope'], #generated when the file is parsed
                        difficulty = self.request.get('difficulty'),
                        condition = self.request.get('condition'),
                        region = self.request.get('region'),
                        nearestCity = self.request.get('nearestCity'),
                        rating = 0,
                        tags = tags,
                        points = simplejson.dumps(trailInfo['points']))
        entry.put()
        
        #if there is any optional add it to the database as well
        try:
            details = TrailDetails(trail = entry,
                                   recommendedSeason = self.request.get('recommendedSeason'),
                                   recommendations = self.request.get('recommendations'),
                                   directions = self.request.get('directions'),
                                   links = self.request.get_all('links'))
            details.put()
        except:
            logging.error("Unexpected error: %s", sys.exc_info()[0])
        
        #log action
        usr = users.get_current_user()
        if(usr is not None):
            logEntry = ActivityLog(user=usr, action="CREATE - Trail")
            logEntry.put()
        
        self.redirect('/trails')
        
        '''if entry:
            
            #logging.warning("Sending response as json...")
            #self.response.headers["Content-Type"] = "application/json"
            #self.response.out.write(entry.toJson())
        else:
            self.error(500)'''