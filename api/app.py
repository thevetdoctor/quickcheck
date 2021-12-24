from flask import Flask, jsonify, request, current_app
from flask_cors import CORS
from flask_migrate import Migrate
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
import requests
import json
import os
import random
from dotenv import load_dotenv
from .models import News, Comments
from . import db
import datetime

load_dotenv()

app = Flask(__name__, static_folder='../ui/build', static_url_path='/')

# setup database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DB_URI')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"pool_pre_ping": True}
app.secret_key = os.environ.get('SECRET_URL')

CORS(app)
db.init_app(app)
migrate = Migrate(app, db)

executors = {
    'default': ThreadPoolExecutor(16),
    'processpool': ProcessPoolExecutor(4)
}
sched = BackgroundScheduler(timezone='Asia/Seoul', executors=executors)


@app.route("/get_news", methods=["GET"])
def get_news():
    print('Calling /get_news')

    query_params_type = request.args.get("type")
    query_params_text = request.args.get("text")
    if(query_params_type or query_params_text):
        if(query_params_type and query_params_text):
            res = db.session.query(News).filter(
                News.type == query_params_type, News.text.like(f"%{query_params_text}%"))
            res1 = db.session.query(Comments).all()
        else:
            if(query_params_type):
                print("type: ", query_params_type, "text: ", query_params_text)
                res = db.session.query(News).filter(
                    News.type == query_params_type)
                res1 = db.session.query(Comments).all()
            elif(query_params_text):
                res = db.session.query(News).filter(
                    News.text.like(f"%{query_params_text}%"))
                res1 = db.session.query(Comments).all()
    else:
        res = db.session.query(News).all()
    res1 = db.session.query(Comments).all()

    news = [
        {
            "id": new.item_id,
            "title": new.title,
            "type": new.type,
            "text": new.text,
            "time": new.time,
            "url": new.url,
            "by": new.by,
            "source": new.source
        } for new in res
    ]
    news1 = [
        {
            "id": new.item_id,
            "title": new.title,
            "type": new.type,
            "text": new.text,
            "time": new.time,
            "url": new.url,
            "by": new.by,
            "source": new.source
        } for new in res1
    ]
    news = news + news1
    return jsonify({"message": "news retrieved", "count": len(news), "news": news})


def seed_db():
    print('Seeding')
    curr_dt = datetime.datetime.now()
    dt = int(round(curr_dt.timestamp()))
    random_int = random.randint(1000000, 10000000)
    p = News(123, "title", "story", "text",
             dt, "url", "by", 'public')
    q = Comments(123, "title", "comment", "text",
                 dt, "url", "by", 'public', int(123), int(123))
    db.session.add(p)
    db.session.add(q)
    db.session.commit()
    return


@ app.route("/apis", methods=["GET"])
def apis():
    print('Calling /apis')
    seed = db.session.query(Comments).filter_by(parentz=123).all()
    if(len(seed) < 1):
        seed_db()

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
    print(response_trimmed)
    for news in range(len(response_trimmed)):
        news_data = requests.get(
            'https://hacker-news.firebaseio.com/v0/item/' + str(response_trimmed[news]) + '.json')
        news_req = news_data.json()

        if news_req is not None:
            create_news = News(news_req.get("id"), news_req.get("title"), news_req.get("type"), news_req.get("text"),
                               news_req.get("time"), news_req.get("url"), news_req.get("by"), 'hackernews')

            if news_req.get("descendants"):
                print('Descendants', news_req.get("descendants"))
            if news_req.get("kids"):
                print(news_req.get("kids"), len(news_req.get('kids')))
                for kid in range(len(news_req.get('kids'))):
                    kid_data = requests.get(
                        'https://hacker-news.firebaseio.com/v0/item/' + str(news_req.get('kids')[kid]) + '.json')
                    kid_req = kid_data.json()
                    print('kid req', kid_req.get('type'))
                    # create_comment =
                    create_comment = Comments(kid_req.get("id"), kid_req.get("title"), kid_req.get("type"), kid_req.get("text"),
                                              kid_req.get("time"), kid_req.get("url"), kid_req.get("by"), 'hackernews', news_req.get("id"), int(123))

                    # create_news.kids.append(create_comment)

                    if kid_req is not None and kid_req.get("kids"):
                        print(kid_req.get("comment kids"),
                              len(kid_req.get('kids')))
                        for kid in range(len(kid_req.get('kids'))):
                            comment_kid_data = requests.get(
                                'https://hacker-news.firebaseio.com/v0/item/' + str(kid_req.get('kids')[kid]) + '.json')
                            comment_kid_req = comment_kid_data.json()
                            print('comment kid req',
                                  comment_kid_req.get('type'))

                            create_kid_comment = Comments(comment_kid_req.get("id"), comment_kid_req.get("title"), comment_kid_req.get("type"), comment_kid_req.get(
                                "text"), comment_kid_req.get("time"), comment_kid_req.get("url"), comment_kid_req.get("by"), 'hackernews', int(123),  kid_req.get("id"))

                            db.session.add(create_kid_comment)
                    db.session.add(create_comment)
            db.session.add(create_news)
            db.session.commit()

        result.append(news_req)
    return jsonify({"message": "fresh news synced", "count": len(result), "news": result})


@ app.route("/api/news", methods=["POST"])
def add_news():
    seed = db.session.query(Comments).filter_by(parentz=123).all()
    if(len(seed) < 1):
        seed_db()

    print('Creating a fresh News article')
    req = request.json
    curr_dt = datetime.datetime.now()
    dt = int(round(curr_dt.timestamp()))
    random_int = random.randint(1000000, 10000000)
    if(req is not None and req.get("type") == 'comment'):
        if(req.get("parent") is not None):
            data = Comments(random_int, req.get("title"), req.get("type"), req.get("text"),
                            dt, req.get("url"), req.get("by"), 'public', req.get("parent"), int(123))
            db.session.add(data)
            db.session.commit()

            val = Comments.query.filter_by(item_id=random_int).all()
            print(val)
            news = [
                {
                    "id": new.item_id,
                    "title": new.title,
                    "type": new.type,
                    "text": new.text,
                    "time": new.time,
                    "url": new.url,
                    "by": new.by,
                    "source": new.source
                } for new in val
            ]
            return jsonify({"message": "fresh news added", "count": len(news), "comment": news[0]})
        else:
            return jsonify({"message": "parent value is required"})
    else:
        data = News(random_int, req.get("title"), req.get("type"), req.get("text"),
                    dt, req.get("url"), req.get("by"), 'public')
        db.session.add(data)
        db.session.commit()

        val = News.query.filter_by(item_id=random_int).all()
        print(val)
        news = [
            {
                "id": new.item_id,
                "title": new.title,
                "type": new.type,
                "text": new.text,
                "time": new.time,
                "url": new.url,
                "by": new.by,
                "source": new.source
            } for new in val
        ]
        return jsonify({"message": "fresh news added", "count": len(news), "news": news[0]})


@ app.route("/api/news/<id>", methods=["PUT", "DELETE"])
def update_news(id):
    req = request.json
    data = News.query.filter_by(item_id=id).all()
    print('Updating/Deleting a News article', data)
    if(len(data) < 1):
        return jsonify({"message": "Item with ID not found"})
    if(request.method == 'PUT'):
        print('Updating a News article', data, req)

        if(req.get("text")):
            data[0].text = req.get("text")
        if(req.get("url")):
            data[0].url = req.get("url")
        if(req.get("by")):
            data[0].by = req.get("by")
        db.session.commit()

        val = db.session.query(News).filter_by(item_id=id).all()
        news = [
            {
                "id": new.item_id,
                "title": new.title,
                "type": new.type,
                "text": new.text,
                "time": new.time,
                "url": new.url,
                "by": new.by
            } for new in val
        ]
        return jsonify({"message": "Item with ID: updated", "news": news})
    else:
        print('Deleting a News article', data)
        db.session.delete(data[0])
        db.session.commit()
        return jsonify({"message": "Item with ID: deleted"})


sched.add_job(apis, 'interval', seconds=300)


@ app.route("/clear")
def clear_db():
    d = db.drop_all()
    e = db.create_all()
    return jsonify({"message": "Table cleared"})


@ app.route("/")
def index():

    return app.send_static_file('index.html')


# def job():
#     app = create_app()
with app.app_context():
    # app.app_context().push()
    # current_app.config["ENV"]
    try:
        sched.start()
        print('pass')
    except:
        print('pass check')
    # pass
    print('check')
# return app


# job()

if __name__ == "__main__":
    db.create_all()
    print('app start')
    app.run()
