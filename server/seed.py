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


        # Workouts
    w1 = Workout(date=date(2026, 10, 12), duration_minutes=45, notes='Leg day')
    w2 = Workout(date=date(2026, 10, 14), duration_minutes=30, notes='Cardio and core')
    w3 = Workout(date=date(2026, 10, 16), duration_minutes=60, notes='Full body')
    db.session.add_all([w1, w2, w3])
    db.session.commit() 

     # WorkoutExercises
    db.session.add_all([
        WorkoutExercise(workout_id=w1.id, exercise_id=squat.id, reps=10, sets=4),
        WorkoutExercise(workout_id=w2.id, exercise_id=running.id, duration_seconds=1200),
        WorkoutExercise(workout_id=w3.id, exercise_id=pushup.id, reps=15, sets=3),
        WorkoutExercise(workout_id=w3.id, exercise_id=yoga.id, duration_seconds=600),
    ])
    db.session.commit()
    print('Database seeded.')