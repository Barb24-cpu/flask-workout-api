from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()

# Categories an exercise may belong to
VALID_CATEGORIES = ['strength', 'cardio', 'flexibility', 'balance']

class Exercise(db.Model):
    __tablename__ = 'exercises'

     # Table constraints
    __table_args__ = (
        db.CheckConstraint('length(name) > 0', name='ck_exercise_name_not_empty'),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    category = db.Column(db.String)
    equipment_needed = db.Column(db.Boolean)


        # Relationships
    workout_exercises = db.relationship(
        'WorkoutExercise', back_populates='exercise',
        cascade='all, delete-orphan')
    workouts = association_proxy('workout_exercises', 'workout')

    # Model validations
    @validates('name')
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError('Exercise name cannot be empty.')
        return value.strip()

    @validates('category')
    def validate_category(self, key, value):
        if value not in VALID_CATEGORIES:
            raise ValueError(f'Category must be one of: {", ".join(VALID_CATEGORIES)}.')
        return value


    def __repr__(self):
        return f'<Exercise {self.id}: {self.name}>'


class Workout(db.Model):
    __tablename__ = 'workouts'

     # Table constraints
    __table_args__ = (
        db.CheckConstraint('duration_minutes > 0', name='ck_workout_duration_positive'),
    )

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    duration_minutes = db.Column(db.Integer)
    notes = db.Column(db.Text)
  
         # Relationships
    workout_exercises = db.relationship(
        'WorkoutExercise', back_populates='workout',
        cascade='all, delete-orphan')
    exercises = association_proxy('workout_exercises', 'exercise')

    # Model validations
    @validates('duration_minutes')
    def validate_duration(self, key, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError('duration_minutes must be a positive integer.')
        return value

    @validates('notes')
    def validate_notes(self, key, value):
        if value is not None and len(value) > 500:
            raise ValueError('Notes must be 500 characters or fewer.')
        return value

    def __repr__(self):
        return f'<Workout {self.id}: {self.date}>'


class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

      # Table constraints
    __table_args__ = (
        db.CheckConstraint('reps >= 0', name='ck_we_reps_non_negative'),
        db.CheckConstraint('sets >= 0', name='ck_we_sets_non_negative'),
        db.CheckConstraint('duration_seconds >= 0', name='ck_we_duration_non_negative'),
    )


    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'))
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'))
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

         # Relationships
    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

     # Model validations
    @validates('reps', 'sets', 'duration_seconds')
    def validate_non_negative(self, key, value):
        if value is not None and (not isinstance(value, int) or value < 0):
            raise ValueError(f'{key} must be a non-negative integer.')
        return value

    def __repr__(self):
        return f'<WorkoutExercise {self.id}: workout={self.workout_id} exercise={self.exercise_id}>'