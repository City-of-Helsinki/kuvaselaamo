[![Build & Staging & Accept](https://github.com/City-of-Helsinki/kuvaselaamo/actions/workflows/staging.yml/badge.svg)](https://github.com/City-of-Helsinki/kuvaselaamo/actions/workflows/staging.yml)

# Kuvaselaamo / Helsinkikuvia.fi

## Summary

Kuvaselaamo is an application for browsing the image archive of Finna service (https://finna.fi). The application also
provides functionalities for arranging images into collections which can be created either by staff members or by
users who have created an account for themselves. The images may be ordered as physical prints by the users for a fee.

The current implementation is Helsinkikuvia.fi service which is maintained by Helsinki City Museum.

## Development with [Docker](https://docs.docker.com/)

Prerequisites:
* Docker engine: 18.06.0+
* Docker compose 1.22.0+

1. Create a `docker-compose.env.yaml` file in the project folder:
   * Use `docker-compose.env.yaml.example` as a base, it does not need any changes for getting the project running.
   * Set entrypoint/startup variables according to taste.
     * `DEBUG`, controls debug mode on/off 
     * `APPLY_MIGRATIONS`, applies migrations on startup
     * `CREATE_ADMIN_USER`, creates an admin user with credentials `kuva-admin`:(password, see below)
     (kuva-admin@hel.ninja)
     * `ADMIN_USER_PASSWORD`, the admin user's password. If this is not given, a random password is generated
     and written into stdout when an admin user is created automatically.
     * `ADD_INITIAL_CONTENT`, bootstrap data import for divisions
     * `HKM_PBW_*`, Visma Pay-related configuration. Used when the user is forwarded to Visma Pay for print payments.
     * `HKM_PRINTMOTOR_*`, Printmotor-related configuration. Used when ordering prints.

2. Run `docker-compose up`
    * The project is now running at [localhost:8080](http://localhost:8080)

## Development without Docker

This chapter contains the application's old documentation. Docker usage is preferred.

### Setup:

- Create python 3.9 virtual envinronment and activate it

```
virtualenv venv
source venv/bin/activate
```

- clone (this) repository
- Install requirements from requirements.txt (see repository)

```
pip install -r requirements.txt
```

- Check your django application settings and setup database, secret key, allowed hosts etc.
- execute `python manage.py migrate`
- create superuser with manage.py

```
python manage.py createsuperuser
```

- execute `python manage.py collectstatic`

- run kuvaselaamo (uwsgi, django's runserver or any other)

### Requirements:

(this paragraph borrowed from linkedevents https://raw.githubusercontent.com/City-of-Helsinki/linkedevents/master/README.md )

Linked Events uses two files for requirements. The workflow is as follows.

`requirements.txt` is not edited manually, but is generated
with `pip-compile`.

`requirements.txt` always contains fully tested, pinned versions
of the requirements. `requirements.in` contains the primary, unpinned
requirements of the project without their dependencies.

In production, deployments should always use `requirements.txt`
and the versions pinned therein. In development, new virtualenvs
and development environments should also be initialised using
`requirements.txt`. `pip-sync` will synchronize the active
virtualenv to match exactly the packages in `requirements.txt`.

In development and testing, to update to the latest versions
of requirements, use the command `pip-compile`. You can
use [requires.io](https://requires.io) to monitor the
pinned versions for updates.

To remove a dependency, remove it from `requirements.in`,
run `pip-compile` and then `pip-sync`. If everything works
as expected, commit the changes.

### Notes about application flow:

1. To function properly, IndexView (index.html) needs at least 1 Collection with "show_on_landing_page" flag set to True. Said collection should have at least 1 Record in it.

2. PublicCollectionsView displays A) Collections with is_featured==True and B) Collections with is_public==True

3. Delicate information such as API keys are stored in a separate local_settings file, not committed to this repository.

## Issue tracking

* [Github issue list](https://github.com/City-of-Helsinki/kuvaselaamo/issues)
* [Jira issues](https://helsinkisolutionoffice.atlassian.net/projects/HEL/issues/?filter=allissues)


## API documentation

* N/A currently


## Environments
Test: https://helsinkikuvia.test.kuva.hel.ninja/

Production: https://helsinkikuvia.fi

## CI/CD builds

Project is using [GitHub Actions](https://github.com/City-of-Helsinki/kuvaselaamo/actions)
for automated builds and deployment into the test environment.
The test environment is built automatically from the `develop` branch.


## Code format

This project uses
[`black`](https://github.com/ambv/black),
[`flake8`](https://gitlab.com/pycqa/flake8) and
[`isort`](https://github.com/timothycrosley/isort)
for code formatting and quality checking. Project follows the basic
black config, without any modifications.

Basic `black` commands:

* To let `black` do its magic: `black .`
* To see which files `black` would change: `black --check .`

[`pre-commit`](https://pre-commit.com/) can be used to install and
run all the formatting tools as git hooks automatically before a
commit.
