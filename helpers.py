import traceback
import sqlite3
import random
import os
import json
from telethon import TelegramClient, events, Button, functions, types

try:
    conn = sqlite3.connect("database.db")
except:
    traceback.print_exc()

if os.path.exists("account.json"):
    with open("account.json", "r+") as f:
        account = json.load(f)
else:
    account = {}
    with open("account.json", "w+") as f:
        json.dump(account, f)


def savesss():
    global account
    with open("account.json", "w+") as f:
        json.dump(account, f)

def Menzione(ID_UTENTE, MENZIONE):
    return f"<a href=tg://user?id={ID_UTENTE}>{MENZIONE}</a>"
async def getBans():
    conn.cursor().execute("SELECT userid FROM bannedusers")
    res = conn.cursor().fetchall()
    bans = []
    for x in res:
        try:
            bans.append(f"{x[0]} | {Menzione(int(x[0]), (await client.get_entity(int(x[0]))).first_name)}")
        except:
            bans.append(f"{x[0]}")
    return bans
def get_ban(user_id: int):
    if conn.execute("SELECT COUNT (userid) FROM bannedusers WHERE userid = ?", [user_id]).fetchone()[0] < 1:
        return False
    else:
        return True
def cambia_tos(testo):
    conn.cursor().execute("UPDATE tos SET tos = ?", [testo])
    conn.commit()
def tos_acc(userid):
    if check_tos(userid):
        pass
    else:
        conn.cursor().execute("INSERT INTO tos (user_accept) VALUES (?)", [userid])
        conn.commit()
def check_tos(userid):
    result = conn.cursor().execute("SELECT user_accept FROM tos WHERE user_accept = ?", [userid])
    if len(result.fetchall()) > 0:
        return True
    else:
       return False
def tosmostra():
    return conn.cursor().execute("SELECT tos FROM tos").fetchone()[0]
def addBan(userId: int):
    conn.cursor().execute("INSERT INTO bannedusers (userid) VALUES (?)", [userId])
    conn.commit()
def rmBan(userId: int):
    conn.cursor().execute("DELETE FROM bannedusers WHERE userid = ?", [userId])
    conn.commit()
def isUserandAdd(user_id: int):
    result = conn.cursor().execute("SELECT * FROM user WHERE chat_id = ?", [user_id])
    if len(result.fetchall()) > 0:
        pass
    else:
        conn.cursor().execute("INSERT INTO user (chat_id, saldo, cron) VALUES (?,?,?)", [user_id, 0, "None"])
        conn.commit()
def get_saldo(user_id):
    result = conn.cursor().execute("SELECT * FROM user WHERE chat_id = ?", [user_id])
    if len(result.fetchall()) > 0:
        for saldo in conn.cursor().execute("SELECT saldo FROM user WHERE chat_id = ?", [user_id]).fetchall()[0]:
            return "%.2f" % saldo
    else:
        pass

def isUser(user_id):
    result = conn.cursor().execute("SELECT * FROM user WHERE chat_id = ?", [user_id])
    if len(result.fetchall()) > 0:
        return True
    else:
        return False
def count_sotto(nomec):
    return conn.cursor().execute("SELECT COUNT(category) FROM sottocategorie WHERE category = ?", [nomec]).fetchone()[0]
def sottokeyboard(nomec):
    keyboard = []
    temp_key = []
    i = 0
    for ii, in conn.cursor().execute("SELECT name FROM sottocategorie WHERE category = ?", [nomec]).fetchall():
        i += 1
        if not (i % 2) == 0:
            temp_key.append(Button.inline(ii, f"sotto_"+ii))
        else:
            temp_key.append(Button.inline(ii, f"sotto_"+ii))
            keyboard.append(temp_key)
            temp_key = []
        if count_sotto(nomec) == i:
            keyboard.append(temp_key)
    return keyboard
def getbuttonsotto(nomec):
    keyboard = []
    temp_key = []
    products = conn.cursor().execute("SELECT name, description, price, file_id FROM products WHERE sottocategory = ?", [nomec]).fetchall()
    if len(products) == 1:
        return [[Button.inline(products[0][0], f"product_{products[0][0]}")], [Button.inline("◀️", "shop")]]
    for x in range(1, len(products) + 1):
        if not (x % 2) == 0:
            temp_key.append(Button.inline(products[x - 1][0], f"product_{products[x - 1][0]}"))
        else:
            temp_key.append(Button.inline(products[x - 1][0], f"product_{products[x - 1][0]}"))
            keyboard.append(temp_key)
            temp_key = []
        if len(products) == x:
            keyboard.append(temp_key)
    keyboard.append([Button.inline("◀️", "shop")])
    return keyboard
# [<telethon.tl.types.KeyboardButtonCallback object at 0x7f7e60ad1760>, [<telethon.tl.types.KeyboardButtonCallback object at 0x7f7e60ad17f0>]]
def keyboardccc(products):
    keyboard = []
    temp_key = []
    if len(products) == 1:
        return [[Button.inline(products[0][0], f"product_{products[0][0]}")], [Button.inline("◀️", "shop")]]
    for x in range(1, len(products)+1):
        if not (x % 2) == 0:
            temp_key.append(Button.inline(products[x-1][0], f"product_{products[x-1][0]}"))
        else:
            temp_key.append(Button.inline(products[x-1][0], f"product_{products[x-1][0]}"))
            keyboard.append(temp_key)
            temp_key = []
        if len(products) == x:
            keyboard.append(temp_key)
    keyboard.append([Button.inline("◀️", "shop")])
    return keyboard
def keyboardDel(products):
    keyboard = []
    temp_key = []
    if len(products) == 1:
        return [[Button.inline(products[0][0], f"delproduct_{products[0][0]}")], [Button.inline("🏡", "shop")]]
    for x in range(1, len(products)+1):
        if not (x%2) == 0:
            temp_key.append(Button.inline(products[x-1][0], f"delproduct_{products[x-1][0]}"))
        else:
            temp_key.append(Button.inline(products[x-1][0], f"delproduct_{products[x-1][0]}"))
            keyboard.append(temp_key)
            temp_key = []
        if len(products) == x:
            keyboard.append(temp_key)
    keyboard.append([Button.inline("🏡", "shop")])
    return keyboard
def keyCategory(products):
    keyboard = []
    temp_key = []
    if len(products) == 1:
        return [[Button.inline(products[0], f"category_{products[0]}")], [Button.inline("🏡", "home")]]
    for x in range(1, len(products)+1):
        if not (x%2) == 0:
            temp_key.append(Button.inline(products[x-1], f"category_{products[x-1]}"))
        else:
            temp_key.append(Button.inline(products[x-1], f"category_{products[x-1]}"))
            keyboard.append(temp_key)
            temp_key = []
        if len(products) == x:
            keyboard.append(temp_key)
    keyboard.append([Button.inline("🏡", "home")])
    return keyboard
def getProducts(name: str = None):
    if name == None:
        result = conn.cursor().execute("SELECT name FROM products").fetchall()
    else:
        result = conn.cursor().execute("SELECT name, description, price, file_id FROM products WHERE name = ?", [name]).fetchone()
    return result
def getProductsK(name: str):
    result = conn.cursor().execute("SELECT name, description, price, file_id FROM products WHERE category = ?", [name]).fetchall()
    r = conn.cursor().execute("SELECT name, description, price, file_id, sottocategory FROM products WHERE category = ?", [name]).fetchall()
    res = []
    lista_esclusi = []
    for i in r:
        if i[4] != "None":
            lista_esclusi.append(i[0])
    for x in result:
        if x[0] not in lista_esclusi:
            res.append(x)
    return res
def getProductsKDEL(name: str):
    result = conn.cursor().execute("SELECT name, description, price, file_id FROM products WHERE category = ?", [name]).fetchall()
    res = []
    for x in result:
        res.append(x)
    return res
def getKey():
    result = conn.cursor().execute("SELECT name FROM category").fetchall()
    res = []
    for x, in result:
      res.append(x)
    return res
def keyCategoryDel(products):
    keyboard = []
    temp_key = []
    if len(products) == 1:
        return [[Button.inline(products[0], f"DEL_{products[0]}")], [Button.inline("◀️", "admin_panel")]]
    for x in range(1, len(products)+1):
        if not (x%2) == 0:
            temp_key.append(Button.inline(products[x-1], f"DEL_{products[x-1]}"))
        else:
            temp_key.append(Button.inline(products[x-1], f"DEL_{products[x-1]}"))
            keyboard.append(temp_key)
            temp_key = []
        if len(products) == x:
            keyboard.append(temp_key)
    keyboard.append([Button.inline("◀️", "admin_panel")])
    return keyboard
def getKdel():
    result = conn.cursor().execute("SELECT name FROM category").fetchall()
    res = []
    for x, in result:
      res.append(x)
    return res
def keyCategoryAddD(products):
    keyboard = []
    temp_key = []
    if len(products) == 1:
        return [[Button.inline(products[0], f"DESCRIZIONE_{products[0]}")], [Button.inline("◀️", "admin_panel")]]
    for x in range(1, len(products) + 1):
        if not (x % 2) == 0:
            temp_key.append(Button.inline(products[x - 1], f"DESCRIZIONE_{products[x - 1]}"))
        else:
            temp_key.append(Button.inline(products[x - 1], f"DESCRIZIONE_{products[x - 1]}"))
            keyboard.append(temp_key)
            temp_key = []
        if len(products) == x:
            keyboard.append(temp_key)
    keyboard.append([Button.inline("◀️", "admin_panel")])
    return keyboard
def addDesc(nomec, desc):
    conn.cursor().execute("UPDATE category SET descrizione = ? WHERE name = ?", [desc, nomec])
    conn.commit()
def returnDesc(nomec):
    try:
        if conn.cursor().execute("SELECT descrizione FROM category WHERE name = ?", [nomec]).fetchone()[0] == "None":
            return False
        else:
            return conn.cursor().execute("SELECT descrizione FROM category WHERE name = ?", [nomec]).fetchone()[0]
    except:
        traceback.print_exc()
        return False
def returnDescSOTTO(nomec):
    try:
        if conn.cursor().execute("SELECT descrizione FROM sottocategorie WHERE name = ?", [nomec]).fetchone()[0] == "None":
            return False
        else:
            return conn.cursor().execute("SELECT descrizione FROM sottocategorie WHERE name = ?", [nomec]).fetchone()[0]
    except:
        traceback.print_exc()
        return False
def getKAddD():
    result = conn.cursor().execute("SELECT name FROM category").fetchall()
    res = []
    for x, in result:
      res.append(x)
    return res
def count():
    return conn.cursor().execute("SELECT COUNT(chat_id) FROM user").fetchone()[0]
def getStats():
    return conn.cursor().execute("SELECT COUNT(*) FROM products").fetchone()[0]
def productExists(name: str) -> bool:
    result = conn.cursor().execute("SELECT COUNT(*) FROM products WHERE name = ?", [name]).fetchone()[0]
    if result > 0:
        return True
    else:
        return False
def addProduct(name: str, description: str, price: int, file_id: str, file_premio: str, testo: str, c: str, sotto: str) -> bool:
    conn.cursor().execute("INSERT INTO products (name, description, price, file_id, file_premio, testo, category, sottocategory) VALUES (?,?,?,?,?,?,?,?)", [name, description, price, file_id, file_premio, testo, c, sotto])
    conn.cursor().execute("INSERT INTO accounts (name, account) VALUES (?,?)", [name, "vuoto"])
    conn.commit()
    return True
def delProductlimited(name:str=None):
    conn.cursor().execute("DELETE FROM products WHERE file_id = ?",[name])
    conn.commit()
def delProduct(name):
    conn.cursor().execute("DELETE FROM products WHERE name = ?", [name])
    conn.commit()
    return True
def update_saldo(saldo: float, user_id: int):
        conn.cursor().execute("UPDATE user SET saldo = ? WHERE chat_id = ?", [saldo, user_id])
        conn.commit()
        return get_saldo(user_id)
def checker_file(name):
    if productExists(name):
        for r in conn.cursor().execute("SELECT file_premio FROM products WHERE name = ?", [name]).fetchall()[0]:
            if r == "vuoto":
                return False
            else:
                return True
import time
def get_account(name):
    if productExists(name):
        for r in conn.cursor().execute("SELECT testo FROM products WHERE name = ?", [name]).fetchall()[0]:
            if r == "account":
                rando = random.choice(account[name])
                account[name].remove(rando)
                savesss()
                if account[name].__len__() == 0:
                    conn.cursor().execute("UPDATE products SET testo = ? WHERE name = ?", ["vuoto", name])
                    conn.commit()
                return rando
def checker_testo(name):
    if productExists(name):
        for r in conn.cursor().execute("SELECT testo FROM products WHERE name = ?", [name]).fetchall()[0]:
            if r == "vuoto":
                return False
            else:
                return True
async def view(products):

    k = []
    for x in products:
        k.append([Button.inline(x[0], f"views_{x[0]}")])

    k.append([Button.inline("🏡", "home")])
    return k

def get_channel():
    for a in conn.cursor().execute("SELECT channel FROM check_ac").fetchone()[0]:
        return a

def get_start():
    try:
        return conn.cursor().execute("SELECT start FROM messaggi").fetchone()[0]
    except:
        traceback.print_exc()
        return "Start non impostato"

def addstartmsg(mex):
    conn.cursor().execute("UPDATE messaggi SET start = ?", [mex])
    conn.commit()


def get_paypal():
    try:
        return conn.cursor().execute("SELECT paypal FROM pagamenti").fetchone()[0]
    except:
        traceback.print_exc()
        return "google.com"

def get_paypalmex():
    try:
        return conn.cursor().execute("SELECT paypal FROM messaggixx").fetchone()[0]
    except:
        traceback.print_exc()
        return "google.com"

def get_btc():
    try:
        return conn.cursor().execute("SELECT bitcoin FROM messaggixx").fetchone()[0]
    except:
        traceback.print_exc()
        return "Vuoto"

def get_shop():
    try:
        return conn.cursor().execute("SELECT shop FROM messaggixx").fetchone()[0]
    except:
        traceback.print_exc()
        return "Vuoto"

def paypalla():
    try:
        return conn.cursor().execute("SELECT paypal FROM pagamenti").fetchone()[0]
    except:
        conn.cursor().execute("INSERT INTO pagamenti (paypal) VALUES (?)", ["google.com"])
        conn.commit()
    try:
        return conn.cursor().execute("SELECT paypal FROM messaggixx").fetchone()[0]
    except:
        conn.cursor().execute("INSERT INTO messaggixx (paypal) VALUES (?)", ["Vuoto"])
        conn.commit()
    try:
        return conn.cursor().execute("SELECT shop FROM messaggixx").fetchone()[0]
    except:
        conn.cursor().execute("INSERT INTO messaggixx (shop) VALUES (?)", ["Vuoto"])
        conn.commit()

def bitmammt():
    try:
        return conn.cursor().execute("SELECT bitcoin FROM messaggi").fetchone()[0]
    except:
        conn.cursor().execute("INSERT INTO messaggixx (bitcoin) VALUES (?)", ["Vuoto"])
        conn.commit()

def startmamma():
    try:
        return conn.cursor().execute("SELECT start FROM messaggi").fetchone()[0]
    except:
        conn.cursor().execute("INSERT INTO messaggi (start) VALUES (?)", ["Start non impostato"])
        conn.commit()

def addpaypallink(text):
    conn.cursor().execute("UPDATE pagamenti SET paypal = ?", [text])
    conn.commit()

def addpaypal(text):
    conn.cursor().execute("UPDATE messaggixx SET paypal = ?", [text])
    conn.commit()

def addshop(text):
    conn.cursor().execute("UPDATE messaggixx SET shop = ?", [text])
    conn.commit()

def addbtcaddress(text):
    conn.cursor().execute("UPDATE messaggixx SET bitcoin = ?", [text])
    conn.commit()

provider_token = "350862534:LIVE:MDIyNmM4ZDQ5NGY4" #Live / Test
TEST = False

def generate_invoice(price_label: str, price_amount: int, currency: str, title: str, description: str, payload: str, start_param: str) -> types.InputMediaInvoice:
    price = types.LabeledPrice(label=price_label, amount=price_amount)
    invoice = types.Invoice(
        currency=currency,
        prices=[price],
        test=TEST,
        name_requested=False,
        phone_requested=False,
        email_requested=False,
        shipping_address_requested=False,
        flexible=True,
        phone_to_provider=False,
        email_to_provider=False
    )
    return types.InputMediaInvoice(
        title=title,
        description=description,
        invoice=invoice,
        payload=payload.encode('UTF-8'),
        provider=provider_token,
        provider_data=types.DataJSON('{}'),
        start_param=start_param,
    )
