FROM python:3.9
WORKDIR /app

COPY ./app.py ./requirements.txt ./
RUN pip install -r ./requirements.txt
RUN pip install gunicorn
ENV FLASK_ENV development

EXPOSE 5000
CMD ["gunicorn", "-b", ":5000", "app:app"]