[![GitHub last commit](https://img.shields.io/github/last-commit/aatrubilin/my_receipts.svg)](https://github.com/aatrubilin/my_receipts/commits/master)
[![CI](https://img.shields.io/github/workflow/status/aatrubilin/my_receipts/CI)](https://github.com/aatrubilin/my_receipts/actions/workflows/ci.yml)
[![Test coverage](coverage.svg)](coverage.svg)

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/pydanny/cookiecutter-django/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License](https://img.shields.io/github/license/aatrubilin/my_receipts.svg)](LICENSE)


# My Receipts

[WIP] Web app for collecting information about purchases.

# Settings

Moved to [settings](config/settings)

Default environment settings in [cookiecutter-django docs](http://cookiecutter-django.readthedocs.io/en/latest/settings.html)

# Basic Commands

## Setting Up Your Users

* To create a **normal user account**, just go to Sign Up and fill out the form.
  Once you submit it, you'll see a "Verify Your E-mail Address" page.
  Go to your console to see a simulated email verification message.
  Copy the link into your browser. Now the user's email should be verified and ready to go.
* To create an **superuser account**, use this command:
  ```bash
  python manage.py createsuperuser
  ```

_For convenience, you can keep your normal user logged in on Chrome and your superuser logged in
on Firefox (or similar), so that you can see how the site behaves for both kinds of users._

## Type checks

Running type checks with mypy:

```bash
mypy my_receipts
```

## Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

```bash
coverage run -m pytest
coverage html
open htmlcov/index.html
```

### To generate coverage badge run:

```bash
coverage-badge -o coverage.svg -f
```

### Running tests with pytest

```bash
pytest
```

## Celery

This app comes with Celery.

To run celery worker from Run/Debug Pycharm Configuration start `Celery`

Or run a celery worker from terminal:

```bash
cd my_receipts
celery -A config.celery_app worker -l info
```

Please note: For Celery's import magic to work, it is important *where* the celery commands are run.
If you are in the same folder with *manage.py*, you should be right.

## Email Server

In development, it is often nice to be able to see emails that are being sent from your application.
For that reason local SMTP server [MailHog](https://github.com/mailhog/MailHog) with a web interface is available as docker container.

Container mailhog will start automatically when you will run all docker containers.
Please check `cookiecutter-django Docker documentation` for more details how to start all containers.

With MailHog running, to view messages that are sent by your application,
open your browser and go to ``http://127.0.0.1:8025``

You also can start `MailHog` Run/Debug Pycharm Configuration.

## Sentry

Sentry is an error logging aggregator service. You can sign up for a free account at
https://sentry.io/signup/?code=cookiecutter or download and host it yourself.
The system is setup with reasonable defaults, including 404 logging
and integration with the WSGI application.

**You must set the DSN url in production.**

## Deployment

The following details how to deploy this application.

### Docker

See detailed [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html)

## Authors

* **Alexandr Trubilin** - *Initial work* - [AATrubilin](https://github.com/aatrubilin)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
