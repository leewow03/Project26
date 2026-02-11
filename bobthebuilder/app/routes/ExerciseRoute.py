from flask import Blueprint, render_template, request, redirect, url_for
from app.models.Exercise import Exercise
from app.services.ExerciseService import ExerciseService

ExerciseF = Blueprint('exercise', __name__)

@ExerciseF.route('/exercise', methods=['GET', 'POST'])
def exercise_list():
    if request.method == 'POST':
        # 1. 사용자가 입력한 운동 정보 받기
        new_ex = Exercise(
            exercise_name=request.form.get('exercise_name'),
            target_muscle=request.form.get('target_muscle')
        )
        # 2. 서비스에 저장 시킴
        ExerciseService.add_exercise(new_ex)
        return redirect(url_for('exercise.exercise_list'))

    # GET 요청 시: 전체 종목 보여주기
    exercises = ExerciseService.get_all_exercises()
    return render_template('auth/exercise_list.html', exercises=exercises)