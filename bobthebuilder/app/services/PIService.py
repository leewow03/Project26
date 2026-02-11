from app.services.Session import Session
from app.models.PI import PI

class PIService:
    @staticmethod
    def save_pi(pi_obj):
        """Model 객체를 받아서 DB에 저장"""
        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = """
                    INSERT INTO PI (height, weight, body_fat, muscle_mass) 
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    pi_obj.height,
                    pi_obj.weight,
                    pi_obj.body_fat,
                    pi_obj.muscle_mass
                ))
                conn.commit()
        finally:
            conn.close()

    @staticmethod
    def get_all_pi():
        """DB에서 모든 기록을 가져와서 Model 객체 리스트로 변환"""
        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM PI ORDER BY recorded_at DESC"
                cursor.execute(sql)
                rows = cursor.fetchall()
                # DB 한 줄 한 줄을 PI 객체로 만들어서 리스트에 담음
                return [PI.from_db(row) for row in rows]
        finally:
            conn.close()