# Grey Neurons Website Monitor

## Development

### Optional Dependencies

While these are optional, it makes life better.

All the steps can be done manually.

If you do not wish to install `just`, look at the `justfile` to figure out what
each of the receipe does, and execute that command manually from the terminal.


* `just` command runner
  * See [installation](https://github.com/casey/just?tab=readme-ov-file#installation) documentation
* `docker` for running dockerized postgres
  * `justfile` has support for starting/stoping dockerized postgres.
  * run `just -l` (in the folder where `justfile` exists) to see all recepies

### Steps

* Create and activate virtual environment. On Linux you can do this by running
following commands
  * `python -m venv /path/to/new/virtual/environment`
  * `source venv/bin/activate`
* install dependencies using `pip install requirements-dev.lock`

* (Optional) Start local postgres (`just start-pgsql`)
* Start development server using `just start-devserver`
* Go to `http://127.0.0.1:8000/docs` to test the APIs


## Run tests

All tests **must** pass before commit

* `just test`


## Run linter and formatter

Please run this before **every** commit

* `just lint`
