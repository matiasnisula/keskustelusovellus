from db import db
import users


def get_list(thread_id):
    sql = "SELECT content , sent_at FROM messages WHERE thread_id=" + str(thread_id)
    result = db.session.execute(sql)
    return result.fetchall()


def save_new(content, thread_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO messages (content, user_id, thread_id, sent_at) " \
        "VALUES (:content, :user_id, :thread_id, NOW())"
    db.session.execute(sql, {"content":content, "user_id":user_id, "thread_id":thread_id})
    db.session.commit()
    return True