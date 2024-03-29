from db import db
import users


def get_threads_on(subject_id):
    sql ="SELECT T.id, T.title, T.subject_id, COUNT(M.thread_id) AS message_count, T.user_id " \
        "FROM threads AS T LEFT JOIN messages AS M ON T.id=M.thread_id AND M.visible=True WHERE T.visible=TRUE " \
        "AND T.subject_id=:id GROUP BY T.id ORDER BY T.id"
    result = db.session.execute(sql, {"id":subject_id})
    return result.fetchall()

def get_threads(query:str, subject_id:int):
    sql = "SELECT * FROM threads WHERE title ILIKE :query AND subject_id=:id AND visible=TRUE"
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

def update(id, content):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql ="UPDATE threads SET title=:title WHERE id=:thread_id AND user_id=:user_id AND visible=TRUE"
    db.session.execute(sql, {"title":content, "thread_id":id, "user_id":user_id})
    db.session.commit()
    return True
    