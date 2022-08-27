from app import db

class SortingEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    past_array = db.Column(db.String(10000))
    steps_array = db.Column(db.String(10000))