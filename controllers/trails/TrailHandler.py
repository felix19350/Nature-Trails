import os
import sys
import logging

from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp import template
from google.appengine.ext import blobstore
from google.appengine.ext import db
from google.appengine.api import users

from models.Trail import Trail
from models.TrailDetails import TrailDetails
from models.ActivityLog import ActivityLog
from utils.KmlParser import KmlParser
from django.utils import simplejson

'''
    REST Like controller for trails

    GET     - Fetches a trail
    POST    - Creates an existing trail
    PUT     - Updates an existing trail
    DELETE  - Deletes an existing trail 
'''
class TrailHandler(blobstore_handlers.BlobstoreUploadHandler):

    '''
        Handler for the GET method. Fetches a single trail.
        @param trailId - The id of the trail to fetch
        @param remote - optional - support for JSONP
        @param callback - optional - support for JSONP
        
        @return the trail as a JSON Object, JSONP is also supported. If the accept header is not "application/json"
        renders the view associated with a trail. 
    '''
    def get(self, trailId): 
        trail = Trail.get(trailId)
        if(trail is not None):
            if(self.request.get("remote") and self.request.get("callback")):
                #If the client provides a "callback" argument, then we assume we have a JSONP call.
                jsonpContent = self.request.get("callback") + "(" + trail.toJson() + ")"
                self.response.headers["Content-Type"] = "text/javascript"
                self.response.out.write(jsonpContent)
            elif(self.request.headers['accept'] in ["application/json", "text/json"]): 
                #If the client requests json them encode the trail as JSON and send it over the wire
                self.response.headers["Content-Type"] = "application/json"
                self.response.out.write(trail.toJson())
            else:
                #otherwise, render the default view
                path = os.path.join(os.path.dirname(__file__) + '/../../templates/default/', 'trail.html')
                uploadUrlStr = '/trail/' + str(trail.key())
                uploadUrl = blobstore.create_upload_url(uploadUrlStr)
                self.response.out.write(template.render(path, {'trail': trail, 'jsonTrail': trail.toJson(), 'logoutUrl': users.create_logout_url("/"), 'uploadUrl': uploadUrl}))
                
        else:
            self.error(404)
     

    '''
        Handler for the POST method. The requests must be encoded with multipart/form-data
        
        A new location is added to the database if the trailId parameter is not set.
        The form is expected to have the following fields:

        @param trailId - optional, if present updates the trail
        @param title
        @param credentialNumber
        @param difficulty
        @param condition
        @param region
        @param nearestCity
        @param tags
        @param file - the KML file
        
        If the following parameters are present, a TrailDetails entry is added:
        @param recommendedSeason - optional
        @param recommendations - optional
        @param directions - optional
        @param links - optional 
    '''
    def post(self, trailId = None):
        
        if(trailId is None):
            try:
                uploadedFiles = self.get_uploads('file')  # 'file' is file upload field in the form
                blobInfo = uploadedFiles[0]
                blobReader = blobInfo.open()
                
                parser = KmlParser()
                trailInfo = parser.parseKml(blobReader)
                
                blobInfo.delete()
                
                #parse tags, if any. It is assumed that they are separated by commas.
                tags = self.request.get('tags').split(',')
                    
                #store entry
                entry = Trail(title = self.request.get('title'),
                                credentialNumber = self.request.get('credentialNumber'),
                                difficulty =self.request.get('difficulty'),
                                condition = self.request.get('condition'),
                                region = self.request.get('region'),
                                nearestCity = self.request.get('nearestCity'),
                                rating = 0,
                                tags = tags,
                                extension = trailInfo['extension'],
                                slope = trailInfo['slope'],                                 
                                startPoint = trailInfo['startPoint'], 
                                points = simplejson.dumps(trailInfo['points']))
                entry.put()
                
                #log action
                usr = users.get_current_user()
                if(usr is not None):
                    logEntry = ActivityLog(user=usr, action="Create - Trail")
                    logEntry.put()
                
                self.redirect('/trails')
            except:
                logging.exception("Unexpected creating trail: %s", sys.exc_info()[0])
                self.error(500)
        
        else:
            self._updateTrail(trailId)

    '''
        Handler for the PUT method. The requests must be encoded with multipart/form-data
        Allows for the update of a trail and associated information.

        @param trailId
        @param title
        @param credentialNumber
        @param difficulty
        @param condition
        @param region
        @param nearestCity
        @param tags
        @param file - the KML file       
    '''
    def put(self, trailId):
        self._updateTrail(trailId)


    '''
        Handler for the DELETE method.
        Deletes a trail and associated data.
        @param trailId
    '''      
    def delete(self, trailId):
        try:
            trail = Trail.get(trailId)
            
            if(trail is not None):
                '''
                    Try to delete the trail, setting the status to 200 if it is successful.
                    Fetches all the trail details matches and deletes them.
                '''
                             
                q = db.Query(TrailDetails).filter('trail', trail)
                
                for trailDetails in q:
                    trailDetails.delete()
                
                trail.delete()
                
                #log action
                usr = users.get_current_user()
                if(usr is not None):
                    logEntry = ActivityLog(user=usr, action="Delete - Trail")
                    logEntry.put()
                  
                self.response.clear()         
                self.response.set_status(200)
            else:
                self.error(404)
                
        except:
            logging.exception("An exception occurred when removing the trail")
            self.error(500)  
            
    
    def _updateTrail(self, trailId):
        try:
            trail = Trail.get(trailId)
            
            if(trail is not None):
                '''
                    Try to update the trail. Returns the updated trail as a JSON object.
                    First the properties that are not related to the file upload are updated.
                '''
                trail.title = self.request.get('title')
                trail.credentialNumber= self.request.get('credentialNumber')
                trail.difficulty= self.request.get('difficulty')
                trail.condition= self.request.get('condition')
                trail.region= self.request.get('region')
                trail.nearestCity= self.request.get('nearestCity')
                trail.tags= self.request.get('tags').split(',')
                
                '''
                    Check if there is a newly uploaded file that superseeds the old data.
                '''
                uploadedFiles = self.get_uploads('file')  # 'file' is file upload field in the form
                if(len(uploadedFiles) > 0):
                    blobInfo = uploadedFiles[0]
                    blobReader = blobInfo.open()
                
                    parser = KmlParser()
                    trailInfo = parser.parseKml(blobReader)
                    
                    trail.extension = trailInfo['extension'] 
                    trail.slope = trailInfo['slope']
                    trail.points = simplejson.dumps(trailInfo['points'])
                    trail.startPoint = trailInfo['startPoint']
                    
                    blobInfo.delete()
                
                #Save the updated trail.
                trail.save()
                
                #log action
                usr = users.get_current_user()
                if(usr is not None):
                    logEntry = ActivityLog(user=usr, action="Update - Trail")
                    logEntry.put()
                           
                self.response.clear()
                self.response.set_status(200)
            else:
                self.error(404)
        
        except:
            logging.exception("An exception occurred when updating the trail")
            self.error(500)             
        

