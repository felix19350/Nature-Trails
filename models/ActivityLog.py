from google.appengine.ext import db
from django.utils import simplejson

class ActivityLog(db.Model):
    '''
    Simple activity log that stores actions performed by the user.
    '''
    user = db.UserProperty(required=True)
    date = db.DateTimeProperty(auto_now_add=True)
    action = db.StringProperty(required=True)
    
        
    def __str__(self) :
        return "%s (%s) - %s \n" % (self.user.nickname(), self.date, self.action)
        
    def toJson(self):
        #return """{"key": "%s", "category": "%s", "description": "%s", "title": "%s", "lat": %f, "lon": %f, "links": %s, "date": "%s"}""" % (self.key(), self.category, self.title, self.description, self.point.lat, self.point.lon, self.printLinks(), self.date)
        return simplejson.dumps({'userId': self.user.user_id(), 'username': self.user.nickname(), 'date': self.date, 'action': self.action})
    
        