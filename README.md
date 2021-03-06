# jasmin-api
Jasmin restful management API

##Documentation

* Installation and cofiguration of the API below
* General Jasmin documentation [http://docs.jasminsms.com/en/latest/index.html](http://docs.jasminsms.com/en/latest/index.html)
* Jasmin management CLI, which is wrapped by the rest API [http://docs.jasminsms.com/en/latest/management/jcli/modules.html](http://docs.jasminsms.com/en/latest/management/jcli/modules.html)
* Swagger documentation will be on the path /docs/ If you run locally with default settings this will be [http://localhost:8000/docs/](http://localhost:8000/docs/)


##Settings

Requires local_settings.py in jasmin_api/jasmin_api
(same directory as settings.py) which should contain:

    DEBUG = False
    SECRET_KEY = '[some random string]'

set DEBUG = True for testing

By default a SQLite database will be used for storing authentication data. You can use a different database by adding a [DATABASES setting](https://docs.djangoproject.com/en/1.8/ref/settings/#databases) to local_settings.py

You can hide the Swagger documentation, which is shown by default, by adding:

    SHOW_SWAGGER = False

You can also override the default settings for the telnet connection in local_settings.py. These settings with their defaults are:

    TELNET_HOST = '127.0.0.1'
    TELNET_PORT = 8990
    TELNET_USERNAME = 'jcliadmin'
    TELNET_PW = 'jclipwd'

##Installing

We recommend installing in a virtualenv

1. Install dependencies:

    $ pip install -r requirements.txt

2. cd to jasmin_api and run:

    $ ./manage.py migrate
    $ ./manage.py createsuperuser
    $ ./manage.py collectstatic

The last is only needed if you are running the production server (see below)
rather than the Django dev server. It should be run again on any upgrade that changes static files. If in doubt, run it.

##Running

To run for testing and development:
    cd jasmin_api;./manage.py runserver

This is slower, requires DEBUG=True,  and is **much less secure**

To run on production:

    cd jasmin_api;run_cherrypy.py

This requires that you run the collectstatic command (see above) and you should
have DEBUG=False

## Dependencies and requirements
* Python 2.7 required, use of virtualenv recommended
* A command line telnet client should be installed - this is a usual with Unix type OSes
* See requirements.txt for packages installable from pypi
* Optional: libyaml would improve performance of Django REST Swagger
