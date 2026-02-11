from flask import render_template, request, redirect, url_for, session, Blueprint
from app.services.BoardService import BoardService

BoardF = Blueprint('board', __name__)


@BoardF.route('/board')
def board_list():
    boards = BoardService.get_list()  # 서비스한테 시킴
    return render_template('auth/board_list.html', boards=boards)


@BoardF.route('/board/write', methods=['GET', 'POST'])
def board_write():
    if request.method == 'GET':
        if 'user_id' not in session:
            return '<script>alert("로그인 후 이용 가능합니다."); location.href="/login";</script>'
        return render_template('auth/board_write.html')

    # POST일 때: 데이터만 뽑아서 서비스에 전달
    BoardService.write(session.get('user_id'), request.form.get('title'), request.form.get('content'))
    return redirect(url_for('board.board_list'))


@BoardF.route('/board/view/<int:board_id>')
def board_view(board_id):
    board = BoardService.get_view(board_id)
    if not board:
        return "<script>alert('존재하지 않는 게시글입니다.');history.back();</script>"
    return render_template('auth/board_view.html', board=board)


@BoardF.route('/board/edit/<int:board_id>', methods=['GET', 'POST'])
def board_edit(board_id):
    if request.method == 'GET':
        board = BoardService.get_view(board_id)
        if board.member_id != session.get('user_id'):  # 권한 체크는 라우트가!
            return "<script>alert('수정 권한이 없습니다.'); history.back(); </script>"
        return render_template('auth/board_edit.html', board=board)

    BoardService.update(board_id, request.form.get('title'), request.form.get('content'))
    return redirect(url_for('board.board_view', board_id=board_id))


@BoardF.route('/board/delete/<int:board_id>')
def board_delete(board_id):
    BoardService.delete(board_id)
    return redirect(url_for('board.board_list'))