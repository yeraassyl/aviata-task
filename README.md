# Cheap Tickets Calendar
Cheap tickets and ticket validation API. Currently using api.skypicker.com/flights
### Getting Started
```pip install -r requirements.txt```</br>

``` python manage.py migrate ```

Also, you need to set up Redis and Celery on your local machine to run the app.  </br>

See the [settings](https://github.com/yeraassyl/cheapest-tickets-calendar/blob/master/flights/settings.py) file
### Usage
To start the celery beat worker you need to run
``` $ celery -A proj worker -B -l INFO ``` </br>


Or you can create systemd or supervisor service to keep Celery running in background

See [docs](https://docs.celeryproject.org/en/stable/userguide/daemonizing.html)

Calendar view shows cheapest tickets for the upcoming month, for the top 10 directions

You can use any directions you want, just change the settings variable. 

Remember to keep them in list of tuples as shown below:

```
TOP_10_DIRECTIONS = [
    ('ALA', 'TSE'),
    ('TSE', 'ALA'),
    ('ALA', 'MOW'),
    ('MOW', 'ALA'),
    ('ALA', 'CIT'),
    ('CIT', 'ALA'),
    ('TSE', 'MOW'),
    ('MOW', 'TSE'),
    ('TSE', 'LED'),
    ('LED', 'TSE')
]
```

Also, you can validate each ticket, in case this ticket is not available, cache for the cheapest ticket will be updated
