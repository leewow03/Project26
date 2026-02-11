from app.services.Session import Session

class WorkoutLogService:
    @staticmethod
    def save_log(log_obj):
        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = """
                    INSERT INTO WorkoutLog (routine_id, exercise_id, weight, reps, duration_seconds) 
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    log_obj.routine_id,
                    log_obj.exercise_id,
                    log_obj.weight,
                    log_obj.reps,
                    log_obj.duration_seconds
                ))
                conn.commit()
        finally:
            conn.close()

    @staticmethod
    def get_logs_by_routine(routine_id):
        """특정 루틴의 운동 기록들만 가져오기 (JOIN 활용)"""
        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                # 운동 이름(Exercise.name)도 같이 가져오면 화면에 뿌리기 좋겠죠?
                sql = """
                    SELECT l.*, e.name as exercise_name 
                    FROM WorkoutLog l
                    JOIN Exercise e ON l.exercise_id = e.id
                    WHERE l.routine_id = %s
                    ORDER BY l.performed_at DESC
                """
                cursor.execute(sql, (routine_id,))
                return cursor.fetchall() # 여기선 닉네임 등이 섞여있어 dict 그대로 보낼게요
        finally:
            conn.close()