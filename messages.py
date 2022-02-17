from db import db
import users


def get_list(thread_id):
    sql = "SELECT id, content, sent_at, user_id FROM messages WHERE thread_id=:id " \
        "AND visible=TRUE"
    result = db.session.execute(sql, {"id":thread_id})
    return result.fetchall()


def save(content, thread_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO messages (content, user_id, thread_id, sent_at, visible) " \
        "VALUES (:content, :user_id, :thread_id, NOW(), :visible)"
    db.session.execute(sql, {"content":content, "user_id":user_id, 
                        "thread_id":thread_id, "visible":True})
    db.session.commit()
    return True

def delete(id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "UPDATE messages SET visible=FALSE WHERE id=:id AND user_id=:user_id"
    db.session.execute(sql, {"id":id, "user_id":user_id})
    db.session.commit()
    return True