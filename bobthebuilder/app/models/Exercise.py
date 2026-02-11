class Exercise:
    def __init__(self, exercise_name, target_muscle, id=None):
        self.id = id
        self.exercise_name = exercise_name
        self.target_muscle = target_muscle

    @staticmethod
    def from_db(row):
        return Exercise(
            id=row.get('id'),
            exercise_name=row.get('Exercise_name'), # DB 컬럼명 주의
            target_muscle=row.get('target_muscle')
        )