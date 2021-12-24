# quickcheck

A simple flask app built for Hacker News API

https://github.com/thevetdoctor/quickcheck

## Installation

```
Navigate into the root directory
RUN source venv/Scripts/activate (on Windows, use the equivalent command on a Mac)
RUN pip install -r requirements.txt
RUN flask run

```

## API

Available endpoints:

BaseUrl : http://localhost:5000

GET ${rootUrl}apis/:

```
to fetch fresh news from hackernews and sync into database

method: GET
parameters: none
returns: {"message": "fresh news synced", "count": count, "news": news}

```

GET ${rootUrl}get_news/:

```
to fetch all news items

method: GET
parameters: none
returns: {"message": "news retrieved", "count": count, "news": news}

```

GET ${rootUrl}get_news/?type&text:

```
to fetch all news items based on type or text

method: GET
parameters(query): type and/or text
returns: {"message": "news retrieved", "count": count, "news": news}

```

POST ${rootUrl}/api/news

```
method: POST
parameters: title, valid text, url and author
returns: {"message": "fresh news added", "count": count, "news": news}

```

PUT ${rootUrl}/api/news/ID

```
to update a news item (not sourced from hackernews)

method: PUT
parameters: text, news item ID
returns: {"message": "Item with ID: updated", "news": news}

```

DELETE ${rootUrl}/api/news/ID

```
to delete a news item (not sourced from hackernews)

method: DELETE
parameters: news item ID
returns: {"message": "Item with ID: deleted"}

```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
