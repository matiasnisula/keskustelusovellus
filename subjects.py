from db import db
import users


def get_all():
    sql = "SELECT S.id, S.title, COUNT(T.subject_id) AS thread_count FROM subjects AS S LEFT JOIN threads AS T " \
        "ON S.id=T.subject_id AND T.visible=TRUE GROUP BY S.id ORDER BY S.id;"
    result = db.session.execute(sql)
    return result.fetchall()


def get_title(id):
    sql = "SELECT title FROM subjects WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()

def get_subjects(query:str):
    sql = "SELECT id, title FROM subjects WHERE title ILIKE :query"
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    return result.fetchall()

def save(title:str):
    user_id = users.user_id()
    if user_id == 0:
        return False
    try:
        sql = "INSERT INTO subjects (title, user_id) VALUES (:title, :user_id)"
        db.session.execute(sql, {"title":title, "user_id":user_id})
        db.session.commit()
    except:
        return False
    return True