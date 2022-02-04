from crypt import methods
from app import app
from flask import render_template, request, redirect
import messages, users, subjects, threads

@app.route("/")
def index():
    list = subjects.get_list()
    return render_template("index.html", subjects=list)

@app.route("/subject/<int:id>", methods=["GET"])
def subject(id):
    list = threads.get_list(id)
    return render_template("subject.html", threads=list, id=id)


@app.route("/subject", methods=["POST"])
def send_subject():
    subject = request.form["subject"]
    if subjects.save(subject):
        return redirect("/")
    else:
        return render_template("error.html", message="Aiheen lisääminen ei onnistunut")

@app.route("/subject/<int:subject_id>/<int:thread_id>", methods=["GET", "POST"])
def get_messages(subject_id,thread_id):
    message_list = messages.get_list(thread_id)
    return render_template("messages.html", messages=message_list, title=message_list[0][0])



@app.route("/subject/<int:id>/newthread", methods=["GET","POST"])
def send_thread(id):
    if request.method == "GET":
        return render_template("newthread.html", id=id)
    if request.method == "POST":
        title = request.form["title"]
        thread_id = threads.save_new(title, id)
        if thread_id != 0:
            message_content = request.form["content"]
            if messages.save_new(message_content, thread_id):
                return redirect("/subject/"+str(id))
        else:
            return render_template("error.html", message="Viestiketjun lisääminen epäonnistui")
    

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")