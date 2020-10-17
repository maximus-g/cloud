# Cloud
[self-hosted] a flask-powered webapp that lets you save and download your files anytime.

## Setup
- install [python dependencies](https://github.com/xolanigumbi/cloud/blob/master/requirements.txt "requirements.txt")

-  initialize database files using flask-migrate
```bash
$ flask db init
$ flask db migrate
$ flask db upgrade
```
## Run
- start flask app
```bash
$ flask run
```
## Todo
- create your personal account
- upload and download files

## WARNING
This stores files in the database (sqlite in this case), which is a bad practice.
If you attempt to upload large files (audio and videos), the server will return 413 status code.
