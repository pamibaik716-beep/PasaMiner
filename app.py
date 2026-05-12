# =========================================
# PASAMINER GOLD PREMIUM
# FULL FINAL VERSION
# =========================================

from flask import Flask, render_template_string, request, redirect, session
from pymongo import MongoClient
from bson.objectid import ObjectId
import random
import time

app = Flask(__name__)

# =========================================
# SECRET
# =========================================

app.secret_key = "GANTI_SECRET_KEY"

# =========================================
# ADMIN LOGIN
# =========================================

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# =========================================
# MONGODB
# =========================================

MONGO_URL = "mongodb://pasaminergold:M12pami*@ac-gpow4zl-shard-00-00.gnxeyyz.mongodb.net:27017,ac-gpow4zl-shard-00-01.gnxeyyz.mongodb.net:27017,ac-gpow4zl-shard-00-02.gnxeyyz.mongodb.net:27017/?ssl=true&replicaSet=atlas-oy6uk4-shard-0&authSource=admin&appName=Cluster0"

client = MongoClient(MONGO_URL)

db = client["pasaminer"]

users = db["users"]
withdraws = db["withdraws"]

# =========================================
# ADS
# =========================================

ADS_LINK = "https://www.profitablecpmratenetwork.com/f76dmpngae?key=edb1a0763db2101358b5ab3a74a3ca24"

ADSTERRA_SCRIPT = """
<script type="text/javascript" src="https://pl29422289.profitablecpmratenetwork.com/cd/89/9b/cd899b6c6eb0a17bd6a09930a0311ea5.js"></script>
"""

# =========================================
# CONFIG
# =========================================

LOGO = "https://files.catbox.moe/8m6l6p.png"

DAILY_REWARD = 100

# =========================================
# RANK
# =========================================

def get_rank(gold):

    if gold >= 10000:
        return "💎 Diamond"

    if gold >= 5000:
        return "🥇 Gold"

    if gold >= 1000:
        return "🥈 Silver"

    return "🥉 Bronze"

# =========================================
# MAIN HTML
# =========================================

HTML = '''

<!DOCTYPE html>
<html>

<head>

<title>PasaMiner Gold</title>

<meta name="viewport"
content="width=device-width, initial-scale=1">

<style>

body{
background:#0f0f0f;
font-family:Arial;
color:white;
padding:15px;
}

.box{
background:#1c1c1c;
padding:20px;
border-radius:20px;
margin-bottom:15px;
}

.logo{
width:120px;
border-radius:50%;
display:block;
margin:auto;
margin-bottom:10px;
}

.title{
text-align:center;
font-size:28px;
font-weight:bold;
color:gold;
margin-bottom:15px;
}

.stat{
background:#2a2a2a;
padding:12px;
border-radius:12px;
margin-top:8px;
}

button{
width:100%;
padding:14px;
border:none;
border-radius:12px;
background:gold;
font-weight:bold;
margin-top:10px;
cursor:pointer;
}

input{
width:95%;
padding:12px;
border:none;
border-radius:10px;
background:#333;
color:white;
margin-top:10px;
}

.leader{
background:#222;
padding:10px;
border-radius:10px;
margin-top:5px;
}

a{
text-decoration:none;
}

</style>

</head>

<body>

<div class="box">

<img src="{{logo}}" class="logo">

<div class="title">
PasaMiner Gold
</div>

{% if not user %}

<form method="POST">

<input type="text"
name="username"
placeholder="Username"
required>

<input type="password"
name="password"
placeholder="Password"
required>

<button type="submit">
LOGIN / REGISTER
</button>

</form>

{% else %}

<div class="stat">
🏅 Rank : {{rank}}
</div>

<div class="stat">
🪙 Gold : {{user.gold}}
</div>

<div class="stat">
💰 Balance : Rp {{user.balance}}
</div>

<div class="stat">
⚡ Power : {{user.power}}
</div>

<div class="stat">
👑 VIP : {{user.vip}}
</div>

<div class="stat">
👥 Referral : {{user.ref_total}}
</div>

<form action="/mine" method="POST">
<button>
⛏ Mine Gold
</button>
</form>

<a href="/claim">
<button>
🎁 Claim Reward
</button>
</a>

<a href="/watchads">
<button>
📺 Watch Ads
</button>
</a>

<form action="/daily" method="POST">
<button>
📅 Daily Reward
</button>
</form>

<form action="/recharge" method="POST">
<button>
🔋 Recharge Power
</button>
</form>

<form action="/withdraw" method="POST">

<input type="text"
name="wallet"
placeholder="Dana / OVO / Gopay"
required>

<input type="number"
name="amount"
placeholder="Jumlah Withdraw"
required>

<button>
💸 Withdraw
</button>

</form>

<h3>👑 VIP LEVEL</h3>

<a href="/vip/1">
<button>VIP 1</button>
</a>

<a href="/vip/2">
<button>VIP 2</button>
</a>

<a href="/vip/3">
<button>VIP 3</button>
</a>

<h3>👥 Referral</h3>

<input value="{{ref}}" readonly>

<h3>🏆 Leaderboard Referral</h3>

{% for x in top_ref %}

<div class="leader">
{{x.username}} - {{x.ref_total}} Ref
</div>

{% endfor %}

<h3>📜 Withdraw History</h3>

{% for wd in history %}

<div class="leader">

Rp {{wd.amount}} -
{{wd.status}}

</div>

{% endfor %}

<br>

<a href="/logout">
<button>
Logout
</button>
</a>

{% endif %}

</div>

{{ads_script|safe}}

</body>
</html>

'''

# =========================================
# ADMIN LOGIN HTML
# =========================================

ADMIN_LOGIN = '''

<body style="
background:#111;
font-family:Arial;
padding:20px;
color:white;
">

<h1>Admin Login</h1>

<form method="POST">

<input type="text"
name="username"
placeholder="Username">

<input type="password"
name="password"
placeholder="Password">

<button>
LOGIN
</button>

</form>

</body>

'''

# =========================================
# ADMIN PANEL HTML
# =========================================

ADMIN_HTML = '''

<body style="
background:#111;
font-family:Arial;
padding:20px;
color:white;
">

<h1>ADMIN PANEL</h1>

<a href="/admin-logout">
<button>Logout Admin</button>
</a>

{% for wd in data %}

<div style="
background:#222;
padding:15px;
border-radius:15px;
margin-top:10px;
">

<p>User : {{wd.username}}</p>

<p>Wallet : {{wd.wallet}}</p>

<p>Amount : {{wd.amount}}</p>

<p>Status : {{wd.status}}</p>

<a href="/approve/{{wd._id}}">
<button style="
background:green;
color:white;
">
Approve
</button>
</a>

<a href="/reject/{{wd._id}}">
<button style="
background:red;
color:white;
">
Reject
</button>
</a>

</div>

{% endfor %}

</body>

'''

# =========================================
# LOGIN REGISTER
# =========================================

@app.route("/", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = users.find_one({
            "username": username
        })

        # LOGIN
        if user:

            if user["password"] == password:

                session["user"] = username

                return redirect("/dashboard")

            return "Password salah"

        # REGISTER
        ref = request.args.get("ref")

        users.insert_one({

            "username": username,
            "password": password,

            "gold": 0,
            "balance": 0,

            "power": 100,

            "vip": 0,

            "ref_total": 0,

            "last_daily": 0,

            "last_ads": 0,

            "last_claim": 0,

            "ref_by": ref

        })

        # BONUS REFERRAL
        if ref:

            users.update_one(
                {"username": ref},
                {
                    "$inc":{
                        "balance":100,
                        "ref_total":1
                    }
                }
            )

        session["user"] = username

        return redirect("/dashboard")

    return render_template_string(
        HTML,
        user=None,
        logo=LOGO,
        ads_script=ADSTERRA_SCRIPT
    )

# =========================================
# DASHBOARD
# =========================================

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/")

    user = users.find_one({
        "username": session["user"]
    })

    rank = get_rank(user["gold"])

    ref = request.host_url + "?ref=" + user["username"]

    top_ref = users.find().sort(
        "ref_total",-1
    ).limit(10)

    history = withdraws.find({
        "username": session["user"]
    }).sort("_id",-1)

    return render_template_string(
        HTML,
        user=user,
        logo=LOGO,
        rank=rank,
        ref=ref,
        top_ref=top_ref,
        history=history,
        ads_script=ADSTERRA_SCRIPT
    )

# =========================================
# MINE
# =========================================

@app.route("/mine", methods=["POST"])
def mine():

    if "user" not in session:
        return redirect("/")

    user = users.find_one({
        "username": session["user"]
    })

    if user["power"] >= 5:

        gold = random.randint(5,15)

        users.update_one(
            {"username": session["user"]},
            {
                "$inc":{
                    "gold":gold,
                    "power":-5
                }
            }
        )

    return redirect("/dashboard")

# =========================================
# CLAIM + ADS
# =========================================

@app.route("/claim")
def claim():

    if "user" not in session:
        return redirect("/")

    user = users.find_one({
        "username": session["user"]
    })

    now = time.time()

    # cooldown 30 detik
    if now - user["last_claim"] < 15:

        return "Tunggu 15 detik"

    users.update_one(
        {"username": session["user"]},
        {
            "$inc":{
                "gold":25
            },
            "$set":{
                "last_claim":now
            }
        }
    )

    return redirect(ADS_LINK)

# =========================================
# WATCH ADS
# =========================================

@app.route("/watchads")
def watchads():

    if "user" not in session:
        return redirect("/")

    user = users.find_one({
        "username": session["user"]
    })

    now = time.time()

    if now - user.get("last_ads", 0) < 15:

        return "Tunggu 15 detik"

    users.update_one(
        {"username": session["user"]},
        {
            "$inc":{
                "gold":50
            },
            "$set":{
                "last_ads":now
            }
        }
    )

    return redirect(ADS_LINK)

# =========================================
# DAILY
# =========================================

@app.route("/daily", methods=["POST"])
def daily():

    if "user" not in session:
        return redirect("/")

    user = users.find_one({
        "username": session["user"]
    })

    now = time.time()

    if now - user["last_daily"] >= 86400:

        users.update_one(
            {"username": session["user"]},
            {
                "$inc":{
                    "gold":DAILY_REWARD
                },
                "$set":{
                    "last_daily":now
                }
            }
        )

    return redirect("/dashboard")

# =========================================
# RECHARGE
# =========================================

@app.route("/recharge", methods=["POST"])
def recharge():

    if "user" not in session:
        return redirect("/")

    users.update_one(
        {"username": session["user"]},
        {
            "$set":{
                "power":100
            }
        }
    )

    return redirect("/dashboard")

# =========================================
# VIP
# =========================================

@app.route("/vip/<int:level>")
def vip(level):

    if "user" not in session:
        return redirect("/")

    users.update_one(
        {"username": session["user"]},
        {
            "$set":{
                "vip":level
            }
        }
    )

    return redirect("/dashboard")

# =========================================
# WITHDRAW
# =========================================

@app.route("/withdraw", methods=["POST"])
def withdraw():

    if "user" not in session:
        return redirect("/")

    amount = int(request.form["amount"])

    wallet = request.form["wallet"]

    user = users.find_one({
        "username": session["user"]
    })

    if amount < 1000:
        return "Minimal WD 1000"

    if user["balance"] < amount:
        return "Balance kurang"

    users.update_one(
        {"username": session["user"]},
        {
            "$inc":{
                "balance":-amount
            }
        }
    )

    withdraws.insert_one({

        "username":user["username"],
        "wallet":wallet,
        "amount":amount,
        "status":"pending"

    })

    return redirect("/dashboard")

# =========================================
# ADMIN LOGIN
# =========================================

@app.route("/admin-login",
methods=["GET","POST"])
def admin_login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:

            session["admin"] = True

            return redirect("/admin")

        return "Login gagal"

    return render_template_string(
        ADMIN_LOGIN
    )

# =========================================
# ADMIN PANEL
# =========================================

@app.route("/admin")
def admin():

    if "admin" not in session:
        return redirect("/admin-login")

    data = withdraws.find().sort("_id",-1)

    return render_template_string(
        ADMIN_HTML,
        data=data
    )

# =========================================
# APPROVE
# =========================================

@app.route("/approve/<id>")
def approve(id):

    if "admin" not in session:
        return redirect("/admin-login")

    withdraws.update_one(
        {"_id":ObjectId(id)},
        {
            "$set":{
                "status":"approved"
            }
        }
    )

    return redirect("/admin")

# =========================================
# REJECT
# =========================================

@app.route("/reject/<id>")
def reject(id):

    if "admin" not in session:
        return redirect("/admin-login")

    wd = withdraws.find_one({
        "_id":ObjectId(id)
    })

    users.update_one(
        {"username":wd["username"]},
        {
            "$inc":{
                "balance":wd["amount"]
            }
        }
    )

    withdraws.update_one(
        {"_id":ObjectId(id)},
        {
            "$set":{
                "status":"rejected"
            }
        }
    )

    return redirect("/admin")

# =========================================
# LOGOUT
# =========================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")

@app.route("/admin-logout")
def admin_logout():

    session.pop("admin")

    return redirect("/admin-login")

# =========================================
# RUN
# =========================================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
