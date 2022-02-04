from sqlalchemy import true
from db import db
import users

def get_list():
    sql = "SELECT * FROM threads"
    result = db.session.execute(sql)
    return result.fetchall()

def get_list(subject_id):
    sql ="SELECT * FROM threads WHERE subject_id=:id"
    result = db.session.execute(sql, {"id":subject_id})
    return result.fetchall()

#Palauttaa lisätyn keskusteluketjun id-numeron
def save_new(title, subject_id):
    user_id = users.user_id()
    if user_id == 0:
        return 0
    sql = "INSERT INTO threads (title, subject_id, user_id) VALUES " \
          "(:title, :subject_id, :user_id) RETURNING id"
    result = db.session.execute(sql, {"title":title, "subject_id":subject_id, "user_id":user_id})
    thread_id = result.fetchone()[0]
    db.session.commit()
    return thread_id
    