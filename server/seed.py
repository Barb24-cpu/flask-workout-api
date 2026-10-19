#!/usr/bin/env python3

from datetime import date

from app import app
from models import db, Exercise, Workout, WorkoutExercise

with app.app_context():
   # Clear tables (child table first because of foreign keys)
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()