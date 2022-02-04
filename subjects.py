from db import db
import users


def get_list():
    sql = "SELECT * FROM subjects"
    result = db.session.execute(sql)
    return result.fetchall()

def save(title:str):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO subjects (title) VALUES (:title)"
    db.session.execute(sql, {"title":title})
    db.session.commit()
    return True