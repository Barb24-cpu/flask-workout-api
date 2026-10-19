#!/usr/bin/env python3

from datetime import date

from app import app
from models import db, Exercise, Workout, WorkoutExercise

with app.app_context():
   # Clear tables (child table first because of foreign keys)
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

     # Exercises
    squat = Exercise(name='Squat', category='strength', equipment_needed=True)
    pushup = Exercise(name='Push-up', category='strength', equipment_needed=False)
    running = Exercise(name='Running', category='cardio', equipment_needed=False)
    yoga = Exercise(name='Yoga Flow', category='flexibility', equipment_needed=False)
    db.session.add_all([squat, pushup, running, yoga])
