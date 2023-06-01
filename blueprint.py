from flask import Blueprint, render_template, flash, request, redirect, session, g, url_for, make_response
from Config.MODELS import UserModel, CommunityModel, ChatMessageModel, MemoModel
from Config.BASE.exts import db
from functools import wraps
from sqlalchemy import asc
from datetime import datetime

bp = Blueprint("bp", __name__, url_prefix='/')


def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if g.user:
            return func(*args, **kwargs)
        else:
            flash('Please log in first.')
            return redirect(url_for('bp.login'))

    return inner


@bp.route('/')
def hp():
    cmty_ls = CommunityModel.query.all()[::-1]
    return render_template('./hp.html', cmty_ls=cmty_ls)


@bp.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        name = request.form.get('name')
        pwd = request.form.get('password')
        user = UserModel.query.filter_by(username=name, password=pwd).first()

        if not user:
            flash("User is not registered or incorrect password.")
            return render_template('./BASE/login.html')
        else:
            session['user_id'] = user.id
            flash("Login successful.")
            return redirect('/')
    else:
        return render_template('./BASE/login.html')


@bp.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        name = request.form.get('name')
        pwd = request.form.get('password')
        verify_pwd = request.form.get('verify_password')

        if len(name) <= 10 and 8 <= len(pwd) <= 20 and pwd == verify_pwd and not UserModel.query.filter_by(
                username=name).first():
            with open(file='static/picture/portrait.jpg', mode='rb') as f:
                portrait = f.read()
            user = UserModel(username=name, password=pwd, portrait=portrait)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please log in.')
            return render_template('./BASE/login.html')
        else:
            flash('The account or password does not meet the requirements, or already exists.')
            return render_template('./BASE/signup.html')

    else:
        return render_template('./BASE/signup.html')


@bp.route('/log_out/')
def log_out():
    session.clear()
    flash('Logout successful.')
    return redirect('/')


@bp.route('/personal/', methods=['POST'])
def personal():
    if request.method == "POST":
        portrait_file = request.files.get('portrait_file')
        portrait_file.seek(0, 2)
        file_size = portrait_file.tell()

        if file_size <= 52428800:
            portrait_file.seek(0)
            user = UserModel.query.get(g.user_id)
            user.portrait = portrait_file.read()
            db.session.commit()
            flash('Change successful.')
            return redirect(url_for('bp.hp'))

        flash('The file exceeds 50MB or does not comply with the regulations.')
        return redirect(url_for('bp.hp'))


@bp.route('/community/', methods=['POST'])
@login_required
def community():
    if request.method == 'POST':
        content = request.form.get('content').replace('\n', '<br>')
        file_lengths_ls = []
        file_ls = []

        for i in range(1, 10):
            file = request.files.get(f'p-{i}')
            file.seek(0, 2)
            file_lengths_ls.append(file.tell())
            file.seek(0)
            file_ls.append(file) if file else None
            print(type(file))

        if not content and not file_ls:
            flash('Not allowed to be empty.')
            return redirect(url_for('bp.hp'))

        if any(file_size < 52428800 for file_size in file_lengths_ls):
            cmty = CommunityModel(content=content, user_id=g.user_id)
            for i, file in enumerate(file_ls):
                print(type(file))
                setattr(cmty, f'picture_{i + 1}', file.read())
            db.session.add(cmty)
            db.session.commit()
            flash('Post successful.')
            return redirect(url_for('bp.hp'))

        flash('The file exceeds 50MB or does not comply with the regulations.')
        return redirect(url_for('bp.hp'))


@bp.route('/chat/', methods=['GET', 'POST'])
@login_required
def chat():
    user_ls = UserModel.query.all()
    if request.method == "GET":
        return render_template('./chat.html', user_ls=user_ls)
    else:
        u_id = request.form.get('u-id')
        message_sender_ls = ChatMessageModel.query.filter_by(sender_id=g.user_id, receiver_id=u_id)
        message_receiver_ls = ChatMessageModel.query.filter_by(sender_id=u_id, receiver_id=g.user_id)
        message_ls = message_sender_ls.union(message_receiver_ls).order_by(asc(ChatMessageModel.timestamp)).all()
        receiver_name = UserModel.query.get(u_id).username
        return render_template('chat.html', message_ls=message_ls, user_ls=user_ls, hid=True, u_id=u_id,
                               receiver_name=receiver_name)


@bp.route('/send_message/', methods=['POST'])
@login_required
def send_message():
    content = request.form.get('send-message')
    sender_id = request.form.get('id-sender')
    receiver_id = request.form.get('id-receiver')

    if content:
        message = ChatMessageModel(sender_id=sender_id, receiver_id=receiver_id, content=content)
        db.session.add(message)
        db.session.commit()

    message_sender_ls = ChatMessageModel.query.filter_by(sender_id=sender_id, receiver_id=receiver_id)
    message_receiver_ls = ChatMessageModel.query.filter_by(sender_id=receiver_id, receiver_id=sender_id)
    message_ls = message_sender_ls.union(message_receiver_ls).order_by(asc(ChatMessageModel.timestamp)).all()

    user_ls = UserModel.query.all()
    receiver_name = UserModel.query.get(receiver_id).username

    if not content:
        flash('Not allowed to be empty.')
        return render_template('chat.html', message_ls=message_ls, user_ls=user_ls, hid=True, u_id=receiver_id,
                               receiver_name=receiver_name)

    return render_template('chat.html', message_ls=message_ls, user_ls=user_ls, hid=True, u_id=receiver_id,
                           receiver_name=receiver_name)


@bp.route('/memo/', methods=['GET', 'POST'])
@login_required
def memo():
    if request.method == 'GET':
        memo_ls = MemoModel.query.filter_by(user_id=g.user_id).all()
        return render_template('memo.html', memo_ls=memo_ls)
    else:
        content = request.form.get('add-content').replace('\n', '<br>')
        target_time_str = request.form.get('target-time')
        target_time = datetime.strptime(target_time_str, '%Y-%m-%dT%H:%M')

        memo_ = MemoModel(user_id=g.user_id, content=content, target_time=target_time)
        db.session.add(memo_)
        db.session.commit()
        flash('Add successful.')
        return redirect(url_for('bp.memo'))


@bp.route('/memo/delete/', methods=['POST'])
@login_required
def memo_delete():
    memo_id = request.form.get('memo_id')
    memo_ = MemoModel.query.get(memo_id)
    db.session.delete(memo_)
    db.session.commit()
    response = make_response()
    response.status_code = 200
    return response


@bp.route('/memo/share/', methods=['POST'])
@login_required
def memo_share():
    share_memo_id = request.form.get('memo_share')
    if share_memo_id:
        print(type(share_memo_id))
        memo_ = MemoModel.query.get(share_memo_id)
        cmty = CommunityModel(content=memo_.content, user_id=g.user_id)
        db.session.add(cmty)
        db.session.commit()
    else:
        flash('error')
    return redirect(url_for('bp.memo'))
