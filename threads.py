from db import db
import users

def get_all_threads():
    sql = "SELECT * FROM threads"
    result = db.session.execute(sql)
    return result.fetchall()

def get_threads_on(subject_id):
    sql ="SELECT * FROM threads WHERE subject_id=:id AND visible=TRUE"
    result = db.session.execute(sql, {"id":subject_id})
    return result.fetchall()

def get_threads(query:str, subject_id:int):
    sql = "SELECT * FROM threads WHERE title ILIKE :query AND subject_id=:id AND visible=True"
    result = db.session.execute(sql, {"query":"%"+query+"%", "id":subject_id})
    return result.fetchall()


def get_title(thread_id):
    sql = "SELECT title FROM threads WHERE id=:id"
    result = db.session.execute(sql, {"id":thread_id})
    return result.fetchone()

def save(title, subject_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO threads (title, subject_id, user_id, visible) VALUES " \
          "(:title, :subject_id, :user_id, :visible)"
    db.session.execute(sql, {"title":title, "subject_id":subject_id, 
                        "user_id":user_id, "visible":True})
    db.session.commit()
    return True

def delete(id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "UPDATE threads SET visible=FALSE WHERE id=:id AND user_id=:user_id"
    db.session.execute(sql, {"id":id, "user_id":user_id})
    db.session.commit()
    return True
    