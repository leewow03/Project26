class Routine:
    def __init__(self, routine_name, day_of_week, id=None, created_at=None):
        self.id = id
        self.routine_name = routine_name
        self.day_of_week = day_of_week
        self.created_at = created_at

    @staticmethod
    def from_db(row):
        return Routine(
            id=row.get('id'),
            routine_name=row.get('routine_name'),
            day_of_week=row.get('day_of_week'),
            created_at=row.get('created_at')
        )