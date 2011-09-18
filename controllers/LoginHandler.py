from google.appengine.api import users
from google.appengine.ext import webapp
'''
    Provides basic support for open id.
'''
openIdProviders = (
    'Google.com/accounts/o8/id', # shorter alternative: "Gmail.com"
    'Yahoo.com',
    'MySpace.com',
    'AOL.com',
    'MyOpenID.com',
    # add more here
)


class LoginHandler(webapp.RequestHandler):
        def get(self):
            user = users.get_current_user()
            if user:  # signed in already
                self.response.out.write('Hello <em>%s</em>! [<a href="%s">sign out</a>]' % (
                    user.nickname(), users.create_logout_url(self.request.uri)))
            else:     # let user choose authenticator
                self.response.out.write('Hello world! Sign in at: ')
                for p in openIdProviders:
                    p_name = p.split('.')[0] # take "AOL" from "AOL.com"
                    p_url = p.lower()        # "AOL.com" -> "aol.com"
                    self.response.out.write('[<a href="%s">%s</a>]' % (
                        users.create_login_url(federated_identity=p_url), p_name))
