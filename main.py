import variables
import json
from flask import *
from chain import Chain


def block_div(block_no, from_name, from_address, to_name, to_address, value):
    block = f"""<div class="block b{block_no}">\n<div class="block-title">Block #{block_no}</div>\n<div class="block-details">\n<div>From : {from_name}({from_address})</div>\n<div>To: {to_name}({to_address})</div>\n<div>Value :{value}</div>\n</div>\n</div>"""
    return block


app = Flask(__name__)
block_chain = Chain()


@app.route("/")
def explorer():
    with open("./data/blocks.json") as file:
        blocks_data = json.load(file)
        blocks_data = {i: blocks_data[str(i)] for i in sorted([int(i) for i in list(blocks_data.keys())])}
    with open("./data/accounts.json") as file:
        accounts = json.load(file)
    all_blocks = ""
    for i in list(blocks_data.keys()):
        from_address = blocks_data[i]["from"]
        from_name = accounts.get(from_address, "")
        to_address = blocks_data[i]["to"]
        to_name = accounts.get(to_address, "")
        value = blocks_data[i]["value"]
        all_blocks += block_div(i, from_name, from_address, to_name, to_address, value)
    all_blocks = "{% extends 'explorer.html' %}\n{% block content %}\n" + all_blocks + "\n{% endblock %}"
    with open('./templates/blocks.html', 'w+') as file:
        file.write(all_blocks)
    return render_template("blocks.html")


@app.route("/wallet")
def wallet():
    if variables.logged_in:
        return render_template("wallet.html", name=variables.current_account_name,
                               address=variables.current_account_address,
                               balance=block_chain.get_balance(variables.current_account_address), symbol="INR")
    return render_template("walletLogin.html")


@app.route("/send")
def send():
    to = request.args.get('to')
    value = request.args.get('amount')
    block_chain.transfer(variables.current_account_address, to, value)
    with open("./data/blocks.json") as file:
        block_no, block_from = block_chain.get_latest_block()
        blocks = json.load(file)
        blocks[str(block_no)] = {"from": block_from, 'to': to, "value": value}
    with open("./data/blocks.json", 'w+') as file:
        json.dump(blocks, file)
    return redirect("/wallet")


@app.route("/login-page")
def login_page():
    variables.logged_in = False
    return render_template("walletLogin.html")


@app.route("/login")
def login():
    username = request.args.get("username")
    password = request.args.get("password")
    with open("./data/credentials.json") as file:
        creds = json.load(file)
        # print(username, password, creds, creds.get(username))
        if password and creds.get(username).get("password") == password:
            variables.logged_in = True
            variables.current_account_name = username
            variables.current_account_address = creds.get(username).get("address")
            return redirect("/wallet")
    return redirect("/login-page")


@app.route("/create-account")
def create_account():
    return render_template("createWallet.html")


@app.route("/signup")
def sign_up():
    username = request.args.get("username")
    password = request.args.get("password")
    retyped_password = request.args.get('retype-password')
    if (password != retyped_password) and password:
        return redirect('/create-account')
    assigned_address = block_chain.assign_account(username)
    with open("./data/credentials.json") as file:
        creds = json.load(file)
        creds[username] = {"password": password, "address": assigned_address}
    with open("./data/credentials.json", 'w+') as file:
        json.dump(creds, file)
    return redirect('/login-page')


app.run()
