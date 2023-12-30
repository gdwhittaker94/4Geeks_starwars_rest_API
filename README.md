# Starwars REST API 
For this project we were tasked with creating our own API instead of just communicating with one like we had been doing in previous projects. Specifically, a REST API ('Representational State Transfer API') which is a type of API that conforms to the constraints of the REST architectural style, uses HTTP methods (typically to perform CRUD operations), usually returns data in JSON format, and features a stateless client-server model. For more info [see here](t.ly/xxMkG).

To make this REST API we used Python, Flask and SQLAlchemy together for the first time, as well as Postman API for testing, in order to imitate the same API we had been using to create a recent [Starwars blog project](https://github.com/gdwhittaker94/4Geeks_stars_wars_blog).

[starwars_rest_api.webm](https://github.com/gdwhittaker94/4Geeks_starwars_rest_API/assets/105855731/d4840bd2-a924-472d-88cc-82bb7e2a3806)


## Project Documentation
Create flask API's in minutes, [📹 watch the video tutorial](https://youtu.be/ORxQ-K3BzQA).

- [Extensive documentation here](https://start.4geeksacademy.com).
- Integrated with Pipenv for package managing.
- Fast deloyment to render.com or heroku with `$ pipenv run deploy`.
- Use of `.env` file.
- SQLAlchemy integration for database abstraction.

## 1) Installation

This template installs itself in a few seconds if you open it for free with Codespaces (recommended) or Gitpod.
Skip this installation steps and jump to step 2 if you decide to use any of those services.

> Important: The boiplerplate is made for python 3.10 but you can change the `python_version` on the Pipfile.

The following steps are automatically runned withing gitpod, if you are doing a local installation you have to do them manually:

```sh
pipenv install;
psql -U root -c 'CREATE DATABASE example;'
pipenv run init;
pipenv run migrate;
pipenv run upgrade;
```

## 2) How to Start coding

There is an example API working with an example database. All your application code should be written inside the `./src/` folder.

- src/main.py (it's where your endpoints should be coded)
- src/models.py (your database tables and serialization logic)
- src/utils.py (some reusable classes and functions)
- src/admin.py (add your models to the admin and manage your data easily)

For a more detailed explanation, look for the tutorial inside the `docs` folder.

## Remember to migrate every time you change your models

You have to migrate and upgrade the migrations for every update you make to your models:

```bash
$ pipenv run migrate # (to make the migrations)
$ pipenv run upgrade  # (to update your databse with the migrations)
```

## Check your API live

1. Once you run the `pipenv run start` command your API will start running live and you can open it by clicking in the "ports" tab and then clicking "open browser".

> ✋ If you are working on a coding cloud like [Codespaces](https://docs.github.com/en/codespaces/developing-in-codespaces/forwarding-ports-in-your-codespace#sharing-a-port) or [Gitpod](https://www.gitpod.io/docs/configure/workspaces/ports#configure-port-visibility) make sure that your forwared port is public.
