from app.services.Session import Session
from app.models.Exercise import Exercise

class ExerciseService:
    @staticmethod
    def add_exercise(exercise_obj):
        """새로운 운동 종목 등록"""
        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "INSERT INTO Exercise (Exercise_name, target_muscle) VALUES (%s, %s)"
                cursor.execute(sql, (exercise_obj.exercise_name, exercise_obj.target_muscle))
                conn.commit()
        finally:
            conn.close()

    @staticmethod
    def get_all_exercises():
        """등록된 모든 운동 종목 가져오기"""
        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM Exercise ORDER BY Exercise_name ASC"
                cursor.execute(sql)
                rows = cursor.fetchall()
                return [Exercise.from_db(row) for row in rows]
        finally:
            conn.close()