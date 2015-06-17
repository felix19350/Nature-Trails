import os
import logging
from controllers.trails.BaseHandler import BaseHandler

'''
    Handler for the static pages.
'''

class StaticHandler(BaseHandler):
    
    pages = ["about", "resources", "bestPractices","404", "500"]

    def get(self, pageName):
        templatePage = pageName
        if(pageName not in self.pages):
            templatePage = "404"
        templatePage = templatePage + ".html"
        #user = users.get_current_user() 
        #requiresLogout = user is not None
        path = os.path.join('default/contents/', templatePage)
        context = {}
        self.render_template(path, **context)

