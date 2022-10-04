from datetime import datetime

from flask import Blueprint, url_for, request, render_template, g
from werkzeug.utils import redirect

from  pybo import db
from pybo.forms import CommentForm
from pybo.models import Question, Comment
from pybo.views.auth_views import login_required, flash

bp = Blueprint('comment', __name__, url_prefix='/comment')

@bp.route('/create/question/<int:question_id>', methods=('GET', 'POST'))
def create_question(question_id):
    form = CommentForm()
    question = Question.quert.get_or_404(question_id)
    if request.method == 'post' and form.validate_on_submit():
        if(g.user):
            comment = Comment(user=g.user, content=form.content.data, creat_date=datetime.now(), question=question)
        elif(not g.user):
                comment = Comment(content=form.content.data, create_date=datetime.now(), question=question)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('question.detail', question_id=question_id))
    return render_template('comment/comment_form.html', form=form)

@bp.route('/modify/question/<int:comment_id>', methods=('GET', 'POST'))
@login_required
def modify_question(comment_id):
    comment = Comment.qurey.get_or_404(comment_id)
    if g.user != comment.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('question.detail', question_id=comment.question_id))
    if request.method == "POST":
        form = CommentForm()
        if form.validate_on_submit():
            form.populate_obj(comment)
            comment.modify_date = datetime.now() #수정일시 저장
            db.session.commit()
            return  redirect(url_for('question.detail', question_id=comment.question_id))
    else:
        form = CommentForm(obj=comment)
    return render_template('comment/comment_form.html', form=form)

bp.route('/delete/question/<int:comment_id>')
@login_required
def delete_question(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    question_id = comment.question.id
    if g.user != comment.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))
