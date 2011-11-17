
import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from controllers.LoginHandler import LoginHandler
from controllers.trails.HomeHandler import HomeHandler
from controllers.trails.TrailsHandler import TrailsHandler
from controllers.trails.StaticHandler import StaticHandler
from controllers.trails.TrailHandler import TrailHandler
from controllers.trails.TrailDetailsHandler import TrailDetailsHandler

application = webapp.WSGIApplication([('/', HomeHandler),
                                      ('/trails', TrailsHandler),
                                      ('/trail', TrailHandler),
                                      ('/trail/(.*)', TrailHandler),
                                      ('/trailDetails', TrailDetailsHandler),
                                      ('/trailDetails/(.*)', TrailDetailsHandler),
                                      ('/_ah/login_required', LoginHandler),
                                      ('/(.*)', StaticHandler)],
                                      debug=True)

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()