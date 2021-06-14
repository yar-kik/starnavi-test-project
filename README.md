# Test task: Python Developer (Social Network)
[![Build Status](https://travis-ci.com/yar-kik/starnavi-test-project.svg?branch=master)](https://travis-ci.com/yar-kik/starnavi-test-project)
[![Coverage Status](https://coveralls.io/repos/github/yar-kik/starnavi-test-project/badge.svg?branch=master)](https://coveralls.io/github/yar-kik/starnavi-test-project?branch=master)
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-3810/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Introduction
Object of this task is to create a simple REST API. 

API was documented with [Postman](https://documenter.getpostman.com/view/14489034/TzeUn8Ty#cebb3e50-23dd-4728-805d-a0687bfe2d35).

API was deployed on [Heroku](https://starnavi-test-project.herokuapp.com).

## Technologies
Project uses such technologies:
* Django and DRF with JWT-token for auth
* PostgreSQL
* Docker for containerizing

## Usage
Get local copy of project with: 
```
git clone https://github.com/yar-kik/starnavi-test-project.git
``` 
To build a local development environment and start API server run:  
```
docker-compose -f docker-compose-dev.yml up -d 
``` 
Or you can build a production ready environment: 
```
docker-compose -f docker-compose.yml up -d
``` 
This may take a few minutes. Finally, your api will work on `http://localhost:8000/`.

## Basic Features
* user signup
* user login
* post creation
* post like/unlike
* post unlike
* analytics about how many likes was made. Example url /api/analitics/?date_from=2020-02-02&date_to=2020-02-15. API should return analytics aggregated by day.
* user activity an endpoint which will show when user was login last time and when he mades a last request to the service.
