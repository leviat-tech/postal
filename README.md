# postal-experiment

to start server (requires python ^3.8 and [poetry](https://python-poetry.org/)):

```
export FLASK_APP=postal_experiment/hello.py
poetry run flask run
```

in another terminal window:

`curl -X POST http://127.0.0.1:5000/hello`
