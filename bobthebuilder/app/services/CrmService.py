from app.services.Session import Session


class CrmService:

    @staticmethod
    def login_user(uid, upw):
        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT id, name, uid, role FROM Member WHERE uid = %s AND password = %s"
                cursor.execute(sql, (uid, upw))
                return cursor.fetchone()
        finally:
            conn.close()

    @staticmethod
    def check_duplicate_uid(uid):
        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id FROM Member WHERE uid = %s", (uid,))
                return cursor.fetchone()
        finally:
            conn.close()

    @staticmethod
    def register_member(uid, password, name):
        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "INSERT INTO Member (uid, password, name) VALUES (%s, %s, %s)"
                cursor.execute(sql, (uid, password, name))
                conn.commit()
                return True
        except Exception as e:
            print(f"회원가입 에러: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def get_member_info(member_id):
        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                # 회원 정보 조회
                cursor.execute("SELECT * FROM Member WHERE id = %s", (member_id,))
                user_info = cursor.fetchone()

                # 게시글 개수 조회 (보너스: 마이페이지용)
                cursor.execute("SELECT COUNT(*) as board_count FROM boards WHERE member_id = %s", (member_id,))
                board_result = cursor.fetchone()

                return user_info, board_result['board_count'] if board_result else 0
        finally:
            conn.close()

    @staticmethod
    def update_member(member_id, name, password=None):
        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                if password:
                    sql = "UPDATE Member SET name = %s, password = %s WHERE id = %s"
                    cursor.execute(sql, (name, password, member_id))
                else:
                    sql = "UPDATE Member SET name = %s WHERE id = %s"
                    cursor.execute(sql, (name, member_id))
                conn.commit()
                return True
        except Exception as e:
            print(f"수정 에러: {e}")
            return False
        finally:
            conn.close()