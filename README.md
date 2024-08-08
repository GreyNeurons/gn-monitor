# Grey Neurons Website Monitor

## Development

* Create and activate virtual environment. On Linux you can do this by running following commands
  * `python -m venv /path/to/new/virtual/environment`
  * `source venv/bin/activate`
* install dependencies using `pip install requirements-dev.lock`
* **All command line operations are done from `src` folder**
* Start development server using `fastapi dev main.py`
* Go to `http://127.0.0.1:8000/docs` to test the APIs


## Run tests

All tests **must** pass before commit

* (from `src` folder) `pytest`


## Run linter and formatter

Please run this before **every** commit

* (from `src` folder) `ruff check --fix`
