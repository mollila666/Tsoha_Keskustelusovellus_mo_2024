from app import app
from flask import render_template, request, redirect
import threads
import users


@app.route("/")
def index():
    return render_template("index.html", areas=threads.get_all_areas())

@app.route("/login", methods=["get", "post"])
def login():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not users.login(username, password):
            return render_template("error.html", message="Väärä tunnus tai salasana")
        return redirect("/")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["get", "post"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        if len(username) < 1 or len(username) > 20:
            return render_template("error.html", message="Tunnuksessa tulee olla 1-20 merkkiä")

        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if password1 == "":
            return render_template("error.html", message="Salasana on tyhjä")

        role = request.form["role"]
        if role not in ("1", "2"):
            return render_template("error.html", message="Tuntematon käyttäjärooli")

        if threads.check_users(username) > 0:
            return render_template("error.html", message="Tunnus on jo käytössä, valitse toinen tunnus")

        if not users.register(username, password1, role):
            print(username)
            print(password1)
            print(role)
            return render_template("error.html", message="Rekisteröinti ei onnistunut")
        return redirect("/")

@app.route("/area/<int:area_id>")
def show_area(area_id):
    info = threads.get_area_info(area_id)
    all_chains = threads.get_all_chains(area_id)
    return render_template("area.html", id=area_id, name=info, chains=all_chains)


@app.route("/create_chain", methods=["post"])
def create_new_chain():
    area_id = request.form["area_id"]
    chain = request.form["chain"]
    content = request.form["content"]
    if len(chain.replace(' ','')) == 0:
        return render_template("error.html", message="Uudella ketjulla pitää olla nimi!", areaid=area_id)
    if len(chain.replace(' ','')) > 200:
        return render_template("error.html", message="Uuden ketjun nimessä on liian monta merkkiä, maksimi on 200!", areaid=area_id)
    if len(content.replace(' ','')) == 0:
        return render_template("error.html", message="Viesti ei saa olla tyhjä, kirjoita viesti!", areaid=area_id)
    if len(content.replace(' ','')) > 1000:
        return render_template("error.html", message="Viesti ei saa olla liian pitkä, maksimi on 1000 merkkiä!", areaid=area_id)
    threads.add_area(area_id,chain,content)
    address="/area/%s" %area_id
    return redirect(address)

@app.route("/chain/<int:chain_id>")
def select_chain(chain_id):
    all_messages = threads.get_all_messages(chain_id)
    chain_name = threads.get_chain_name(chain_id)
    area_id = threads.get_area_id(chain_id)
    return render_template("select_chain.html", id=chain_id, messages=all_messages, name=chain_name[0],area_id=area_id)

@app.route("/create_message", methods=["post"])
def create_new_message():
    chain_id = request.form["chain_id"]
    message = request.form["Message"]
    if len(message.replace(' ','')) == 0:
        return render_template("error.html", message="Viesti ei saa olla tyhjä, kirjoita viesti uudelleen!", areaid=chain_id)
    if len(message.replace(' ','')) > 1000:
        return render_template("error.html", message="Uusi viesti ei saa olla liian pitkä, maksimi on 1000 merkkiä!", areaid=chain_id)
    threads.add_message(chain_id,message)
    address="/chain/%s" %chain_id
    return redirect(address)

@app.route("/admin")
def admin_tools():
    all_areas=threads.get_areas()
    all_users=threads.get_users()
    return render_template("admin.html",areas=all_areas, users=all_users)

@app.route("/create_area", methods=["post"])
def create_new_area():
    area_name = request.form["area_name"]
    if threads.check_areas(area_name) > 0:
        return render_template("error.html", message="Alueen nimi on jo käytössä, valitse toinen nimi alueelle")
    if len(area_name.replace(' ','')) == 0:
        return render_template("error.html", message="Alueen nimessä pitää olla vähintään 1 merkki!")
    if len(area_name.replace(' ','')) > 200:
        return render_template("error.html", message="Alueen nimessä on liian monta merkkiä, maksimi on 200!")
    threads.add_new_area(area_name)
    return redirect("/")

@app.route("/delete_area", methods=["post"])
def delete_old_area():
    area_name = request.form["area_name"]
    threads.delete_area(area_name)
    return redirect("/")

@app.route("/search_message", methods=["post"])
def search_messages():
    key_word = request.form["key_word"]
    found_messages=threads.search_messages(key_word)
    return render_template("search.html",messages=found_messages, keyword=key_word)

@app.route("/create_private_area", methods=["post"])
def create_private_areas():
    area_name = request.form["area_name"]
    user_name=request.form.getlist('users')
    if threads.check_areas(area_name) > 0:
        return render_template("error.html", message="Alueen nimi on jo käytössä, valitse toinen nimi alueelle")
    if len(area_name.replace(' ','')) == 0:
        return render_template("error.html", message="Alueen nimessä pitää olla vähintään 1 merkki!")
    if len(user_name) == 0:
        return render_template("error.html", message="Valitse vähintään 1 käyttäjä!")
    threads.add_private_area(area_name,user_name)
    return redirect("/")

@app.route("/owndata")
def own_data():
    all_chains_messages=threads.get_chains_messages()
    return render_template("owndata.html", owndata=all_chains_messages)

@app.route("/editchain/<int:chain_id>")
def rename_chain(chain_id):
    chain_name = threads.get_chain_name(chain_id)
    return render_template("edit_chain.html", id=chain_id, name=chain_name[0])

@app.route("/rename_chain", methods=["post"])
def rename_delete_chain():
    chainid = request.form["chain_id"]
    chain_name = threads.get_chain_name(chainid)
    newname=request.form["new_name"]
    delete_chain=request.form["tuhoa"]
    if len(newname.replace(' ','')) == 0:
        return render_template("error.html", message="Muokattu ketjun nimi ei saa olla tyhjä, kirjoita nimi uudelleen!", areaid=chainid)
    if len(newname.replace(' ','')) > 200:
        return render_template("error.html", message="Muokattu ketjun nimi ei saa olla liian pitkä, maksimi 200 merkkiä!", areaid=chainid)
    if newname != chain_name[0]:
        threads.mod_delete_chain(chainid,newname)
    if delete_chain == '1':
        threads.delete_chain(chainid)
    return redirect("/owndata")

@app.route("/editmessage/<int:message_id>")
def rename_message(message_id):
    message_name = threads.get_message_name(message_id)
    return render_template("edit_message.html", id=message_id, name=message_name[0])

@app.route("/rename_message", methods=["post"])
def rename_delete_message():
    messageid = request.form["message_id"]
    message_name = threads.get_message_name(messageid)
    newname=request.form["new_name"]
    delete_message=request.form["tuhoa"]
    if len(newname.replace(' ','')) == 0:
        return render_template("error.html", message="Muokattu viesti ei saa olla tyhjä, kirjoita viesti uudelleen!", areaid=messageid)
    if len(newname.replace(' ','')) > 1000:
        return render_template("error.html", message="Muokattu viesti ei saa olla liian pitkä, maksimi 1000 merkkiä!", areaid=messageid)
    if newname != message_name[0]:
        threads.mod_delete_message(messageid,newname)
    if delete_message == '1':
        threads.delete_message(messageid)
    return redirect("/owndata")
