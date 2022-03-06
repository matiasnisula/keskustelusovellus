from db import db
import users


def get_list(thread_id):
    sql = "SELECT M.id AS id, M.content AS content, M.sent_at AS sent_at, " \
        "U.username AS username, M.user_id AS user_id FROM messages AS M, users AS U " \
        "WHERE M.thread_id=:id AND M.visible=TRUE AND M.user_id=U.id"
    result = db.session.execute(sql, {"id":thread_id})
    return result.fetchall()

def get_message_content(id):
    sql = "SELECT content FROM messages WHERE id=:id AND visible=TRUE"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()


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

def update(id, thread_id, content):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "UPDATE messages SET content=:content WHERE id=:id AND user_id=:user_id " \
        "AND thread_id=:thread_id AND visible=TRUE"
    db.session.execute(sql, {"content":content, "id":id, "user_id":user_id, "thread_id":thread_id})
    db.session.commit()
    return True
