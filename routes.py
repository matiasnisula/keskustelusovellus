from app import app
from flask import render_template, request, redirect, url_for, session
import messages, users, subjects, threads

@app.route("/")
def index():
    list = subjects.get_all()
    return render_template("index.html", subjects=list, subject_count=len(list),
                            text="Aiheiden määrä")


@app.route("/result" ,methods=["GET"])
def result():
    query = request.args["query"].strip()
    if query == "":
        return redirect("/")
    result_subjects = subjects.get_subjects(query)
    return render_template("index.html", subjects=result_subjects, subject_count=len(result_subjects),
                            text="Hakutulokset")


@app.route("/result/<int:subject_id>" ,methods=["GET"])
def result_threads(subject_id):
    query = request.args["query"].strip()
    if query == "":
        url = f"/subject/{subject_id}"
        return redirect(url)
    result_threads = threads.get_threads(query, subject_id)
    subject = subjects.get_title(subject_id)
    return render_template("threads.html", threads=result_threads, 
                            subject=subject[0], subject_id=subject_id, text=f"Hakutuloksia: {len(result_threads)}")


@app.route("/subject/<int:subject_id>", methods=["GET"])
def subject(subject_id):
    #Tämä yhdellä kyselyllä?
    list = threads.get_threads_on(subject_id)
    subject = subjects.get_title(subject_id)[0]
    return render_template("threads.html", threads=list, subject_id=subject_id, subject=subject)


@app.route("/subject", methods=["POST"])
def send_subject():
    subject = request.form["subject"].strip()
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    if subject == "":
        return render_template("index.html", error_message="Älä jätä kenttää tyhjäksi!")

    if subjects.save(subject):
        return redirect("/")
    else:
        return render_template("index.html", error_message="Aiheen lisääminen ei onnistunut")


@app.route("/subject/<int:subject_id>/<int:thread_id>", methods=["GET", "POST"])
def send_message(subject_id,thread_id):
    message_list = messages.get_list(thread_id)
    title = threads.get_title(thread_id)[0]
    if request.method == "GET":
        return render_template("messages.html", messages=message_list, title=title, 
                            subject_id=subject_id, thread_id=thread_id)
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        content = request.form["content"].strip()
        if content == "":
            return render_template("messages.html", messages=message_list, title=title, 
                            subject_id=subject_id, thread_id=thread_id, 
                            error_message="Viestikenttä oli tyhjä!")

        if messages.save(content, thread_id):
            url = f"/subject/{subject_id}/{thread_id}"
            return redirect(url)
        else:
            return render_template("messages.html", messages=message_list, title=title, 
                            subject_id=subject_id, thread_id=thread_id, 
                            error_message="Viestin lähettäminen epäonnistui!")


@app.route("/subject/<int:id>/newthread", methods=["GET","POST"])
def send_thread(id):
    if users.user_id() == 0:
            return render_template("newthread.html", id=id, error_message="Virhe: kirjaudu sisään lähettääksesi viesti!")
    if request.method == "GET":
        return render_template("newthread.html", id=id)
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        thread = request.form["title"].strip()
        if thread == "":
            return render_template("newthread.html", id=id, error_message="Virhe: viestikenttä oli tyhjä!")
        if threads.save(thread, id):
            return redirect("/subject/"+str(id))
        else:
            return render_template("newthread.html", id=id, error_message="Viestiketjun lisääminen epäonnistui")


@app.route("/delete/<int:subject_id>/<int:id>", methods=["GET"])
def delete_thread(subject_id, id):
    if threads.delete(id):
        return redirect("/subject/"+str(subject_id))
    else:
        return render_template("threads.html", error_message="Viestiketjun poistaminen epäonnistui")


@app.route("/deletemessage/<int:subject_id>/<int:thread_id>/<int:message_id>")
def delete_message(subject_id, thread_id, message_id):
    if messages.delete(message_id):
        url = f"/subject/{subject_id}/{thread_id}"
        return redirect(url)
    else:
        return render_template("messages.html", error_message="Viestin poisto epäonnistui")


@app.route("/update/<int:subject_id>/<int:thread_id>", methods=["GET", "POST"])
def update_thread(subject_id, thread_id):
    if request.method == "GET":
        content = threads.get_title(thread_id)[0]
        return render_template("updatethread.html", subject_id=subject_id, 
                                thread_id=thread_id, thread_content=content)
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        content = request.form["content"].strip()
        if content == "":
            return render_template("updatethread.html", subject_id=subject_id, 
                                    thread_id=thread_id,
                                    error_message="Virhe: Lomaketta ei voi lähettää tyhjänä")
        if threads.update(thread_id, content):
            url = f"/subject/{subject_id}"
            return redirect(url)
        else:
            return render_template("updatethread.html", subject_id=subject_id, 
                                    thread_id=thread_id,
                                    error_message="Virhe: Viestiketjun muokkaaminen epäonnistui")


@app.route("/update/<int:subject_id>/<int:thread_id>/<int:message_id>", methods=["GET", "POST"])
def update_message(subject_id, thread_id, message_id):
    if request.method == "GET":
        content = messages.get_message_content(message_id)[0]
        return render_template("updatemessage.html", subject_id=subject_id, thread_id=thread_id, 
                                message_id=message_id, message_content=content)
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        content = request.form["content"].strip()
        if content == "":
            return render_template("updatemessage.html", subject_id=subject_id, 
                                    thread_id=thread_id, message_id=message_id,
                                    error_message="Virhe: Lomaketta ei voi lähettää tyhjänä")
        if messages.update(message_id, thread_id, content):
            url = f"/subject/{subject_id}/{thread_id}"
            return redirect(url)
        else:
            return render_template("updatemessage.html", subject_id=subject_id, 
                                    thread_id=thread_id, message_id=message_id,
                                    error_message="Virhe: Viestin muokkaaminen epäonnistui")



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
            return render_template("login.html", error_message="Virhe: väärä tunnus tai salasana")


@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"].strip()
        password1 = request.form["password1"].strip()
        password2 = request.form["password2"].strip()
        if password1 != password2:
            return render_template("register.html", error_message="Virhe: salasanat eroavat")
        if username == "":
            return render_template("register.html", error_message="Virhe: syötä käyttäjätunnus")
        if password1 == "":
            return render_template("register.html", error_message="Virhe: syötä salasana")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("register.html", error_message="Virhe:: rekisteröinti ei onnistunut")