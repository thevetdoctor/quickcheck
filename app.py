from flask import Flask, jsonify
import requests
# from flask_crontab import Crontab
app = Flask(__name__)

# crontab = Crontab(app)


# @crontab.job(minute="1")
@app.route("/api", methods=["GET", "POST"])
def api():
    response = requests.get(
        'https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty')
    response_parsed = response.json()
    response_sliced = response_parsed[slice(0, 10)]
    # print(response_sliced)
    response_data = []
    for news in range(len(response_sliced)):
        news_req = requests.get(
            'https://hacker-news.firebaseio.com/v0/item/' + str(response_sliced[news]) + '.json')
        # print(news_req.json())
        response_data.append(news_req.json())
    return jsonify({"api": response_data, "count": len(response_data)})


@app.route("/")
def my_scheduled_job():
    with open("text.txt", "a") as file:
        file.write("Welcome to my job\n")
    return jsonify({"message": "Welcome to my job"})


if __name__ == "__main__":
    app.run(debug=True)
