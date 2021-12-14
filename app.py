from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import requests

app = Flask(__name__)

# from flask_crontab import Crontab
# crontab = Crontab(app)

# setup databse configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://fsnxmjiu:VfgQQZJ6EOeVGxEsXVo6AemcQZ6wnmnO@castor.db.elephantsql.com/fsnxmjiu"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'obasecret'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# @crontab.job(minute="1")


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, unique=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    type = db.Column(db.String(20), nullable=False)
    time = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String(250), nullable=True)
    kids = db.Column(db.String)
    by = db.Column(db.String(30), nullable=False)

    def __init__(self, item_id, title, type, time, url, kids, by):
        self.item_id = item_id
        self.title = title
        self.type = type
        self.time = time
        self.url = url
        self.kids = kids
        self.by = by


@app.route("/get_news", methods=["GET"])
def get_news():
    res = News.query.all()
    news = [
        {
            "id": new.id,
            "title": new.title,
            "type": new.type,
            "time": new.time,
            "url": new.url,
            "kids": new.kids,
            "by": new.by
        } for new in res
    ]
    return jsonify({"message": "news retrieved", "count": len(news), "news": news})


@app.route("/api", methods=["GET", "POST"])
def api():
    response = requests.get(
        'https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty')
    response_parsed = response.json()
    response_sliced = response_parsed[slice(0, 100)]
    # print(response_sliced)
    req = db.session.query(News.item_id)
    res = req.all()
    res_parsed = []
    for s in res:
        for t in s:
            res_parsed.append(t)
    response_trimmed = []
    # print(res_parsed)
    for r in response_sliced:
        try:
            if(res_parsed.index(r) >= 0):
                u = res_parsed.index(r)
                # print(f"Index of {r} is {u}")
        except:
            # print(f"{r} is not present")
            response_trimmed.append(r)

    response_data = []
    for news in range(len(response_trimmed)):
        news_data = requests.get(
            'https://hacker-news.firebaseio.com/v0/item/' + str(response_trimmed[news]) + '.json')
        news_req = news_data.json()
        # print(news_req)
        data = News(news_req.get("id"), news_req.get("title"), news_req.get("type"),
                    news_req.get("time"), news_req.get("url"), news_req.get("kids"), news_req.get("by"))
        db.session.add(data)
        db.session.commit()

        response_data.append(news_req)
    return jsonify({"count": len(response_data), "api": response_data})


@app.route("/")
def my_scheduled_job():
    with open("text.txt", "a") as file:
        file.write("Welcome to my job\n")
    return jsonify({"message": "Welcome to my job"})


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
