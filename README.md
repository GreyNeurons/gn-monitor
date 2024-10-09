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


## Keycloak related
**Using Keycloak: A Quick Guide**

1. **Ensure MySQL/PostgreSQL is Running**  
   Before starting Keycloak, make sure the MySQL or PostgreSQL database that Keycloak is using is up and running.

2. **Start Keycloak Server**  
   Use the following command to start the Keycloak server:

./kc.sh start --hostname-strict false --http-enabled true


Access Keycloak at: [http://localhost:8080](http://localhost:8080)  
Default credentials: `admin/admin`

3. **Create a Realm**

- Create a new realm named **gnc**.

4. **Create a User in the GNC Realm**

- Create a user within the **gnc** realm.
- Set a username and password for the user.
- Assign the **manage-users** and **manage-clients** roles to this user.

*(Insert the image here)*

- This user will be used in your `.env` file for authentication.

5. **Verify User Access**

- Log in to [http://localhost:8080/realms/gnc/console](http://localhost:8080/realms/gnc/console) using the user credentials you created to verify that they can log in and access the console.

