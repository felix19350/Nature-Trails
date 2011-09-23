import os
import logging
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.api import users

class SearchHandler(webapp.RequestHandler):
    '''
         Handles the searches. Returns the search results as a list of json objects.
    '''
    
    def get(self):
        #TODO: Check options for fulltext search.
        
        