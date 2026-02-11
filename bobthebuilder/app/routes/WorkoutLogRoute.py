from flask import Blueprint, render_template, request, redirect, url_for
from app.models.WorkoutLog import WorkoutLog
from app.services.WorkoutLogService import WorkoutLogService

WorkoutLogF = Blueprint('log', __name__)


@WorkoutLogF.route('/log/write', methods=['POST'])
def log_write():
    # 사용자가 화면(Select Box 등)에서 선택한 ID값들과 수치들을 받아옵니다.
    new_log = WorkoutLog(
        routine_id=request.form.get('routine_id'),
        exercise_id=request.form.get('exercise_id'),
        weight=request.form.get('weight'),
        reps=request.form.get('reps'),
        duration_seconds=request.form.get('duration_seconds')
    )

    # 서비스 호출
    WorkoutLogService.save_log(new_log)

    # 저장 후 해당 루틴의 상세 페이지로 돌아가기
    return redirect(url_for('routine.view', routine_id=new_log.routine_id))