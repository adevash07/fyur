from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    genres = db.Column(db.String())
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    looking_for_talent = db.Column(db.Boolean)
    description = db.Column(db.String(500))
    venue_shows = db.relationship('Show', back_populates='venue', lazy='dynamic')
   
 
    def __repr__(self):
        return f'<Venue {self.id} {self.name}>'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120), nullable=True)
    looking_for_venue = db.Column(db.Boolean, default=False)
    description = db.Column(db.String(120), nullable=True)
    artist_shows = db.relationship('Show', back_populates='artist', lazy=True)
    
    def __repr__(self):
        return f'<Artist {self.id} {self.name}>'
    
    @property
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'genres': self.genres.split(','),
            'image_link': self.image_link,
            'facebook_link': self.facebook_link,
            'website_link': self.website_link,
            'looking_for_venue': self.looking_for_venue,
            'description': self.description,
        }
    @property
    def to_dict_with_shows(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'genres': self.genres.split(','),
            'image_link': self.image_link,
            'facebook_link': self.facebook_link,
            'website_link': self.website_link,
            'looking_for_venue': self.looking_for_venue,
            'description': self.description,
            'upcoming_shows': [show.to_dict for show in self.shows.filter(Show.start_time > datetime.now())],
            'upcoming_shows_count': len(self.shows.filter(Show.start_time > datetime.now())),
            'past_shows': [show.to_dict for show in self.shows.filter(Show.start_time < datetime.now())],
            'past_shows_count': len(self.shows.filter(Show.start_time < datetime.now())),
        }
        
    def __repr__(self):
        return f'<Artist {self.id} {self.name}>'
        

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
    __tablename__ = 'Show'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    start_time = db.Column(db.DateTime, nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    venue = db.relationship('Venue', back_populates='venue_shows')
    artist = db.relationship('Artist', back_populates='artist_shows')
    
    def __repr__(self):
        return f'<Show {self.id} {self.name}>'
