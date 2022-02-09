from db import db
import users

def get_all_threads():
    sql = "SELECT * FROM threads"
    result = db.session.execute(sql)
    return result.fetchall()

def get_threads_on(subject_id):
    sql ="SELECT * FROM threads WHERE subject_id=:id"
    result = db.session.execute(sql, {"id":subject_id})
    return result.fetchall()

def get_title(thread_id):
    sql = "SELECT title FROM threads WHERE id=:id"
    result = db.session.execute(sql, {"id":thread_id})
    return result.fetchone()

def save_new(title, subject_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO threads (title, subject_id, user_id) VALUES " \
          "(:title, :subject_id, :user_id)"
    db.session.execute(sql, {"title":title, "subject_id":subject_id, "user_id":user_id})
    db.session.commit()
    return True
    