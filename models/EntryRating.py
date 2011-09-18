from google.appengine.ext import db
from models.Trail import Trail

class EntryRating(db.Model):
    '''
    Stores the ratings users give to locations
    Parameters:
        entry_key
        user_id
        rating
    '''
    trail = db.ReferenceProperty(Trail)
    user = db.UserProperty(required = True)
    rating = db.RatingProperty(required = True)

    def __str__(self) :
        return "%s: %s - %f" % (self.user.nickname(), self.title, self.rating)
        