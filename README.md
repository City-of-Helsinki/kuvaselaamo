#HELSINKIKUVIA.FI

Setup:
------------
- Create python 2.7 virtual envinronment and activate it

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

(next paragraph borrowed from linkedevents https://raw.githubusercontent.com/City-of-Helsinki/linkedevents/master/README.md )

Requirements:
------------

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

Notes about application flow:
------------

1. To function properly, IndexView (index.html) needs at least 1 Collection with "show_on_landing_page" flag set to True. Said collection should have at least 1 Record in it.

2. PublicCollectionsView displays A) Collections with is_featured==True and B) Collections with is_public==True

3. Order views need PrintProduct objects (user selects the product they want from a list of PrintProduct objects). 
- Product names are determined in models.py (PRODUCT_LAYOUTS_LIST). These must match those configured in printing provider's API.
- Product dimensions are in millimeters (A4 horizontal 297x210 etc.)
- Paper quality can be anything (redundant, i.e. application is indifferent to its value). 
- Helsinki determines prices per product.

4. Delicate information such as API keys are stored in a separate local_settings file, not committed to this repository.


