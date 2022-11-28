# PhotoHub

Instagram-inspired website created in Django.
PhotoHub allows you to upload, browse, comment, and like photos.
Users can also create their profiles and follow each other.
## Features

**Photos features:**
- Browsing and filtering photos list
- Adding, editing, deleting photos
- Displaying details of photos
- Commenting and liking photos
- Displaying liked photos

**Users features:**
- Browsing and filtering users list
- Following other users
- Registration and login
- Editing profile details
- Resetting password by email
- Changing password when logged in

**Other features:**
- Celery sends daily emails with a summary of followed users' activity

## Demo

The demo version was previously available at Heroku.
Unfortunately, as of November 28, 2022, Heroku's free tier is no longer available.

## Installation
**Requirements:**
You must have python 3.10 and git installed on your machine.

Clone repository:
```bash
$ git clone https://github.com/bartvbx/photohub-django.git
$ cd PhotoHub
```

Set and run virtual environment:
```bash
$ python3 -m venv ./venv
$ . venv/bin/activate
```

Install required dependencies:
```bash
(venv)$ pip install -r requirements.txt
```

Many of the project settings are stored in the environment variables, to run an application you should set at least **PH_DJANGO_SECRET_KEY**.

Now you can start the application:
```bash
(venv)$ python manage.py migrate
(venv)$ python manage.py runserver
```

If you want to start the app with some initial data:
```bash
(venv)$ python manage.py migrate
(venv)$ python manage.py loaddata initial_user
(venv)$ python manage.py shell

	from users.models import Profile
	Profile.objects.all().delete()
	exit()

(venv)$ python manage.py loaddata initial_profile
(venv)$ python manage.py loaddata initial_data
(venv)$ python manage.py runserver
```
## Environment Variables
Values of variables used by database (other than SQLite), email service, Celery, and AWS in settings.py are stored in environment variables.
If you want to use any of these services, appropriate environment variables should be set.

## Tech Stack

Backend:
- Django
- PostgreSQL
- Celery
- Redis

Frontend:
- Bootstrap

Deployed using Heroku and AWS S3.


## License

[MIT](https://choosealicense.com/licenses/mit/)
