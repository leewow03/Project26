from flask import render_template, request, redirect, url_for, session, Blueprint

from app.services import Session
from app.services.CrmService import CrmService

CrmF = Blueprint('crm', __name__)

@CrmF.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')

    uid = request.form.get('uid')
    upw = request.form.get('upw')

    #
    user = CrmService.login_user(uid, upw)

    if user:
        session['user_id'] = user['id']
        session['user_name'] = user['name']
        session['user_uid'] = user['uid']
        session['user_role'] = user['role']
        return redirect(url_for('index'))
    else:
        return "<script>alert('아이디나 비번이 틀렸습니다.');history.back();</script>"

@CrmF.route('/logout')
def logout():
    session.clear()  # 세션 데이터를 모두 삭제
    # 로그아웃 후 로그인 페이지로 보낼 때도 crm.login 이라고 써야 합니다.
    return redirect(url_for('crm.login'))

@CrmF.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'GET':
        return render_template('auth/join.html')

    uid = request.form.get('uid')
    password = request.form.get('password')
    name = request.form.get('name')

    # 3. 여기도 CrmService로 수정
    if CrmService.check_duplicate_uid(uid):
        return "<script>alert('이미 존재하는 아이디입니다.'); history.back();</script>"

    # 4. 여기도 CrmService로 수정
    if CrmService.register_member(uid, password, name):
        return "<script>alert('회원가입이 완료되었습니다!'); location.href='/login';</script>"
    else:
        return "가입 중 오류가 발생했습니다."

@CrmF.route('/member_edit', methods=['GET','POST'])
def member_edit():
    if 'user_id' not in session: #세션에 user_id가 없으면
        return redirect(url_for('login')) #로그인 경로로 보냄

    # 있으면 db 연결 시작!
    conn = Session.get_connection()
    try:
        with conn.cursor() as cursor:
            if request.method == 'GET':
            # 기존 정보 불러오기
                cursor.execute("SELECT * FROM member WHERE id = %s", (session['user_id'],))
                user_info = cursor.fetchone()

                return render_template('auth/member_edit.html', user = user_info)
                #                                         ★get요청시 페이지      객체 전달용 코드★
            new_name = request.form.get('name')
            new_pw = request.form.get('password')
            # POST 요청: 정보 업데이트
            if new_pw:  # 비밀번호 입력 시에만 변경
                sql = "UPDATE member SET password = %s WHERE id = %s"
                cursor.execute(sql, (new_pw, session['user_id']))
            else:  # 이름만 변경
                sql = "UPDATE member SET name = %s WHERE id = %s"
                cursor.execute(sql, (new_name, session['user_id']))

            conn.commit()
            session['user_name'] = new_name  # 세션 이름 정보도 갱신
            return "<script>alert('정보가 수정되었습니다.'); location.href='/myprofile';</script>"

    except Exception as e:
        print(f"회원수정 에러: {e}")
        return "가입 중 오류가 발생했습니다. /n member_edit()메서드를 확인하세요!!!"


    finally:
        conn.close()

@CrmF.route('/myprofile')
def myprofile():
    if 'user_id' not in session:
        return redirect(url_for('crm.login'))


    # 5. 여기도 CrmService로 수정
    user_info, board_count = CrmService.get_member_info(session['user_id'])
    return render_template('auth/myprofile.html', user=user_info, board_count=board_count)


