from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from models import db, Exercise, Workout, WorkoutExercises
from schemas import (
    exercise_schema, exercises_schema, exercise_detail_schema,
    workout_schema, workouts_schema, workout_detail_schema,
    workout_exercise_schema,
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

# Define Routes 


# Workouts 

@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return make_response(jsonify(workouts_schema.dump(workouts)), 200)


@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = db.get_or_404(Workout, id)
    return make_response(jsonify(workout_detail_schema.dump(workout)), 200)


@app.route('/workouts', methods=['POST'])
def create_workout():
    try:
        data = workout_schema.load(request.get_json() or {})
        workout = Workout(**data)
        db.session.add(workout)
        db.session.commit()
    except ValidationError as err:
        return make_response(jsonify({'errors': err.messages}), 400)
    except (ValueError, IntegrityError) as err:
        db.session.rollback()
        return make_response(jsonify({'errors': str(err)}), 400)
    return make_response(jsonify(workout_schema.dump(workout)), 201)


@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = db.get_or_404(Workout, id)
    db.session.delete(workout)  # cascade also deletes its WorkoutExercises
    db.session.commit()
    return make_response(jsonify({'message': f'Workout {id} deleted'}), 200)


# Exercises 

@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return make_response(jsonify(exercises_schema.dump(exercises)), 200)


@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = db.get_or_404(Exercise, id)
    return make_response(jsonify(exercise_detail_schema.dump(exercise)), 200)


@app.route('/exercises', methods=['POST'])
def create_exercise():
    try:
        data = exercise_schema.load(request.get_json() or {})
        exercise = Exercise(**data)
        db.session.add(exercise)
        db.session.commit()
    except ValidationError as err:
        return make_response(jsonify({'errors': err.messages}), 400)
    except (ValueError, IntegrityError) as err:
        db.session.rollback()
        return make_response(jsonify({'errors': str(err)}), 400)
    return make_response(jsonify(exercise_schema.dump(exercise)), 201)


@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = db.get_or_404(Exercise, id)
    db.session.delete(exercise)  # cascade also deletes its WorkoutExercises
    db.session.commit()
    return make_response(jsonify({'message': f'Exercise {id} deleted'}), 200)


# Add an exercise to a workout 

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises',
           methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    db.get_or_404(Workout, workout_id)
    db.get_or_404(Exercise, exercise_id)
    try:
        data = workout_exercise_schema.load(request.get_json() or {})
        we = WorkoutExercise(workout_id=workout_id, exercise_id=exercise_id, **data)
        db.session.add(we)
        db.session.commit()
    except ValidationError as err:
        return make_response(jsonify({'errors': err.messages}), 400)
    except (ValueError, IntegrityError) as err:
        db.session.rollback()
        return make_response(jsonify({'errors': str(err)}), 400)
    return make_response(jsonify(workout_exercise_schema.dump(we)), 201)


if __name__ == '__main__':
    app.run(port=5555, debug=True)