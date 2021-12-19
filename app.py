from flask import Flask, jsonify, request, current_app
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='./build', static_url_path='/')

# setup databse configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DB_URI')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"pool_pre_ping": True}
app.secret_key = os.environ.get('SECRET_URL')

CORS(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, unique=True, nullable=False)
    title = db.Column(db.String, nullable=True)
    type = db.Column(db.String(20), nullable=False)
    text = db.Column(db.String, nullable=True)
    time = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String(250), nullable=True)
    by = db.Column(db.String(50), nullable=True)

    # kids = db.relationship('Comments', backref='news', lazy=True)
    # comment_id = db.Column(db.Integer, db.ForeignKey(
    #     'comments.id'), default=1)
    # comment = db.relationship(
    #     'Comments', backref=db.backref('news', lazy=True))

    def __init__(self, item_id, title, type, text, time, url, by):
        self.item_id = item_id
        self.title = title
        self.type = type
        self.text = text
        self.time = time
        self.url = url
        self.by = by


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, unique=True, nullable=False)
    title = db.Column(db.String, nullable=True)
    type = db.Column(db.String(20), nullable=False)
    text = db.Column(db.String, nullable=True)
    time = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String(250), nullable=True)
    by = db.Column(db.String(50), nullable=True)

    parent = db.Column(db.Integer, db.ForeignKey(
        'news.item_id'), nullable=False)
    news = db.relationship('News', backref=db.backref('comments', lazy=True))

    # parentz = db.Column(db.Integer, db.ForeignKey(
    #     'comments.item_id'), nullable=False)
    # comments = db.relationship(
    #     # 'Comments', backref=db.backref('comments', lazy=True))
    #     'Comments', remote_side=[item_id])

    def __init__(self, item_id, title, type, text, time, url, by):
        self.item_id = item_id
        self.title = title
        self.type = type
        self.text = text
        self.time = time
        self.url = url
        self.by = by


@app.route("/get_news", methods=["GET"])
def get_news():
    query_params_type = request.args.get("type")
    query_params_text = request.args.get("text")
    if(query_params_type):
        res = db.session.query(News).filter(News.type == query_params_type)
    elif(query_params_text):
        res = db.session.query(News).filter(
            News.text.like(f"%{query_params_text}%"))
    else:
        res = db.session.query(Comments).all()
    news = [
        {
            "id": new.item_id,
            "title": new.title,
            "type": new.type,
            "text": new.text,
            "time": new.time,
            "url": new.url,
            "by": new.by
        } for new in res
    ]
    return jsonify({"message": "cached news retrieved", "count": len(news), "news": news})


executors = {
    'default': ThreadPoolExecutor(16),
    'processpool': ProcessPoolExecutor(4)
}
sched = BackgroundScheduler(timezone='Asia/Seoul', executors=executors)


@ app.route("/apis", methods=["GET", "POST"])
def apis():
    print('Calling /apis')
    response = requests.get(
        'https://hacker-news.firebaseio.com/v0/newstories.json?print=pretty')
    response_parsed = response.json()
    response_sliced = response_parsed[slice(0, 50)]

    req = db.session.query(News.item_id)
    res = req.all()
    res_parsed = []
    for s in res:
        for t in s:
            res_parsed.append(t)
    response_trimmed = []
    for r in response_sliced:
        try:
            if(res_parsed.index(r) >= 0):
                u = res_parsed.index(r)
        except:
            response_trimmed.append(r)

    result = []
    for news in range(len(response_trimmed)):
        news_data = requests.get(
            'https://hacker-news.firebaseio.com/v0/item/' + str(response_trimmed[news]) + '.json')
        news_req = news_data.json()

        create_news = News(news_req.get("id"), news_req.get("title"), news_req.get("type"), news_req.get("text"),
                           news_req.get("time"), news_req.get("url"), news_req.get("by"))

        if news_req is not None and news_req.get("descendants"):
            print('Descendants', news_req.get("descendants"))
        if news_req is not None and news_req.get("kids"):
            print(news_req.get("kids"), len(news_req.get('kids')))
            for kid in range(len(news_req.get('kids'))):
                kid_data = requests.get(
                    'https://hacker-news.firebaseio.com/v0/item/' + str(news_req.get('kids')[kid]) + '.json')
                kid_req = kid_data.json()
                print('kid req', kid_req.get('type'))
                create_comment = Comments(kid_req.get("id"), kid_req.get("title"), kid_req.get("type"), kid_req.get("text"),
                                          kid_req.get("time"), kid_req.get("url"), kid_req.get("by"))
                create_news.comments.append(create_comment)
                news_req['kids'].append(kid_req)
                db.session.add(create_news)
        db.session.commit()

        result.append(news_req)
    return jsonify(result)


@ app.route("/api", methods=["GET", "POST"])
def api():
    print('Calling /api')
    response = requests.get(
        'https://hacker-news.firebaseio.com/v0/newstories.json?print=pretty')
    response_parsed = response.json()
    response_sliced = response_parsed[slice(0, 3)]
    req = db.session.query(News.item_id)
    res = req.all()
    res_parsed = []
    for s in res:
        for t in s:
            res_parsed.append(t)
    response_trimmed = []
    for r in response_sliced:
        try:
            if(res_parsed.index(r) >= 0):
                u = res_parsed.index(r)
        except:
            response_trimmed.append(r)

    response_data = []
    for news in range(len(response_trimmed)):
        news_data = requests.get(
            'https://hacker-news.firebaseio.com/v0/item/' + str(response_trimmed[news]) + '.json')
        news_req = news_data.json()
        data = News(news_req.get("id"), news_req.get("title"), news_req.get("type"), news_req.get("text"),
                    news_req.get("time"), news_req.get("url"), news_req.get("by"))
        db.session.add(data)
        db.session.commit()

        response_data.append(news_req)
    return jsonify({"message": "fresh news retrieved", "count": len(response_data), "news": response_data})


sched.add_job(api, 'interval', seconds=300)


@app.route("/clear")
def clear_db():
    d = db.drop_all()
    e = db.create_all()
    return jsonify({"message": "Table cleared"})


@ app.route("/")
def index():
    return app.send_static_file('index.html')

    # with app.app_context():
    # current_app.config["ENV"]
    # sched.start()


if __name__ == "__main__":
    db.create_all()
    app.run()
