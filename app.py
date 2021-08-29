import re
from flask import Flask, render_template, request, session, redirect
import uuid, random, string

import requests
from database import database as db
import Auto


app = Flask(__name__)
app.secret_key = str(uuid.uuid4())
@app.route("/login")
def login():
    if isLogin(): return redirect("/")
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_process():
    id = request.form.get("id")
    pw = request.form.get("pw")
    query = db.select("panel", guild_id=id, password=pw)
    if query:
        session["login"] = id
        return redirect("/")
    return redirect("/login")

def isLogin():
    return True if session.get("login", False) else False
@app.route("/name/<id>")
def _name(id):
    if not isLogin(): return "Login Please"
    query = db.select("product", guild_id=session.get("login", ""), id=id)
    if query:
        p = request.args.get("name", "0")
        db.update("product","name", p, guild_id=session.get("login", ""), id=id)

        return "성공적으로 변경되었습니다."
    return "ERROR"
@app.route("/addStock/<id>", methods=["POST"])
def addStock(id):
    if not isLogin(): return "Login Please"
    query = db.select("product", guild_id=session.get("login", ""), id=id)
    if query:
        p = request.form.get("value", "")   
        for i in p.split("\n"):
            if i.strip() == "": continue
            query = db.select("stock", guild_id=session.get("login", ""), product_id=id, value=i)
            if not query:
                db.insert("stock", guild_id=session.get("login", ""), product_id=id, value=i)
        return "성공적으로 추가되었습니다."
    return "ERROR"
@app.route("/role", methods=["POST"])
def role(id):
    if not isLogin(): return "Login Please"
    query = db.select("role", guild_id=session.get("login"))
    if query:
        db.update("role", "value", request.form.get("val"), guild_id=session.get("login"))
    else:
        db.insert("role", value=request.form.get("val"), guild_id=session.get("login"))
    return "성공적으로 변경되었습니다."
@app.route("/webhook", methods=["POST"])
def webhook(id):
    if not isLogin(): return "Login Please"
    query = db.select("webhook", guild_id=session.get("login"))
    if query:
        db.update("webhook", "purlog", request.form.get("pur"), guild_id=session.get("login"))
        db.update("webhook", "admlog", request.form.get("adm"), guild_id=session.get("login"))
    else:
        db.insert("webhook", purlog=request.form.get("pur"), admlog=request.form.get("adm"), guild_id=session.get("login"))
    return "성공적으로 변경되었습니다."
@app.route("/amount/<id>")
def amount_(id):
    if not isLogin(): return "Login Please"
    query = db.select("users", guild_id=session.get("login", ""), user_id=id)
    if query:
        p = request.args.get("amount", "0")
        if not p.isdigit(): return "Digit Only"
        db.update("users","amount", p, guild_id=session.get("login", ""),user_id=id)

        return "성공적으로 변경되었습니다."
    return "ERROR"
@app.route("/raw/<id>")
def raw(id):
    
    query = db.select("raw", id=id)
    text = ""
    for i in query:
        text += f"{i[1]}<br>\n"
    return text
@app.route("/culture", methods=["POST"])
def culture_():
    if not isLogin(): return "Login Please"
    _, message, token = Auto.CulturelandGetToken(request.form.get("id"), request.form.get("pw"))
    query = db.select("culture", guild_id=session.get("login", ""))
    if query:
        db.update("culture", "token", token, guild_id=session.get("login", ""))
    else:
        db.insert("culture", token=token, guild_id=session.get("login", ""))
    return message
@app.route("/price/<id>")
def price(id):
    if not isLogin(): return "Login Please"
    query = db.select("product", guild_id=session.get("login", ""), id=id)
    if query:
        p = request.args.get("price", "0")
        if not p.isdigit(): return "Digit Only"
        db.update("product","price", p, guild_id=session.get("login", ""), id=id)

        return "성공적으로 변경되었습니다."
    return "ERROR"
@app.route("/delStock/<id>")
def delStock(id):
    if not isLogin(): return "Login Please"
    db.delete("stock", guild_id=session.get("login", ""), product_id=id, value=request.args.get("name"))
    return "성공적으로 삭제되었습니다."
@app.route("/del/<id>")
def _del(id):
    if not isLogin(): return "Login Please"
    query = db.select("product", guild_id=session.get("login", ""), id=id)
    if query:
        db.delete("product", guild_id=session.get("login", ""), id=id)

        return "성공적으로 삭제되었습니다."
    return "ERROR"
@app.route("/create")
def create():
    if not isLogin(): return redirect("/login")
    st = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(20))
    db.insert("product", guild_id=session.get("login", ""), id=st, name=st, price="0")
    return "성공적으로 생성되었습니다."
@app.route("/product/<id>")
def product(id):
    if not isLogin(): return redirect("/login")
    query = db.select("product", guild_id=session.get("login", ""), id=id)
    if query:
        stock_query = db.select("stock", guild_id=session.get("login", ""), product_id=id)
        product_query = db.select("product", guild_id=session.get("login", ""))
        users_query = db.select("users", guild_id=session.get("login", ""))
        
        role_query = db.select("role", guild_id=session.get("login", ""))
        role_query = role_query if role_query else [0, ""]
        logs_query = db.select("webhook", guild_id=session.get("login", ""))
        logs_query = logs_query if logs_query else [0, "", ""]
        return render_template("index.html", product=query[0], stock=stock_query,tf="product", product_query=product_query, users_query=users_query,role_query=role_query, logs_query=logs_query)
    return redirect("/")
@app.route("/")
def index():
    if not isLogin(): return redirect("/login")
    product_query = db.select("product", guild_id=session.get("login", ""))
    users_query = db.select("users", guild_id=session.get("login", ""))
    role_query = db.select("role", guild_id=session.get("login", ""))
    role_query = role_query if role_query else [0, ""]
    logs_query = db.select("webhook", guild_id=session.get("login", ""))
    logs_query = logs_query if logs_query else [0, "", ""]
    return render_template("index.html", product_query=product_query, users_query=users_query, tf="None",role_query=role_query, logs_query=logs_query)

app.run("0.0.0.0", 80)