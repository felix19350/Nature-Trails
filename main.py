
import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from controllers.IndexHandler import IndexHandler
from controllers.DefaultIndexHandler import DefaultIndexHandler
from controllers.MobileIndexHandler import MobileIndexHandler
from controllers.NewLocationHandler import NewLocationHandler
from controllers.UpdateLocationHandler import UpdateLocationHandler
from controllers.FetchLocationHandler import FetchLocationHandler
from controllers.ListLocationsHandler import ListLocationsHandler
from controllers.LoginHandler import LoginHandler
from controllers.trails.TrailsHandler import TrailsHandler
from controllers.trails.NewTrailHandler import NewTrailHandler
from controllers.trails.GetTrailHandler import GetTrailHandler
from controllers.trails.GetTrailDetailsHandler import GetTrailDetailsHandler

application = webapp.WSGIApplication([('/', IndexHandler),
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