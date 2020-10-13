# cloud
[self-hosted] a flask-powered webapp that lets you save and download your files anytime.

## setup
- install [python dependencies](https://github.com/xolanigumbi/cloud/blob/master/requirements.txt "requirements.txt")

-  initialize database files using flask-migrate
```bash
$ flask db init
$ flask db migrate
$ flask db upgrade
```
## run
- start flask app
```bash
$ flask run
```
## todo
- create your personal account
- upload and download files