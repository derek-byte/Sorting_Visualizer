from app import db

class User(db.Model):
    id = db.Column(db.Integer)
    username = db.Column(db.String(20)) 