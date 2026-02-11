from flask import Blueprint, render_template, request, redirect, url_for
from app.models.PI import PI
from app.services.PIService import PIService

PIF = Blueprint('pi', __name__)

@PIF.route('/pi', methods=['GET', 'POST'])
def pi_index():
    if request.method == 'POST':
        # 1. Route의 역할: 사용자 입력값(Form)을 받아서 Model 객체(그릇)에 담기
        new_pi = PI(
            height=request.form.get('height'),
            weight=request.form.get('weight'),
            body_fat=request.form.get('body_fat'),
            muscle_mass=request.form.get('muscle_mass')
        )

        # 2. Service의 역할 호출: "이 객체 저장해줘!"
        PIService.save_pi(new_pi)

        # 3. 다시 목록 화면으로 이동
        return redirect(url_for('pi.pi_index'))

    # GET 요청일 때: 목록 불러오기
    # 1. Service에게 데이터 가져오라고 시킴
    pi_list = PIService.get_all_pi()

    # 2. 받아온 데이터를 HTML에 전달
    return render_template('auth/pi_list.html', pi_list=pi_list)