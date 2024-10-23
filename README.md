## Setup

I recommend you create some virtual environment with a python version >= 3.11, e.g.
```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```




You might need to init migrations

```bash
flask db init
flask db migrate -m"Migration initiale"
```

Now apply the migration to the database
```bash
flask db upgrade
```

To run the server
```bash
flask run
```
to access Swagger-ui  visit http://127.0.0.1:5000/apidocs/


Run the test suite with

```bash
python -m pytest -v
```


Mootez HICHRI