# Flask Api Authentication

Example Project using Api authentication with Flask - Python

# Requirements

Python is required to run this project.
https://python.org/

# Installation

Use the following command on the terminal

```sh
pip3 install -r requirements.txt
```

# Libs

- Flask
- Flask SQL Alchemy
- Flask Login - https://flask-login.readthedocs.io/en/latest/

# Flask Shell

Use to create and make new registrys on the database

Commands

```sh
# Enters the flask shell on the terminal
flask shell

# Create an instance of the object user with username and password values
user = User(username="admin", password="123")

# See the user info
user
user.username


# Save the object on the database
db.session.add(user)
db.session.commit()

```

# Run Docker for MySql

Requires docker desktop installed.\
On bash run:

```sh
docker-compose up
# or 
docker-compose up -d #does not lock the terminal
```
if its already running: 

```sh
docker-compose up --force-recreate
```