from app import db


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String, nullable=False)
    type = db.Column(db.String(20), nullable=False)
    time = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String(250), nullable=False)
    by = db.Column(db.String(30), nullable=False)

    def __init__(self, item_id, title, type, time, url, by):
        self.item_id = item_id
        self.title = title
        self.type = type
        self.time = time
        self.url = url
        self.by = by
