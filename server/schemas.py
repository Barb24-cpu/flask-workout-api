from marshmallow import Schema, fields, validate, validates_schema, ValidationError

from models import VALID_CATEGORIES



class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    category = fields.Str(required=True, validate=validate.OneOf(VALID_CATEGORIES))
    equipment_needed = fields.Bool(load_default=False)


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1))
    notes = fields.Str(allow_none=True, validate=validate.Length(max=500))


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)
    reps = fields.Int(allow_none=True, validate=validate.Range(min=1))
    sets = fields.Int(allow_none=True, validate=validate.Range(min=1))
    duration_seconds = fields.Int(allow_none=True)
    exercise = fields.Nested(ExerciseSchema, dump_only=True, validate=validate.Range(min=1))

     @validates_schema
    def require_some_measure(self, data, **kwargs):
        # A workout exercise must record reps/sets or a duration
        if not any(data.get(f) for f in ('reps', 'sets', 'duration_seconds')):
            raise ValidationError('Provide at least one of reps, sets or duration_seconds.')



class WorkoutDetailSchema(WorkoutSchema):
    # Includes reps/sets/duration data and each exercise (stretch goal)
    workout_exercises = fields.Nested(WorkoutExerciseSchema, many=True, dump_only=True)


class ExerciseDetailSchema(ExerciseSchema):
    workouts = fields.Nested(WorkoutSchema, many=True, dump_only=True)


exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
exercise_detail_schema = ExerciseDetailSchema()
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
workout_detail_schema = WorkoutDetailSchema()
workout_exercise_schema = WorkoutExerciseSchema()