"""
模組名稱: auth.py
模組描述: 負責使用者驗證與設定相關的功能，包括註冊、登入、登出以及修改使用者資料。
依賴模組: os, flask, werkzeug, app.module.controller.util, app.module.models, app
"""

import os
from flask import Blueprint, flash, render_template, redirect, session, request, url_for
from app.module.util.validators import allowed_file, check_login
from app.module.models import Auth, Users
from werkzeug.utils import secure_filename
from app import app

# 建立 Blueprint 對象，負責管理與身份驗證相關的路由
bp = Blueprint('auth', __name__, url_prefix='/')

# 註冊頁面
@bp.route('/signup', methods=['GET'])
def signup_page():
    """
    功能: 渲染註冊頁面。如果已登入，將重定向到首頁。
    回傳值: HTML 頁面。
    """
    if session.get('user'):
        return redirect('/')
    return render_template('signup.html', data=None)

# 處理註冊請求
@bp.route('/signup', methods=['POST'])
def signup():
    """
    功能: 處理使用者註冊表單的提交，檢查是否有錯誤並建立新帳號。
    回傳值: 成功重定向至登入頁面，失敗渲染註冊頁面並顯示錯誤訊息。
    """
    user_data = request.form
    if Auth.query.filter_by(email=user_data['email']).first():
        return render_template('signup.html', error='此帳號已存在', data=user_data)
    if user_data['password'] != user_data['confirm-password']:
        return render_template('signup.html', error='密碼不一致', data=user_data)
    
    new_user = Users(
        name=user_data['username'],
        email=user_data['email'],
        gender=user_data['gender'],
        birthday=user_data['birthday'],
        stream_hash= f"stream{abs(hash(user_data['email']))}"
    )
    new_user.save()
    new_auth = Auth(
        email=user_data['email'],
        password=user_data['password']
    )
    new_auth.save()
    return redirect('/login')

# 登入頁面
@bp.route('/login', methods=['GET'])
def login_page():
    """
    功能: 渲染登入頁面。如果已登入，將重定向至首頁。
    回傳值: HTML 頁面。
    """
    if session.get('user'):
        return redirect('/')
    if next_page := request.args.get('next'):
        return render_template('login.html', next=next_page)
    return render_template('login.html')

# 處理登入請求
@bp.route('/login', methods=['POST'])
def login():
    """
    功能: 處理使用者登入表單的提交，檢查帳號和密碼是否正確。
    回傳值: 成功重定向至指定頁面或首頁，失敗渲染登入頁面並顯示錯誤訊息。
    """
    user_data = request.form
    passwd_table = Auth.query.filter_by(email=user_data['email']).first()
    next_page = request.args.get('next')
    if not passwd_table:
        return render_template('login.html', error='此帳號不存在', email=user_data['email'])
    if not passwd_table.check_password(user_data['password']):
        return render_template('login.html', error='密碼錯誤', email=user_data['email'])
    
    user = Users.query.filter_by(email=user_data['email']).first()
    session['user'] = {
        'email': user.email,
        'name': user.name,
        'gender': user.gender,
        'birthday': user.birthday,
        'stream_hash': user.stream_hash
    }
    return redirect(next_page) if next_page else redirect('/')

# 登出
@bp.route('/logout', methods=['GET'])
def logout_page():
    """
    功能: 處理使用者登出並清除 Session 資料。
    回傳值: 重定向至首頁。
    """
    session.pop('user', None)
    session.pop('email', None)
    session.pop('username', None)
    return redirect('/')

# 修改使用者資料頁面
@bp.route('/settings', methods=['GET'])
@check_login
def setting_page(user):
    """
    功能: 渲染使用者資料設定頁面，需登入驗證。
    參數:
        user (dict): 當前使用者的 Session 資料。
    回傳值: HTML 頁面。
    """
    user = Users.query.filter_by(email=user['email']).first()
    return render_template('setting.html', user=user)

def ensure_upload_folder_exists():
    """
    功能: 確保上傳資料夾存在，若不存在則建立。
    """
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

# 處理設定更新請求
@bp.route('/update_settings', methods=['POST'])
def settings():
    """
    功能: 處理使用者更新資料的表單提交，包含檔案上傳處理。
    回傳值: 成功重定向至設定頁面，失敗渲染設定頁面。
    """
    if request.method != 'POST':
        return render_template('setting.html', user=user)
    name = request.form['name']
    email = request.form['email']
    user = Users.query.filter_by(email=email).first()
    avatar = None
    if 'avatar' in request.files:
        file = request.files['avatar']
        if file and allowed_file(file.filename):
            filename = secure_filename(f"{user.id}-{file.filename}")
            avatar = filename
            ensure_upload_folder_exists()
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    user.email = email
    user.name = name
    if avatar:
        user.avatar = filename
    user.save()
    flash('設定已更新', 'success')
    return redirect(url_for('auth.setting_page'))
