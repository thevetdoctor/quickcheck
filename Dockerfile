FROM python:3.9
WORKDIR /app

COPY ./api/ ./requirements.txt ./
RUN pip install -r ./requirements.txt
RUN pip install gunicorn
ENV FLASK_ENV development 
ENV DB_URI postgresql://fsnxmjiu:VfgQQZJ6EOeVGxEsXVo6AemcQZ6wnmnO@castor.db.elephantsql.com/fsnxmjiu
ENV SECRET_KEY obasecret

EXPOSE 5000
CMD ["gunicorn", "-b", ":5000", "app:app"]