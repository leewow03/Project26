from flask import render_template, request, redirect, url_for, session,Blueprint
from app.models import Score
from app.services.Session import Session

ScoreF = Blueprint('score', __name__)

@ScoreF.route('/score/add')
def score_add():
    if session.get('user_role') not in ('admin', 'manager'):
        return "<script>alert('권한이 없습니다.'); history.back(); </script>"

    target_uid = request.args.get('uid') #주소를 통해서 넘어가는값
    target_name = request.args.get('name')
    # request.args는 URL을 통해서 넘어오는 값 주소뒤에 ?K=V&K=V~~

    conn = Session.get_connection()
    try:
        with conn.cursor() as cursor:
            # 1. 대상 학생의 id 찾기
            cursor.execute("SELECT id FROM members WHERE uid = %s", (target_uid, ))
            student = cursor.fetchone()

            # 2. 기존 성적이 있는지 조회
            existing_score = None
            if student:
                cursor.execute("SELECT * FROM scores WHERE member_id = %s", (student['id'], ))
                row = cursor. fetchone ()
                print(row) #테스트용 코드를 dict타입으로 콘솔 출력
                if row:
                    # 기존에 만든 Score.from_db 활용
                    existing_score= Score.from_db(row)
                    # 위쪽에 갹체 로드 처리 : from LMS.dmain import Board, Score

            return render_template('score_form.html',
                                   target_uid=target_uid,
                                   target_name=target_name,
                                   score=existing_score) # score 객체전달

    finally:
        conn.close()

@ScoreF.route('/score/save', methods = ['POST'])
def score_save():
    if session.get('user_role') not in ('admin', 'manager'):
            return "권한 오류", 403
            # 웹페이지에 오류 페이지로 교체

    # 폼 데이터 수집
    target_uid = request.form.get('target_uid')
    kor = int(request.form.get('korean', 0))
    eng = int(request.form.get('english', 0))
    math = int(request.form.get('math', 0))

    conn = Session.get_connection()
    try:
        with conn.cursor() as cursor:
            #1. 대상 학생의 id(PK) 가져오기 -> 학생의 번호를 가져오기
            cursor.execute("SELECT id FROM members WHERE uid = %s", (target_uid,))
            student = cursor.fetchone()
            print(student)
            if not student:
                return "<script>alert('존재하지 않는 학생입니다.'); history.back(); </script>"

            # 2.Score 객체 생성(계산 프로퍼티 활용)
            temp_score =Score(member_id=student['id'], kor=kor, eng=eng,math=math)
            #           __init__를 활용하여 객체 생성

            # 3. 기존 데이터가 있는지 확인
            cursor.execute("SElECT id FRom scores WHERE member_id = %s", (student['id']))
            is_exist=cursor.fetchone() #성적이 있으면 id가 나옴, 없으면 None

            if is_exist:
                # UPDATE 실행
                sql ="""
                    UPDATE scores SET korean=%s, english=%s, math=%s,
                    total=%s, average=%s, grade=%s
                    WHERE member_id = %s
                """
                cursor.execute(sql,(temp_score.kor, temp_score.eng,temp_score.math,
                                    temp_score.total, temp_score.avg, temp_score.grade,
                                    student['id']))

            else:
                #INSERT 실행
                sql = """
                INSERT INTO scores (member_id, korean, english, math, total, average, grade)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """

                cursor.execute(sql, (student['id'], temp_score.kor, temp_score.eng, temp_score.math,
                        temp_score.total, temp_score.avg, temp_score.grade))

            conn.commit()
            return f"<script>alert('{target_uid} 학생 성적 저장 완료!); locatin.href= '/score/list;</script>"
    finally:
        conn.close()

@ScoreF.route('/score/list')
def score_list(): #score 기반
    # 1. 권한 체크 (관리자나 매니저만 볼 수 있게 설정)
    if session.get('user_role') not in ('admin', 'manager'):
        return "<script>alert('권한이 없습니다.'); history.back() ;< /script>"

    conn = Session.get_connection()
    try:
        with conn.cursor() as cursor:
            # 2. JOIN을 사용하여 학생 이름(name)과 성적 데이터를 함께 조회
            # 성적이 없는 학생은 제외하고, 성적이 있는 학생들만 총점 순으로 정렬
            sql = """
                SELECT m.name, m.uid, s .* FROM scores s
                JOIN members m ON s.member_id = m.id
                ORDER BY s.total DESC
            """
            cursor.execute(sql)
            datas = cursor.fetchall()
            print(f" sql 결과 테스트 : {datas}")

            # 3. DB에서 가져온 딕셔너리 리스트를 Score 객체 리스트로 변환
            score_objects = []
            for data in datas:
                # Score 클래스에 정의한 from_db 활용
                s = Score.from_db(data) #직렬화(dict 타입을 -> 객체로 만들어)
                # 객체에 없는 이름(name) 정보는 수동으로 살짝 넣어주기 (join에서 만든 값 사용)
                s.name = data['name']
                s.uid = data['uid']
                score_objects.append(s) # 객체를 리스트에 넣음

            return render_template('score_list.html', scores=score_objects)
            #                           프론트 화면 ui에                  성적이 담긴 리스트 객체를 전달함!!
    finally:
        conn.close()

@ScoreF.route('/score/members')
def score_members (): #member기반으로 성적 있는지 확인
    if session.get('user_role') not in ('admin', 'manager'):
        return "<script>alert('권한이 없습니다.'); history.back() ;< /script>"

    conn = Session. get_connection()
    try:
        with conn.cursor() as cursor:
            # LEFT JOIN을 통해 성적이 있으면 s.id가 숫자로, 없으면 NULL로 나옵니다.
            sql = """
                SELECT m.id, m.uid, m.name, s.id AS score_id
                FROM members m
                LEFT JOIN scores s ON m.id = s.member_id
                WHERE m.role = 'user'
                ORDER BY m.name ASC
            """
            cursor.execute(sql)
            members = cursor.fetchall()
            return render_template( 'score_member_list.html', members=members)

    finally:
        conn.close()

@ScoreF.route('/score/my')
def score_my():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = Session.get_connection()
    try:
        with conn.cursor() as cursor:
            # 내 ID로만 조회
            sql = "SELECT * FROM scores WHERE member_id = %s"
            cursor.execute(sql, (session['user_id'], ))
            row = cursor.fetchone ()
            print(row)

            # Score 객체로 변환 (from_db 활용)
            score = Score.from_db(row) if row else None

            return render_template('score_my.html', score=score)
    finally:
        conn.close()






