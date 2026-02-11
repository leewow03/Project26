from flask import Blueprint, render_template, request, redirect, url_for
from app.models.Routine import Routine
from app.services.RoutineService import RoutineService

RoutineF = Blueprint('routine', __name__)

@RoutineF.route('/routine', methods=['GET', 'POST'])
def routine_list():
    if request.method == 'POST':
        # 1. 사용자가 입력한 루틴 정보 받아서 그릇(Model)에 담기
        new_routine = Routine(
            routine_name=request.form.get('routine_name'),
            day_of_week=request.form.get('day_of_week')
        )
        # 2. 서비스 주방장에게 저장 시키기
        RoutineService.add_routine(new_routine)
        return redirect(url_for('routine.routine_list'))

    # GET 요청 시: 전체 루틴 목록 보여주기
    routines = RoutineService.get_all_routines()
    return render_template('auth/routine_list.html', routines=routines)