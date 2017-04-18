#HELSINKIKUVIA.FI

Notes about application flow:

1. To function properly, IndexView (index.html) needs at least 1 Collection with "show_on_landing_page" flag set to True. Said collection should have at least 1 Record in it.

2. PublicCollectionsView displays A) Collections with is_featured==True and B) Collections with is_public==True

3. Order views need PrintProduct objects (user selects the product they want from a list of PrintProduct objects). 
- Product names are determined in models.py (PRODUCT_LAYOUTS_LIST). These must match those configured in printing provider's API.
- Product dimensions are in millimeters (A4 horizontal 297x210 etc.)
- Paper quality can be anything (redundant, i.e. application is indifferent to its value). 
- Helsinki determines prices per product.

4. Delicate information such as API keys are stored in a separate local_settings file, not committed to this repository.


# Kuvaselaamo app based on https://github.com/City-of-Helsinki/kuvaselaamo 

This is structural change for kuvaselaamo app for easier deployment and cleaner project structure/repository.


## How to:

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