from flask import request, jsonify, render_template
from app import app
from app.module.controller import docs, devices, users, update, user_html

# app 公用變數
app.register_blueprint(users.bp)
app.register_blueprint(devices.bp)
app.register_blueprint(docs.bp)
app.register_blueprint(update.bp)
app.register_blueprint(user_html.bp)