from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from LMS.common.Session import Session
from ultralytics import YOLO
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

model = YOLO('yolo11m.pt')
VEHICLE_CLASSES = {2: 'car', 5: 'bus', 7: 'truck'}

# 로그인
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    uid = request.form.get('uid')
    password = request.form.get('password')
    conn = Session.get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "select id, uid, name, role from members where uid = %s and password=%s"
            cursor.execute(sql, (uid, password))
            user = cursor.fetchone()
            if user:
                session['user_id'] = user['id']
                session['user_name'] = user['name']
                session['user_uid'] = user['uid']
                session['user_role'] = user['role']
                return redirect(url_for('index'))
            else:
                return "<script>alert('아이디 또는 비밀번호가 틀렸습니다.');history.back();</script>"
    finally:
        conn.close()

# 로그아웃
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# 회원가입
@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'GET':
        return render_template('join.html')
    uid = request.form.get('uid')
    password = request.form.get('password')
    name = request.form.get('username')
    email = request.form['email']
    conn = Session.get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("select id from members where uid = %s", (uid,))
            if cursor.fetchone():
                return "<script>alert('이미 존재하는 아이디입니다.');history.back();</script>"
            sql = "insert into members (uid, password, name, email) values (%s, %s, %s, %s)"
            cursor.execute(sql, (uid, password, name, email))
            conn.commit()
            return "<script>alert('회원가입이 완료되었습니다.');location.href='/login';</script>"
    except Exception as e:
        print(f"회원가입 에러: {e}")
        return "회원가입 중 오류가 발생했습니다."
    finally:
        conn.close()

# 회원수정
@app.route('/member/edit', methods=['GET', 'POST'])
def member_edit():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = Session.get_connection()
    try:
        with conn.cursor() as cursor:
            if request.method == 'GET':
                cursor.execute("select * from members where id = %s", (session['user_id'],))
                user_info = cursor.fetchone()
                return render_template('member_edit.html', user=user_info)
            new_name = request.form.get('name')
            new_password = request.form.get('password')
            if new_password:
                sql = "update members set password = %s where id = %s"
                cursor.execute(sql, (new_password, session['user_id']))
            else:
                sql = "update members set name = %s where id = %s"
                cursor.execute(sql, (new_name, session['user_id']))
            conn.commit()
            session['user_name'] = new_name
            return "<script>alert('정보가 수정되었습니다.');location.href='/mypage';</script>"
    finally:
        conn.close()

# 마이페이지
@app.route('/mypage')
def mypage():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = Session.get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("select * from members where id = %s", (session['user_id'],))
            user_info = cursor.fetchone()
            return render_template('mypage.html', user=user_info)
    finally:
        conn.close()

# 분석 게시판
@app.route('/analyze')
def analyze():
    return render_template('analyze.html')

# YOLO 분석 API
@app.route('/board/result', methods=['POST'])
def board_result():
    file = request.files.get('image_file')
    if not file:
        return jsonify({'analysis_result': '이미지가 없습니다.'}), 400
    img_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(img_path)
    results = model(img_path)[0]
    detected = []
    for box in results.boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        if cls_id in VEHICLE_CLASSES and conf > 0.4:
            detected.append(f"{VEHICLE_CLASSES[cls_id]} (신뢰도: {round(conf*100, 1)}%)")
    result_text = "감지된 차량:\n" + "\n".join(detected) if detected else "차량이 감지되지 않았습니다."
    return jsonify({'analysis_result': result_text})


# 사이트 소개
@app.route('/introduce')
def about():
    return render_template('introduce.html')

# 메인
@app.route('/')
def index():
    return render_template('main.html')


@app.route('/board')
def board():
    records = ...  # DB에서 감지 이력 조회
    return render_template('board.html', records=records)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)