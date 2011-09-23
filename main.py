
import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from controllers.LoginHandler import LoginHandler
from controllers.trails.HomeHandler import HomeHandler
from controllers.trails.TrailsHandler import TrailsHandler
from controllers.trails.NewTrailHandler import NewTrailHandler
from controllers.trails.GetTrailHandler import GetTrailHandler
from controllers.trails.GetTrailDetailsHandler import GetTrailDetailsHandler

application = webapp.WSGIApplication([('/', HomeHandler),
                                      ('/trails', TrailsHandler),
                                      ('/trails/new', NewTrailHandler),
                                      ('/trails/show', GetTrailHandler),
                                      ('/trails/fetchDetails', GetTrailDetailsHandler),
                                      ('/_ah/login_required', LoginHandler)],
                                      debug=True)

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()