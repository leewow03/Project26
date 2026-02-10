from flask import render_template, request, redirect, url_for, session,Blueprint
from app.services.Session import Session
from app.models.Board import Board

BoardF = Blueprint('board', __name__)

@BoardF.route('/board/write',methods=['GET','POST']) #http://localhost:5000//board/write
def board_write():
# 1. 사용자가 '글쓰기' 버튼을 눌러서 들어왔을 때 (화면 보여주기)
    if request.method == 'GET':
        # 로그인 체크 (로그인 안 했으면 글 못 쓰게)
        if 'user_id' not in session:
            return '<script>alert("로그인 후 이용 가능합니다."); location.href="/login";</script>'
        return render_template('auth/board_write.html')

# 2. 사용자가 '등록하기' 버튼을 눌러서 데이터를 보냈을때 (DB 저장)
    elif request.method == 'POST': #<form acation="/board/write" methods="POST">
        title =request.form.get('title')
        content = request.form.get('content')
        #세션에 저장된 로그인 유저의 id(member_id)
        member_id = session.get('user_id')

        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "INSERT INTO boards (member_id, title, content) VALUES (%s, %s, %s)"
                cursor.execute(sql, (member_id, title, content))
                conn.commit()
            return redirect(url_for('board.board_list'))  # 저장 후 목록으로 이동
        except Exception as e:
            print(f"글쓰기 에러: {e}")
            return "저장 중 에러가 발생했습니다."
        finally:
            conn.close()

@BoardF.route('/board') #http://localhost:500/board
def board_list():
    conn = Session.get_connection()
    try:
        with conn.cursor() as cursor:
            # 작성자 이름을 함꼐 가져오기 위한 JOIN 사용
            sql = """
                SELECT b.*, m.name as writer_name
                FROM boards b
                JOIN member m ON b.member_id = m.id
                ORDER BY b.id DESC
            """
            cursor.execute(sql)
            rows = cursor.fetchall()
            boards = [Board.from_db(row) for row in rows] # from LMS.domain import Board
            return render_template('auth/board_list.html', boards=boards)
    finally:
        conn.close()

@BoardF.route('/board/view/<int:board_id>') #http://localhost:5000/board/view/99(게시물번호)
def board_view(board_id):
    conn = Session.get_connection()
    try:
            with conn.cursor() as cursor:
            # JOIN을 동해 작성자 정보(name, uid)를 함께 조회
                sql = """
                    SELECT b .* , m.name as writer_name, m.uid as writer_uid
                    FROM boards b
                    JOIN member m ON b.member_id = m.id
                    WHERE b.id = %s
                    """
                cursor.execute(sql, (board_id,))
                row = cursor.fetchone()
                print(row) #db에서 나온 dict타입 콘솔에 출력 테스트용
                if not row:
                    return "<script>alert('존재하지 않는 게시글입니다.');history.back();</script>"

                # Board 객체로 변환 (앞서 작성한 Board.py의 from_db 활용)
                board = Board.from_db(row)

                return render_template('auth/board_view.html', board=board)
    finally:
        conn.close()

@BoardF.route ('/board/edit/<int:board_id>', methods=['GET','POST'])
def board_edit(board_id):
    conn = Session.get_connection()
    try:
        with conn.cursor() as cursor:
        # 1. 화면 보여주기 (기존 데이터 로드)
            if request.method == 'GET':
                sql = "SELECT * FROM boards WHERE id = %s"
                cursor.execute(sql, (board_id,))
                row = cursor.fetchone()

                if not row:
                    return "<script>alert('존재하지 않는 게시글입니다.'); history.back(); </script>"

                # 본인 확인 로직 (필요시 추가)
                if row['member_id'] != session.get('user_id'):
                    return "<script>alert('수정 권한이 없습니다.'); history.back(); </script>"
                print(row)# 콘솔에 출력 테스트용
                board = Board.from_db(row)
                return render_template( 'board.board_edit.html', board=board)

            # 2. 실제 DB 업데이트 처리
            elif request.method == 'POST':
                title = request.form.get('title')
                print(title)
                content = request.form.get('content')

                sql = "UPDATE boards SET title=%s, content=%s WHERE id=%s"
                cursor.execute(sql, (title, content, board_id))
                conn.commit()

                return redirect(url_for('board.board_view', board_id=board_id))

    finally:
        conn.close()

@BoardF.route('/board/delete/<int:board_id>')
def board_delete(board_id):

    conn = Session.get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM boards WHERE id = %s" # 저장된 테이블명 boards 사용
            cursor.execute(sql, (board_id, ))
            conn.commit()

            if cursor.rowcount > 0:
                print(f"게시글 {board_id}번 삭제 성공")
            else:
                return "<script>alert('삭제할 게시글이 없거나 권한이 없습니다.'); history.back(); </script>"

        return redirect(url_for('board.board_list'))
    except Exception as e:
        print(f"삭제 에러: {e}")
        return "삭제 중 오류가 발생했습니다."
    finally:
        conn.close()

