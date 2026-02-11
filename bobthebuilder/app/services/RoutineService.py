from app.services.Session import Session
from app.models.Routine import Routine

class RoutineService:
    @staticmethod
    def add_routine(routine_obj):
        """새 루틴 저장"""
        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "INSERT INTO Routine (routine_name, day_of_week) VALUES (%s, %s)"
                cursor.execute(sql, (routine_obj.routine_name, routine_obj.day_of_week))
                conn.commit()
        finally:
            conn.close()

    @staticmethod
    def get_all_routines():
        """모든 루틴 목록 가져오기"""
        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM Routine ORDER BY id DESC"
                cursor.execute(sql)
                rows = cursor.fetchall()
                return [Routine.from_db(row) for row in rows]
        finally:
            conn.close()