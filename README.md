# flask_curses_example
Example of Flask app with Flask_SQLAlchemy for Python courses.

# Overall
This is example of web application is created to show small practical example of Flask microframework.

First commits used raw SQL queries to maintain backend needs. Last commits uses ORM system (Flask-Alchemy or i.e SQLAlchemy) for same purpose.
Currently dev_react branch is more advanced - for home page view it uses React JS library. Also, added csrf tokens and DB migrations support.

# How to use migrations
- run virtualenv and cd to root directory
- execute:
    - for Linux: $ export FLASK_APP=flask_example.py
    - for Windows: SET FLASK_APP=flack_example.py
- make changes to /scraper_app/models.py
- execute: flask db migrate -m "Comment to this migration"
- check new file created in /migrations/versions/%revision%_%migration_comment%.py
- if all looks o'key execute: flask db upgrade

Now you successfully made a migration.

Soon I'll add notice about React JS.
