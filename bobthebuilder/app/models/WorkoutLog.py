class WorkoutLog:
    def __init__(self, routine_id, exercise_id, weight, reps, duration_seconds, id=None, performed_at=None):
        self.id = id
        self.routine_id = routine_id
        self.exercise_id = exercise_id
        self.weight = weight
        self.reps = reps
        self.duration_seconds = duration_seconds
        self.performed_at = performed_at

    @staticmethod
    def from_db(row):
        return WorkoutLog(
            id=row.get('id'),
            routine_id=row.get('routine_id'),
            exercise_id=row.get('exercise_id'),
            weight=row.get('weight'),
            reps=row.get('reps'),
            duration_seconds=row.get('duration_seconds'),
            performed_at=row.get('performed_at')
        )