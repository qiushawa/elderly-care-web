from flask import Blueprint, render_template, redirect
from flask import session
from flask import request
from app.module.models import Auth, Users
bp = Blueprint('auth', __name__, url_prefix='/')

# sign up
@bp.route('/signup', methods=['GET'])
def signup_page():
    if session.get('user'): return render_template('index.html')
    return render_template('signup.html', data = None)

@bp.route('/signup', methods=['POST'])
def signup():
    user_data = request.form
    redata = user_data
    if Auth.query.filter_by(email=user_data['email']).first():
        return render_template('signup.html', error='此帳號已存在', data=user_data)
    if user_data['password'] != user_data['confirm-password']:
        return render_template('signup.html', error='密碼不一致', data=user_data)
    new_user = Users(
        name=user_data['username'],
        email=user_data['email'],
        sex=user_data['gender'],
        birthday=user_data['birthday']
    )
    new_user.save()
    new_auth = Auth(
        email=user_data['email'],
        password=user_data['password']
    )
    new_auth.save()
    return render_template('login.html')


@bp.route('/login', methods=['GET'])
def login_page():
    user = session.get('user')
    if user:return render_template('index.html')
    return render_template('login.html')

@bp.route('/login', methods=['POST'])
def login():
    user_data = request.form
    passwd_table = Auth.query.filter_by(email=user_data['email']).first()
    if not passwd_table: return render_template('login.html', error='此帳號不存在', email=user_data['email'])
    if not passwd_table.check_password(user_data['password']): return render_template('login.html', error='密碼錯誤', email=user_data['email'])
    user = Users.query.filter_by(email=user_data['email']).first()
    
    session['user'] = {
        'email': user.email,
        'name': user.name,
        'sex': user.sex,
        'birthday': user.birthday
    }

    return redirect('/')


@bp.route('/logout', methods=['GET'])
def logout_page():
    session.pop('user', None)
    session.pop('email', None)
    session.pop('username', None)
    return render_template('index.html')