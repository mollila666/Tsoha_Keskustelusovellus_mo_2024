import os
from db import db
from flask import abort, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text


def login(name, password):
    sql = "SELECT password, id, role FROM users WHERE name='%s'" %name
    result = db.session.execute(text(sql))
    user = result.fetchone()
    if not user:
        return False
    if not check_password_hash(user[0], password):
        return False
    session["user_id"] = user[1]
    session["user_name"] = name
    session["user_role"] = user[2]
    session["csrf_token"] = os.urandom(16).hex()
    return True

def logout():
    del session["user_id"]
    del session["user_name"]
    del session["user_role"]

def register(name, password, role):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (name, password, role) VALUES ('%s', '%s', %s)" %(name, hash_value, str(role))
        db.session.execute(text(sql))
        db.session.commit()
    except:
        return False
    return login(name, password)

def user_id():
    return session.get("user_id", 0)

def require_role(role):
    if role > session.get("user_role", 0):
        abort(403)

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)