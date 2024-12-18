# Infinite Heirarchical Comments

## Overview
Infinite Heirarichal Comments is a dockerized tree-based heirarchical level comment app that is developed using Flask as backend and React as frontend framework.

## Prerequisites
Ensure you have the following tools installed:
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Project Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Setup .env file
- Copy ENV file `cp .env.example .env`
- Update env variables

### 3. Build the Project
Use Docker Compose to build the project:
```bash
docker-compose build
```

### 4. Run the Project
Use Docker Compose to run the frontend and backend services:
```bash
docker-compose up
```

### 5. Access the Application
- **Frontend**: http://localhost:3000 (default React port)
**Backend**: http://localhost:5000 (Flask port)
- **Backend Swagger Documentation**: http://localhost:5000/apidocs

## Apply Alembic Migrations
Whenever a change is made in user or comments model, you have to apply the alembic migrations

### Create migration file
Change the 'Test migration' text accordingly
```bash
flask db migrate -m "Test migration"
```

### Apply migration
```bash
flask db upgrade
```


## Run Test Cases
There are three different ways to run the test cases.

### File specific test cases
```bash
python -m unittest test.test_users
```

### Class specific test cases
```bash
python -m unittest test.test_users.TestUserRoutes
```

### Indiviual test case
```bash
python -m unittest test.test_users.TestUserRoutes.test_signup_user_success
```

## API Endpoints
The Flask backend exposes two main routes:

### Users
- `POST /users/login`: Login as a user.
- `POST /users/signup`: Register a new user.

### Comments
- `GET /comments/list`: Retrieve all comments in a tree-based heirarchy.
- `POST /comments/create`: Create a new comment.
- `DELETE /comments/delete/<int:pk>`: Delete a comment.

> Full Swagger API documentation is available at `http://localhost:5000/apidocs`.


## Technologies Used
### Frontend:
- React
- Docker

### Backend:
- Flask
- Flask-SQLAlchemy (For database and ORM)
- Flask-Marshmallow (For defining schemas)
- Flask-JWT-Extended (For JWT Authentication)
- Swagger (Flasgger)
- Docker

## Notes
- Ensure ports `3000` (frontend) and `5000` (backend) are available.
- You can modify the `docker-compose.yml` file to change port bindings or service configurations.
