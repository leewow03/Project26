from app.services.Session import Session
from app.models.Board import Board

class BoardService:
    @staticmethod
    def get_list():
        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = """SELECT b.*, m.name as writer_name 
                         FROM boards b JOIN member m ON b.member_id = m.id 
                         ORDER BY b.id DESC"""
                cursor.execute(sql)
                rows = cursor.fetchall()
                return [Board.from_db(row) for row in rows]
        finally:
            conn.close()

    @staticmethod
    def write(member_id, title, content):
        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "INSERT INTO boards (member_id, title, content) VALUES (%s, %s, %s)"
                cursor.execute(sql, (member_id, title, content))
                conn.commit()
        finally:
            conn.close()

    @staticmethod
    def get_view(board_id):
        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = """SELECT b.*, m.name as writer_name, m.uid as writer_uid 
                         FROM boards b JOIN member m ON b.member_id = m.id 
                         WHERE b.id = %s"""
                cursor.execute(sql, (board_id,))
                row = cursor.fetchone()
                return Board.from_db(row) if row else None
        finally:
            conn.close()

    @staticmethod
    def update(board_id, title, content):
        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "UPDATE boards SET title=%s, content=%s WHERE id=%s"
                cursor.execute(sql, (title, content, board_id))
                conn.commit()
        finally:
            conn.close()

    @staticmethod
    def delete(board_id):
        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "DELETE FROM boards WHERE id = %s"
                cursor.execute(sql, (board_id,))
                conn.commit()
        finally:
            conn.close()