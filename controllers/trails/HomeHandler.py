import os
import logging
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.api import users

'''
    Handler for the home page. If the user is logged in then he is redirected to the trails
    archive, otherwise he is 
'''

class HomeHandler(webapp.RequestHandler):
    
    #default open id providers. For each of these a link should be created
    openIdProviders = (
        'Google.com/accounts/o8/id', # shorter alternative: "Gmail.com"
        #'Yahoo.com',
        #'MySpace.com',
        #'AOL.com',
        #'MyOpenID.com',
        # add more here
    )
    
    def get(self):
        #user = users.get_current_user()
        path = os.path.join(os.path.dirname(__file__) + '/../../templates/default/', 'home.html')
        self.response.out.write(template.render(path, {"links": self.createProviderLinks()}))            
                
           
    def createProviderLinks(self):
        links = []
        for p in self.openIdProviders:
            p_name = p.split('.')[0] # take "AOL" from "AOL.com"
            p_url = p.lower()        # "AOL.com" -> "aol.com"
            logging.warning("name: " + p_name)
            logging.warning("name: " + p_url)
            links.append({"name": p_name, "url": users.create_login_url(federated_identity = p_url, dest_url="/about")})
            
        return links
        

