from . import db


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, unique=True, nullable=False)
    title = db.Column(db.String, nullable=True)
    type = db.Column(db.String(20), nullable=False)
    text = db.Column(db.String, nullable=True)
    time = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String(250), nullable=True)
    by = db.Column(db.String(50), nullable=True)
    source = db.Column(db.String(50), nullable=False)

    # kids = db.relationship('Comments', backref='news', lazy='joined')

    def __init__(self, item_id, title, type, text, time, url, by, source):
        self.item_id = item_id
        self.title = title
        self.type = type
        self.text = text
        self.time = time
        self.url = url
        self.by = by
        self.source = source


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, unique=True, nullable=False)
    title = db.Column(db.String, nullable=True)
    type = db.Column(db.String(20), nullable=False)
    text = db.Column(db.String, nullable=True)
    time = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String(250), nullable=True)
    by = db.Column(db.String(50), nullable=True)
    source = db.Column(db.String(50), nullable=False)

    parent = db.Column(db.Integer, db.ForeignKey(
        'news.item_id'), nullable=False)
    parents = db.relationship('News', lazy='joined', innerjoin=True)

    parentz = db.Column(db.Integer, db.ForeignKey(
        'comments.item_id'), nullable=True)
    kids = db.relationship(
        'Comments', remote_side=[item_id])

    def __init__(self, item_id, title, type, text, time, url, by, source, parent, parentz):
        self.item_id = item_id
        self.title = title
        self.type = type
        self.text = text
        self.time = time
        self.url = url
        self.by = by
        self.source = source
        self.parent = parent
        self.parentz = parentz
