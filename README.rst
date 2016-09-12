Coellection for Django 1.9
==========================
A front end web-app for google docs spreadsheet
This project demo lives at `cody-rocker.ddns.net <https://cody-rocker.ddns.net/coellection>`_

:Developer:
    `Cody Rocker <mailto:cody.rocker.83@gmail.com>`_.

- *Requirements*
    + Django 1.9.3
    + xlrd 0.9.4

This repo can be cloned directly into a running Django environment as a standalone application. If you don't have a running Django environment setting up a development/testing environment is easy.
`Read the Docs <https://docs.djangoproject.com/en/1.9/topics/install/>`_

Clone source and install dependencies
-------------------------------------

Move into the top level of your django environment and run the following.

.. code-block:: bash
    
    # Clone repo
    $ git clone https://github.com/cody-rocker/coellection

    # Resulting structure should be:
    #   /mysite
    #     /mysite
    #     /coellection

    # Change into app directory and install dependencies
    $ cd coellection
    $ pip install -r requirements.txt

Getting started
---------------

Install app in mysite/settings.py

.. code-block:: python
    
    INSTALLED_APPS = [
        # This entry must be added
        'coellection',
        # Default django apps
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    ]

Configure mysite/urls.py

.. code-block:: python

    urlpatterns = [
        url(r'^admin/', admin.site.urls),
        # Add the following url redirect
        url(r'^coellection/', include('coellection.urls')),
    ]

Make migrations and migrate database to create required tables.

.. code-block:: bash
    
    # From top level of your django environment
    $ python manage.py makemigrations coellection
    $ python manage.py migrate

    # Collect static files if running on production server
    $ python manage.py collectstatic

Populate the coellection tables from google doc spreadsheet.

.. code-block:: bash

    # From top level of your django environment
    $ python manage.py refresh_coellection

If this is on a live server (Apache, Nginx, Gunicorn, etc.) you should restart the service at this point.

Test Results
------------

At this point you should be able to interact with the app in your browser at http://example.com/coellection if it's on a production server or http://127.0.0.1:8000/coellection if running on a default dev environment.
