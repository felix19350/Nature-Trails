import os
import sys
import logging

from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.api import users

from models.Trail import Trail
from models.TrailDetails import TrailDetails
from models.ActivityLog import ActivityLog

'''
Gets the trail's details. The response is the object encoded as json, or a 404 if the id does not exist.
'''

class TrailDetailsHandler(webapp.RequestHandler):
    
    def get(self, trailDetailsId = None):
        trailDetails = None
        if(trailDetailsId is None):
            #If no particular trail details Id is given we try to get latest details 
            #for a given trail
            trail = Trail.get(self.request.get('trailId'))
            if(trail is not None):
                q = db.Query(TrailDetails).filter('trail', trail)
                temp = q.fetch(1)

                trailDetails = temp[0] if len(temp) > 0 else  None 
            else:
                self.error(404)
        else:
            #Get the particular trail details object
            trailDetails = TrailDetails.get(trailDetailsId)
        

        #Output the template, for now there is no need to send the data as JSON.    
        path = os.path.join(os.path.dirname(__file__) + '/../../templates/default/', 'trailDetails.html')
        updateUrl = '/trailDetails' if trailDetails is None else '/trailDetails/' + str(trailDetails.key())
        self.response.out.write(template.render(path, {'trailDetails': trailDetails, 'trailId': str(trail.key()), 'updateUrl': updateUrl}))        

                            
    '''
        Handler for the POST method.
        Creates new trail details object for a given trail if no trailDetailsId parameter is given.
    '''
    def post(self, trailDetailsId=None):
        try:
            if(trailDetailsId is None):
                trail = Trail.get(self.request.get('trailId'))
                if(trail is not None):
                    details = TrailDetails(trail=trail,
                                           recommendedSeason=self.request.get('recommendedSeason'),
                                           recommendations=self.request.get('recommendations').strip(),
                                           directions=self.request.get('directions').strip(),
                                           links=self.request.get_all('links'))
                    details.put() 
                    
                    usr = users.get_current_user()
                    if(usr is not None):
                        logEntry = ActivityLog(user=usr, action="Create - Trail details")
                        logEntry.put()  
                        
                    self.response.clear()
                    self.response.set_status(200)                    
                else:
                    self.error(404)
            else:
                self._updateTrailDetails(trailDetailsId)
        except:
            logging.exception("Unexpected error creating trail details: %s", sys.exc_info()[0])
            self.error(500)
            
    '''
        Handler for the PUT method
        Updates an existing trail details object
    ''' 
    def put(self, trailDetailsId):
        self._updateTrailDetails(trailDetailsId)        
    
    
    def delete(self, trailDetailsId):
        try:
            trailDetails = TrailDetails.get(trailDetailsId) 
            if(trailDetails is not None):
                trailDetails.delete()
                
                usr = users.get_current_user()
                if(usr is not None):
                    logEntry = ActivityLog(user=usr, action="Delete - Trail details")
                    logEntry.put()
                
                self.response.clear()
                self.response.set_status(200)
            else:
                self.error(404)
        except:
            logging.exception("Unexpected error deleting trail details: %s", sys.exc_info()[0])
            self.error(500)              
    
    '''
        Method used to update the trail details
    '''             
    def _updateTrailDetails(self, trailDetailsId):
        try:
            trailDetails = TrailDetails.get(trailDetailsId) 
            if(trailDetails is not None):
                trailDetails.recommendedSeason = self.request.get('recommendedSeason')
                trailDetails.recommendations = self.request.get('recommendations').strip()
                trailDetails.directions = self.request.get('directions').strip()
                trailDetails.links = self.request.get_all('links') 
                trailDetails.save() 
              
                usr = users.get_current_user()
                if(usr is not None):
                    logEntry = ActivityLog(user=usr, action="Update - Trail details")
                    logEntry.put()
              
                self.response.clear()
                self.response.set_status(200)
            else:
                self.error(404)  
        except:
            logging.exception("Unexpected error creating trail details: %s", sys.exc_info()[0])
            self.error(500)          
      
        
