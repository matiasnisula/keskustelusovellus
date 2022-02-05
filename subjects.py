from db import db
import users


def get_all():
    sql = "SELECT id, title FROM subjects"
    result = db.session.execute(sql)
    return result.fetchall()

def get_title(id):
    sql = "SELECT title FROM subjects WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()

def save(title:str):
    user_id = users.user_id()
    if user_id == 0:
        return False
    try:
        sql = "INSERT INTO subjects (title) VALUES (:title)"
        db.session.execute(sql, {"title":title})
        db.session.commit()
    except:
        return False
    return True