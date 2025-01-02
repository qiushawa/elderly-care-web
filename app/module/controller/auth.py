import os
from flask import Blueprint, flash, render_template, redirect, session, request, url_for
from app.module.controller.util import allowed_file, check_login
from app.module.models import Auth, Users
from werkzeug.utils import secure_filename
from app import app

bp = Blueprint('auth', __name__, url_prefix='/')

# 註冊頁面
@bp.route('/signup', methods=['GET'])
def signup_page():
    if session.get('user'):
        return redirect('/')
    return render_template('signup.html', data=None)

# 處理註冊請求
@bp.route('/signup', methods=['POST'])
def signup():
    user_data = request.form
    # 檢查帳號是否已存在
    if Auth.query.filter_by(email=user_data['email']).first():
        return render_template('signup.html', error='此帳號已存在', data=user_data)
    # 檢查密碼是否一致
    if user_data['password'] != user_data['confirm-password']:
        return render_template('signup.html', error='密碼不一致', data=user_data)
    
    # 建立新使用者
    new_user = Users(
        name=user_data['username'],
        email=user_data['email'],
        gender=user_data['gender'],
        birthday=user_data['birthday']
    )
    new_user.save()
    
    # 建立新帳號
    new_auth = Auth(
        email=user_data['email'],
        password=user_data['password']
    )
    new_auth.save()
    
    return redirect('/login')

# 登入頁面
@bp.route('/login', methods=['GET'])
def login_page():
    if session.get('user'):
        return redirect('/')
    
    next_page = request.args.get('next')
    if next_page:
        return render_template('login.html', next=next_page)
    return render_template('login.html')

# 處理登入請求
@bp.route('/login', methods=['POST'])
def login():
    user_data = request.form
    passwd_table = Auth.query.filter_by(email=user_data['email']).first()
    next_page = request.args.get('next')
    # 檢查帳號是否存在
    if not passwd_table:
        return render_template('login.html', error='此帳號不存在', email=user_data['email'])
    # 檢查密碼是否正確
    if not passwd_table.check_password(user_data['password']):
        return render_template('login.html', error='密碼錯誤', email=user_data['email'])
    
    user = Users.query.filter_by(email=user_data['email']).first()
    session['user'] = {
        'email': user.email,
        'name': user.name,
        'gender': user.gender,
        'birthday': user.birthday
    }
    
    if next_page:
        return redirect(next_page)
    return redirect('/')

# 登出
@bp.route('/logout', methods=['GET'])
def logout_page():
    session.pop('user', None)
    session.pop('email', None)
    session.pop('username', None)
    return redirect('/')

# 修改使用者資料 seeting page
@bp.route('/settings', methods=['GET'])
@check_login
def setting_page(user):
    user = Users.query.filter_by(email=user['email']).first()
    return render_template('setting.html', user=user)

def ensure_upload_folder_exists():
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

@bp.route('/update_settings', methods=['POST'])
def settings():
    if request.method == 'POST':
        # 取得表單資料
        name = request.form['name']
        email = request.form['email']
        user = Users.query.filter_by(email=email).first()
        # 處理頭像檔案上傳
        avatar = None
        if 'avatar' in request.files:
            file = request.files['avatar']
            if file and allowed_file(file.filename):
                # 確保檔案名安全
                filename = secure_filename(f"{user.id}-{file.filename}")
                avatar = filename  # 這會在後續保存檔案

                # 確保上傳資料夾存在
                ensure_upload_folder_exists()

                # 儲存檔案
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # 更新資料庫
        user.email = email
        user.name = name
        if avatar:
            user.avatar = filename
        user.save()

        # 成功訊息
        flash('設定已更新', 'success')
        return redirect(url_for('auth.setting_page'))

    return render_template('setting.html', user=user)
