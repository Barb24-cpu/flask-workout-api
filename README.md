# flask-workout-api

# Workout Tracker API

## Description
A Flask REST API for personal trainers to track workouts and reusable exercises.
Built with Flask, SQLAlchemy, Flask-Migrate and Marshmallow. A workout can contain
many exercises, with reps, sets or duration recorded for each.

## Installation
1. Clone the repo and enter it:
```bash
   git clone https://github.com/Barb24-cpu/flask-workout-api.git
   cd flask-workout-api
```
2. Install dependencies and activate the virtual environment:
```bash
   pipenv install
   pipenv shell
```
3. Create and migrate the database:
```bash
   cd server
   flask db init
   flask db migrate -m "initial migration"
   flask db upgrade head
```
   (If a `migrations/` folder already exists, skip `flask db init`.)
4. Seed the database:
```bash
   python seed.py
```

## Running the app
From the `server/` directory:
```bash
flask run -p 5555
```
The API runs at http://localhost:5555

## Endpoints
| Method | Endpoint | Description |
|---|---|---|
| GET | `/workouts` | List all workouts |
| GET | `/workouts/<id>` | Show one workout with its exercises, including reps/sets/duration |
| POST | `/workouts` | Create a workout |
| DELETE | `/workouts/<id>` | Delete a workout and its associated WorkoutExercises |
| GET | `/exercises` | List all exercises |
| GET | `/exercises/<id>` | Show an exercise and its associated workouts |
| POST | `/exercises` | Create an exercise |
| DELETE | `/exercises/<id>` | Delete an exercise and its associated WorkoutExercises |
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout with reps/sets/duration |

## Validations
- Table constraints: not-null, unique exercise name, check constraints on durations, reps and sets.
- Model validations: name, category, duration and notes length.
- Schema validations: Marshmallow field validators and a rule requiring reps, sets or duration.

## Dependencies
See the `Pipfile`.