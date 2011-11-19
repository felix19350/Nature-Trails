import os
import logging
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.api import users

'''
    Handler for the static pages.
'''

class StaticHandler(webapp.RequestHandler):
    
    pages = ["about", "resources", "regulation", "bestPractices","404", "500"]
    
    def get(self, pageName):
        templatePage = pageName
        if(pageName not in self.pages):
            templatePage = "404"
        
        templatePage = templatePage + ".html"
         
        user = users.get_current_user() 
        requiresLogout = user is not None
            
        path = os.path.join(os.path.dirname(__file__) + '/../../templates/default/contents/', templatePage)
        self.response.out.write(template.render(path, {'requiresLogout': requiresLogout, 'logoutUrl': users.create_logout_url("/")}))            
                
           

        

