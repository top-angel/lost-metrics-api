# Lost Metrics API



## Getting started

## Helpful commands

Run dev server

`python manage.py runserver`

Use particular settings based on the environment `local`, `dev`,  `production`.
For example to run server with dev settings

`python manage.py runserver --settings LostMetrics.settings.dev`

Make migrations 

`python manage.py makemigrations`

Run migrations 

`python manage.py migrate`

restart gunicorn

`sudo systemctl restart gunicorn`

export data

`./manage.py dumpdata > db.json`