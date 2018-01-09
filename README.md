# Django_ams_api

Assignment Management System API built with Django Rest Framework

## Development
This application was developed using [Django Rest Framework](http://www.django-rest-framework.org/)

## Installation
* Make sure you have Python installed on your local machine.
* Clone the repository `$ git clone https://github.com/Del-sama/Django_ams_api.git`
* Change into the directory `$ cd /Django_ams_api`
* Install all required dependencies with `$ pip install -r requirements.txt`
* Create a `.env` file in your root directory as described in `.env.sample` file

## Testing
* python manage.py test

## Usage
* Start the application `$ python manage.py runserver`
* Use `Postman` to consume available endpoints
* A user can:
  * Create an account
  * Sign in
  * Sign out
  * Create assignments
  * Get assignments
  * Get a single assignment
  * Edit a single assignment
  * Delete a single assignment
  * Create courses
  * Get courses
  * Get a single course
  * Edit a single course
  * Delete a single course
  * Create submissions
  * Get submissions
  * Get a single submission
  * Edit a single submission
  * Delete a single submission
  * Get all assignments for a course
  * Get all submissions for an assignment
  * Get all assignments created by a particular user
  * get all submissions created by a particular user

## Endpoints
| Request type      | Endpoint          | Action |
| ------------- |:-------------:| -----:|
| POST          | /users/ | Create a user|
| POST          | /login/  | Log a user in |
| POST          | /logout/ | Sign a user out|
| POST           | courses/:id/assignments/     | Create an assignment
| GET          | /assignments/ | Get all assignment |
| GET           | /assignments/:id    | Get a particular assignment|
| DELETE        | /assignments/:id   | Delete an assignment|
| PUT           | /assignments/:id   | Update an assignment |
| POST           | /courses/     | Create a course
| GET          | /courses/ | Get all course |
| GET           | /courses/:id    | Get a particular course|
| DELETE        | /courses/:id   | Delete a course|
| PUT           | /courses/:id   | Update a course |
| POST           | assignments/:id/submissions/     | Create a submission
| GET          | /submissions/ | Get all submissions |
| GET           | /submissions/:id    | Get a particular submission|
| DELETE        | /submissions/:id   | Delete a submission|
| PUT           | /submissions/:id   | Update a submission |
