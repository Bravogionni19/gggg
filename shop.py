#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

# ===============================#

import os
import json
import asyncio
import sys
import traceback
import sqlite3
import random
from telethon import TelegramClient, events, Button, functions, types
from helpers import *

# ===============================#

if not os.path.exists("shopbot_session"):
    os.mkdir("shopbot_session")

# ===============================#

# var da impostare #
channel = -1001470888156
ccc = False
ref_ll = 0.01
api_ids = 14732436
api_hashs = "6a6dcca1828828119158463284f00897"
TOKEN = "5745526853:AAGR1vbGKKXS72XfCrsXGGON-ReTHhQDdeU"
ADMIN = [5045889151]
# noob #
client = TelegramClient('shopbot_session/bot_token', api_hash=api_hashs, api_id=api_ids).start(bot_token=TOKEN)
client.parse_mode = 'html'
check_products = None
in_chat = []
new_product = {}

# ===============================#

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


# ===============================#

try:
    conn = sqlite3.connect("database.db")
    conn.cursor().execute("CREATE TABLE IF NOT EXISTS bannedusers (userid INT)", [])
    conn.cursor().execute("CREATE TABLE IF NOT EXISTS tos (tos TEXT, user_accept INT)")
    conn.cursor().execute("CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, description TEXT, price INT, file_id TEXT, file_premio TEXT, testo TEXT, account BOOL, category TEXT, sottocategory TEXT)")
    conn.cursor().execute("CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, account TEXT)")
    conn.cursor().execute("CREATE TABLE IF NOT EXISTS category (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, descrizione TEXT)")
    conn.cursor().execute("CREATE TABLE IF NOT EXISTS sottocategorie (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, category TEXT, descrizione TEXT)")
    conn.cursor().execute("CREATE TABLE IF NOT EXISTS user (chat_id INT, saldo FLOAT, cron TEXT)")
    conn.cursor().execute("CREATE TABLE IF NOT EXISTS pagamenti (paypal TEXT)")
    conn.cursor().execute("CREATE TABLE IF NOT EXISTS messaggi (start TEXT)")
    conn.cursor().execute("CREATE TABLE IF NOT EXISTS messaggixx (paypal TEXT, bitcoin TEXT, shop TEXT)")
    conn.commit()
except:
    traceback.print_exc()
    exit(code="❌ » Errore nel database")


def tos():
    try:
        conn.cursor().execute("SELECT tos FROM tos").fetchall()[0]
    except:
        conn.cursor().execute("INSERT INTO tos (tos) VALUES (?)", ["Tos non impostati"])
        conn.commit()

tos()
startmamma()
paypalla()
bitmammt()

# ---------------------------------------#

cur = conn.cursor()
LISTAPAGATI = []

"""@client.on(events.NewMessage(pattern=r"\/restart", incoming=True))
async def riavvia(event):
    if (await event.get_sender()).id in ADMIN:
        sys.stdout.flush()
        os.execl(sys.executable, 'python', __file__, *sys.argv[1:])"""

# stripe
@client.on(events.Raw(types.UpdateBotPrecheckoutQuery))
async def payment_pre_checkout_handler(event):
    product = event.payload.decode()
    if product == "5":
        await client(functions.messages.SetBotPrecheckoutResultsRequest(query_id=event.query_id, success=True, error=None))
    elif product == "10":
        await client(functions.messages.SetBotPrecheckoutResultsRequest(query_id=event.query_id, success=True, error=None))
    if product == "15":
        await client(functions.messages.SetBotPrecheckoutResultsRequest(query_id=event.query_id, success=True, error=None))
    elif product == "20":
        await client(functions.messages.SetBotPrecheckoutResultsRequest(query_id=event.query_id, success=True, error=None))
    else:
        await client(functions.messages.SetBotPrecheckoutResultsRequest(query_id=event.query_id, success=False, error="❌Errore❌"))

@client.on(events.Raw(types.UpdateNewMessage))
async def payment_received_handler(event):
    if isinstance(event.message.action, types.MessageActionPaymentSentMe):
        payment: types.MessageActionPaymentSentMe = event.message.action
        p = payment.payload.decode()
        if p == "5":
            update_saldo(float(get_saldo(int(event.message.sender_id))) + 5, event.message.sender_id)
            await client.send_message(event.message.sender_id, f"<b>✅ ⇢ Abbiamo Aggiunto 5€ Al Tuo Account</b>")
        elif p == "10":
            update_saldo(float(get_saldo(int(event.message.sender_id))) + 10, event.message.sender_id)
            await client.send_message(event.message.sender_id, f"<b>✅ ⇢ Abbiamo Aggiunto 10€ Al Tuo Account</b>")
        elif p == "15":
            update_saldo(float(get_saldo(int(event.message.sender_id))) + 15, event.message.sender_id)
            await client.send_message(event.message.sender_id, f"<b>✅ ⇢ Abbiamo Aggiunto 15€ Al Tuo Account</b>")
        elif p == "20":
            update_saldo(float(get_saldo(int(event.message.sender_id))) + 20, event.message.sender_id)
            await client.send_message(event.message.sender_id, f"<b>✅ ⇢ Abbiamo Aggiunto 20€ Al Tuo Account</b>")
# parte start
@client.on(events.NewMessage(func=lambda e: e.is_private and e.text.startswith("/start")))
async def startimp(event):
    user = await event.get_sender()
    try:
        tt = event.text.split(" ")[1]
        if not isUser(user.id) and not int(tt) == user.id:
            isUserandAdd(user.id)
            update_saldo(float(get_saldo(tt)) + float(ref_ll), int(tt))
            await client.send_message(int(tt), f"<b>👋🏻Ciao, l'utente {user.first_name} ha utilizzato il tuo link reffeal sono stati invitati con successo! +0.01€</b>")
            for a in ADMIN:
                try:
                    await client.send_message(a, user.first_name + " Ha usato il link di " + str(tt))
                except:
                    pass
            await event.respond(
                f"<b>👋🏻Ciao, per utilizzare il bot devi essere iscritto al canale!⬇️</b>",
                buttons=[
                        [Button.url("🗝ISCRIVITI🗝", "https://t.me/" + (await client.get_entity(channel)).username)],
                        [Button.inline("✅️AGGIORNA✅️", "controlla_iscrizione")]
                    ]
                )
        else:
            isUserandAdd(user.id)
            await event.respond("Hai già avviato il bot in passato, furbetto!!")
    except:
        isUserandAdd(user.id)
        if ccc:
            try:
                await client(functions.channels.GetParticipantRequest(
                        channel=channel,
                        participant=user.id))
                if not user.id in ADMIN:
                    await event.respond(  # per utenti
                            get_start().replace("{mention}", Menzione(user.id, user.first_name)).replace("{nome}", user.first_name).replace("{username}", "@"+user.username).replace("{saldo}", str(get_saldo(user.id))),

                            buttons=[
                                [Button.inline("💰SALDO💰", "saldo"), Button.inline("🛍SHOP🛍", "shop")],                                   
                [Button.url("⛩️REDIRECT⛩️", "https://t.me/MonstersChannel"), Button.inline("🔒TOS🔒", "tos")],
                [Button.inline("📋ALTRO📋", "altro"), Button.url("🆘️SUPPORTO🆘️", "https://t.me/Assistenza_Monsters_Bot")], 
                [Button.inline("📊STATISTICHE📊", "stats")]], link_preview=False)

                else:
                    await event.respond(  # per admin
                            get_start().replace("{mention}", Menzione(user.id, user.first_name)).replace("{nome}", user.first_name).replace("{username}", "@"+user.username).replace("{saldo}", str(get_saldo(user.id))),
                            buttons=[
                                [Button.inline("👮🏻‍♂️Pannello👮🏻‍♂️", "admin_panel")],
                                [Button.inline("💰SALDO💰", "saldo"), Button.inline("🛍SHOP🛍", "shop")],                                   
                [Button.url("⛩️REDIRECT⛩️", "https://t.me/MonstersChannel"), Button.inline("🔒TOS🔒", "tos")],
                [Button.inline("📋ALTRO📋", "altro"), Button.url("🆘️SUPPORTO🆘️", "https://t.me/Assistenza_Monsters_Bot")], 
                [Button.inline("📊STATISTICHE📊", "stats")]], link_preview=False)


            except:
                await event.respond(
                f"<b>👋🏻Ciao, per utilizzare il bot devi essere iscritto al canale!⬇️</b>",
                buttons=[
                        [Button.url("🗝ISCRIVITI🗝","https://t.me/" + (await client.get_entity(channel)).username)],
                        [Button.inline("🔄AGGIORNA🔄", "controlla_iscrizione")]
                    ]
                )
        else:
            if not user.id in ADMIN:
                await event.respond(  # per utenti
                    get_start().replace("{mention}", Menzione(user.id, user.first_name)).replace("{nome}", user.first_name).replace("{username}", "@"+user.username).replace("{saldo}", str(get_saldo(user.id))),
                        buttons=[
                    
                            [Button.inline("💰SALDO💰", "saldo"), Button.inline("🛍SHOP🛍", "shop")],                                   
                [Button.url("⛩️REDIRECT⛩️", "https://t.me/MonstersChannel"), Button.inline("🔒TOS🔒", "tos")],
                [Button.inline("📋ALTRO📋", "altro"), Button.url("🆘️SUPPORTO🆘️", "https://t.me/Assistenza_Monsters_Bot")], 
                [Button.inline("📊STATISTICHE📊", "stats")]], link_preview=False)


            else:
                await event.respond(  # per admin
                     get_start().replace("{mention}", Menzione(user.id, user.first_name)).replace("{nome}", user.first_name).replace("{username}", "@"+user.username).replace("{saldo}", str(get_saldo(user.id))),
                        buttons=[
                            [Button.inline("👮🏻‍♂️Pannello👮🏻‍♂️", "admin_panel")],
                            [Button.inline("💰SALDO💰", "saldo"), Button.inline("🛍SHOP🛍", "shop")],                                   
                [Button.url("⛩️REDIRECT⛩️", "https://t.me/MonstersChannel"), Button.inline("🔒TOS🔒", "tos")],
                [Button.inline("📋ALTRO📋", "altro"), Button.url("🆘️SUPPORTO🆘️", "https://t.me/Assistenza_Monsters_Bot")], 
                [Button.inline("📊STATISTICHE📊", "stats")]], link_preview=False)


@client.on(events.NewMessage(func=lambda e: e.is_private and e.text.startswith("/mexstart")))
async def messagestart(event):
    if (await event.get_sender()).id in ADMIN:
        addstartmsg(event.text.replace("/mexstart", ""))
        await event.respond("Mex start impostato !")
# vari cmd
@client.on(events.NewMessage(func=lambda e: e.is_private))
async def Menu_1(event):
    global ADMIN, check_products, new_product, account, channel, ccc, in_chat, ref_ll, LISTAPAGATI
    user = await event.get_sender()
    if event.text.startswith("/ban") and user.id in ADMIN:
        try:
            addBan(event.text.split()[1])
            await event.respond("✅ » Utente bannato")
        except:
            await event.respond("Usage: /ban [userId]")
    elif event.text.startswith("/unban") and user.id in ADMIN:
        try:
            rmBan(event.text.split()[1])
            await event.respond("✅ » Utente sbannato")
        except:
            traceback.print_exc()
            await event.respond("Usage: /unban [userId]")
    elif event.text.startswith("/admin") and user.id in ADMIN:
        try:
            ADMIN.append(int(event.text.split()[1]))
            await event.respond("✅ » Utente messo admin")
        except:
            traceback.print_exc()
            await event.respond("Usage: /admin [userId]")
    elif event.text.startswith("/unadmin") and user.id in ADMIN:
        try:
            ADMIN.remove(int(event.text.split()[1]))
            await event.respond("✅ » Utente tolto admin")
        except:
            traceback.print_exc()
            await event.respond("Usage: /unadmin [userId]")
    elif event.text.startswith("/tos") and user.id in ADMIN:
        try:
            tostext = event.text.replace("/tos", "")
            cambia_tos(tostext)
            await event.respond("✅ » Tos messi correttamente")
        except:
            traceback.print_exc()
            await event.respond("Usage: /tos [tostext]")
    elif get_ban(user.id):
        return await event.respond("❌ » Sei bannato")
    if user.id in in_chat:
        for x in ADMIN:
            try:
                await client.send_message(x, f"<a href=tg://user?id={user.id}>{user.first_name}</a> {user.id} : {event.text}", file=event.media,
                                          link_preview=False)
            except:
                pass
        await event.respond("✅ » Messaggio inviato correttamente")
    elif event.is_reply and user.id in ADMIN:
        reply = await event.get_reply_message()
        if reply == None:
            return
        ent = reply.entities
        try:
            id = ent[0].user_id
        except:
            id = int(reply.text.split(" ")[1])
        try:
            await client.send_message(id, "👮🏻‍♂️: "+event.raw_text.replace("<nolink>", ""), file=event.media,
                                      link_preview=("<nolink>" not in event.raw_text))
        except TypeError:
            await client.send_message(id, "👮🏻‍♂️: "+event.raw_text.replace("<nolink>", ""),
                                      link_preview=("<nolink>" not in event.raw_text))
        for x in ADMIN:
            try:
                await client.send_message(x, f"Uno dello staff ha già risposto a {id}")
            except:
                pass
        await event.respond("✅ » Messaggio inviato correttamente")
    elif event.text.startswith("/ref") and user.id in ADMIN:
        try:
            ref_ll = float(event.text.split(" ")[1])
            await event.respond(f"✅ » ref aumento messo a {ref_ll} correttamente")
        except:
            traceback.print_exc()
            await event.respond("Usage: /ref [price]")
    elif get_ban(user.id):
        return await event.respond("❌ » Sei bannato")
    elif user.id in in_chat:
        for x in ADMIN:
            try:
                await client.send_message(x, f"{Menzione(user.id, user.first_name)}: {event.text}", file=event.media,
                                          link_preview=False)
            except:
                pass
        await event.respond("✅ » Messaggio inviato correttamente")
    elif event.is_reply and user.id in ADMIN:
        reply = await event.get_reply_message()
        ent = reply.entities
        id = ent[0].user_id
        try:
            await client.send_message(id, event.raw_text.replace("<nolink>", ""), file=event.media,
                                      link_preview=("<nolink>" not in event.raw_text))
        except TypeError:
            await client.send_message(id, event.raw_text.replace("<nolink>", ""),
                                      link_preview=("<nolink>" not in event.raw_text))
        await event.respond("✅ » Messaggio inviato correttamente")
    elif user.id in LISTAPAGATI:
        if event.photo:
            for x in ADMIN:
                try:
                    await client.send_message(x, f"{Menzione(user.id, user.first_name)}: Prova pagamento\nUserid: <code>{user.id}</code>", file=event.media, link_preview=False)
                except:
                    pass
            LISTAPAGATI.remove(user.id)
            await event.respond("🏡 Torna alla home 🏡", buttons=[[Button.inline("🏡", "home")]])
        else:
            await event.respond("Va inviata una foto !")
    elif event.text.startswith("/add") and user.id in ADMIN:
        text = event.text.split(" ")
        update_saldo(float(get_saldo(int(text[1]))) + float(text[2]), text[1])
        await event.respond("✅ » Saldo ricaricato con successo")
        await client.send_message(int(text[1]), f"✅ » È stato aggiunto del saldo al tuo account")
    elif event.text.startswith("/del") and user.id in ADMIN:
        text = event.text.split(" ")
        update_saldo(float(get_saldo(int(text[1]))) - float(text[2]), text[1])
        await event.respond("✅ » Saldo rimosso con successo")
        await client.send_message(int(text[1]), f"❌ » È stato rimosso del saldo dal tuo account")
    elif event.text.startswith("/post") and user.id in ADMIN:
        text = event.text.replace("/post", "")
        for a, in conn.cursor().execute("SELECT chat_id FROM user").fetchall():
            try:
                await client.send_message(a, "" + text)
            except:
                pass
        await event.respond(f"✅ » Post inviato")
    elif event.text.startswith("/linkpp") and user.id in ADMIN:
        text = event.raw_text.replace("/linkpp", "")
        addpaypallink(text)
        await event.respond(f"✅ » Paypal Link impostato correttamente")
    elif event.text.startswith("/paypal") and user.id in ADMIN:
        text = event.raw_text.replace("/paypal", "")
        addpaypal(text)
        await event.respond(f"✅ » Paypal mex impostato correttamente")
    elif event.text.startswith("/bitcoin") and user.id in ADMIN:
        text = event.text.replace("/bitcoin", "")
        addbtcaddress(text)
        await event.respond(f"✅ » Bitcoin mex impostato correttamente")
    elif event.text.startswith("/shop") and user.id in ADMIN:
        text = event.text.replace("/shop", "")
        addshop(text)
        await event.respond(f"✅ » shop mex impostato correttamente")

# add product
    elif check_products == 1 and user.id in ADMIN:
        if not productExists(event.text):
            new_product['file_premio'] = "vuoto"
            new_product['testo'] = "vuoto"
            new_product['name'] = event.text
            check_products = 2
            await event.respond("✅ » Invia la descrizione")
        else:
            check_products = None
            await event.respond('❌ » Prodotto già esistente', buttons=[[Button.inline("◀️", "admin_panel")]])
    elif check_products == 2 and user.id in ADMIN:
        new_product['description'] = event.text
        check_products = 3
        await event.respond("✅ » Invia il prezzo, solo numero(es. 10)")
    elif check_products == 3 and user.id in ADMIN:
        try:
            float(event.text)
            new_product['price'] = event.text
            check_products = 4
            await event.respond("✅ » Invia un testo per riconoscere il prodotto (es. bot)")
        except:
            await event.respond("✅ » Invia un prezzo, solo numero(es. 10)")
    elif check_products == 4 and user.id in ADMIN:
        new_product["cacca"] = event.text
        check_products = 90
        await event.respond("✅ » Invia il nome della categoria")
    elif check_products == 90 and user.id in ADMIN:
        check_products = None
        result = conn.cursor().execute("SELECT * FROM category WHERE name = ?", [event.text])
        if len(result.fetchall()) > 0:
            pass
        else:
            conn.cursor().execute("INSERT INTO category (name, descrizione) VALUES (?, ?)", [event.text, "None"])
            conn.commit()
        if addProduct(new_product['name'], new_product['description'], float(new_product['price']),
                      new_product["cacca"], new_product['file_premio'], new_product['testo'], event.text, "None"):
            await event.respond("✅ » Prodotto aggiunto correttamente", buttons=[[Button.inline("◀️", "admin_panel")]])
    elif check_products == 5 and user.id in ADMIN:
        try:
            await event.message.download_media("file_premi/" + new_product["faffa"])
            conn.cursor().execute("UPDATE products SET file_premio = ? WHERE name = ?",
                                  [event.message.media.document.attributes[0].file_name, new_product["faffa"]])
            conn.commit()
            await event.respond("✅ » File aggiunto correttamente", buttons=[[Button.inline("◀️", "admin_panel")]])
        except:
            pass
        check_products = None
    elif check_products == 6 and user.id in ADMIN:
        try:
            splitter = event.text.split("\n")
            account[new_product["faffa"]] = []
            for a in splitter:
                account[new_product["faffa"]].append(a)
                savesss()
            await event.respond("✅ » Account aggiunto/i correttamente", buttons=[[Button.inline("◀️", "admin_panel")]])
        except:
            pass
        check_products = None
    elif check_products == 7 and user.id in ADMIN:
        check_products = None
        try:
            conn.cursor().execute("UPDATE products SET testo = ? WHERE name = ?", [event.text, new_product["faffa"]])
            conn.commit()
            await event.respond("✅ » Testo aggiunto correttamente", buttons=[[Button.inline("◀️", "admin_panel")]])
        except:
            pass
    elif check_products == "desc":
        addDesc(new_product["descrizionec"], event.text)
        check_products = None
        await event.respond("✅ » Descrizione aggiunta correttamente", buttons=[[Button.inline("◀️", "admin_panel")]])
    elif check_products == "add_sotto":
        result = conn.cursor().execute("SELECT * FROM sottocategorie WHERE name = ?", [event.text])
        if len(result.fetchall()) > 0:
            await event.respond("✅ » Sottocategoria già esistente, riprova con un altro nome !", buttons=[[Button.inline("◀️", "admin_panel")]])
        else:
            new_product["nome_sotto"] = event.text
            check_products = "add_sotto_twoStep"
            await event.respond("✅ » Ora invia il nome della categoria in cui vuoi metterlo (se non esiste verrà creata)", buttons=[[Button.inline("◀️", "admin_panel")]])
    elif check_products == "add_sotto_twoStep":
        result = conn.cursor().execute("SELECT * FROM category WHERE name = ?", [event.text])
        if len(result.fetchall()) > 0:
            conn.cursor().execute("INSERT INTO sottocategorie (name, category, descrizione) VALUES (?, ?, ?)", [new_product["nome_sotto"], event.text, "None"])
            conn.commit()
            check_products = None
            await event.respond("✅ » SottoCategoria aggiunta correttamente", buttons=[[Button.inline("◀️", "admin_panel")]])
        else:
            conn.cursor().execute("INSERT INTO category (name, descrizione) VALUES (?, ?)", [event.text, "None"])
            conn.cursor().execute("INSERT INTO sottocategorie (name, category) VALUES (?, ?)", [new_product["nome_sotto"], event.text])
            conn.commit()
            check_products = None
            await event.respond("✅ » SottoCategoria aggiunta correttamente", buttons=[[Button.inline("◀️", "admin_panel")]])
    elif check_products == "del_sotto":
        try:
            conn.cursor().execute("DELETE FROM sottocategorie WHERE name = ?", [event.text])
            conn.commit()
        except:
            pass
        check_products = None
        await event.respond("✅ » SottoCategoria rimossa correttamente", buttons=[[Button.inline("◀️", "admin_panel")]])
    elif check_products == "add_p_sotto":
        new_product["sottocategoriacazzo"] = event.text
        check_products = "add_p_sotto_final"
        await event.respond("✅ » Ora invia il nome del prodotto (il prodotto deve essere già creato)", buttons=[[Button.inline("◀️", "admin_panel")]])
    elif check_products == "add_p_sotto_final":
        try:
            conn.cursor().execute("UPDATE products SET sottocategory = ? WHERE name = ?", [new_product["sottocategoriacazzo"], event.text])
            conn.commit()
        except:
            pass
        check_products = None
        await event.respond("✅ » Prodotto aggiunto alla sottocategoria correttamente", buttons=[[Button.inline("◀️", "admin_panel")]])
    elif check_products == "add_descS":
        new_product["sottocategoriacazzoDURO"] = event.text
        check_products = "add_descS_final"
        await event.respond("✅ » Ora invia la descrizione (la sottocategoria deve essere già stata creata, se la vuoi togliere scrivi None)", buttons=[[Button.inline("◀️", "admin_panel")]])
    elif check_products == "add_descS_final":
        try:
            conn.cursor().execute("UPDATE sottocategorie SET descrizione = ? WHERE name = ?", [event.text, new_product["sottocategoriacazzoDURO"]])
            conn.commit()
        except:
            pass
        check_products = None
        await event.respond("✅ » Descrizone aggiunta correttamente", buttons=[[Button.inline("◀️", "admin_panel")]])
    elif check_products == "add_category_duro":
        result = conn.cursor().execute("SELECT * FROM category WHERE name = ?", [event.text])
        if len(result.fetchall()) > 0:
            pass
        else:
            conn.cursor().execute("INSERT INTO category (name, descrizione) VALUES (?, ?)", [event.text, "None"])
            conn.commit()
        check_products = None
        await event.respond("✅ » Categoria aggiunta correttamente", buttons=[[Button.inline("◀️", "admin_panel")]])
# ===============================#

@client.on(events.CallbackQuery(func=lambda e: e.is_private))
async def Bottoni(event):
    global ADMIN, check_products, new_product, account, channel, ccc, in_chat, LISTAPAGATI
    user = await event.get_sender()
    if get_ban(user.id):
        return await event.edit("❌ » Sei bannato dall'uso del bot!")
    if event.data == b"home":
        if user.id in in_chat:
            in_chat.remove(user.id)
        if not user.id in ADMIN:
            await event.edit(  # per utenti
               get_start().replace("{mention}", Menzione(user.id, user.first_name)).replace("{nome}", user.first_name).replace("{username}", "@"+user.username).replace("{saldo}", str(get_saldo(user.id))),
                buttons=[
                    [Button.inline("💰SALDO💰", "saldo"), Button.inline("🛍SHOP🛍", "shop")],                                   
                [Button.url("⛩️REDIRECT⛩️", "https://t.me/MonstersChannel"), Button.inline("🔒TOS🔒", "tos")],
                [Button.inline("📋ALTRO📋", "altro"), Button.url("🆘️SUPPORTO🆘️", "https://t.me/Assistenza_Monsters_Bot")], 
                [Button.inline("📊STATISTICHE📊", "stats")]], link_preview=False)

        else:
            await event.edit(  # per admin
                get_start().replace("{mention}", Menzione(user.id, user.first_name)).replace("{nome}", user.first_name).replace("{username}", "@"+user.username).replace("{saldo}", str(get_saldo(user.id))),
                buttons=[
                    [Button.inline("👮🏻‍♂️Pannello👮🏻‍♂️", "admin_panel")],
                    [Button.inline("💰SALDO💰", "saldo"), Button.inline("🛍SHOP🛍", "shop")],                                   
                [Button.url("⛩️REDIRECT⛩️", "https://t.me/MonstersChannel"), Button.inline("🔒TOS🔒", "tos")],
                [Button.inline("📋ALTRO📋", "altro"), Button.url("🆘️SUPPORTO🆘️", "https://t.me/Assistenza_Monsters_Bot")], 
                [Button.inline("📊STATISTICHE📊", "stats")]], link_preview=False)

    elif event.data == b"reff":
        await event.edit(
            f"✅ Link da inviare agli Amici per guadagnare <b>{ref_ll}€</b>\n\n⇢ <code>https://t.me/{(await client.get_me()).username}?start={user.id}</code>",
            buttons=[[Button.inline("◀️", "rc")]])
    elif event.data == b"crn":
        r = cur.execute("SELECT cron FROM user WHERE chat_id = ?", [user.id]).fetchone()[0]
        if r == "None":
            await event.edit("📄 Cronologia acquisti\n\n<i>Nessun acquisto</i>",
                             buttons=[[Button.inline("◀️", "saldo")]])
        else:
            n = 4096
            rs = [r[i:i + n] for i in range(0, len(r), n)]
            if len(rs) > 1:
                s = 1
                for x in rs:
                    if s == 1:
                        await event.edit(f"📄 Cronologia acquisti\n\n{x}")
                    elif len(rs) == s:
                        await event.respond(x, buttons=[[Button.inline("◀️", "saldo")]])
                    else:
                        await event.respond(x)
                    s += 1
            else:
                await event.edit(f"📄 Cronologia acquisti\n\n{r}", buttons=[[Button.inline("◀️", "saldo")]])

    elif event.data == b"controlla_iscrizione":
        try:
            await client(functions.channels.GetParticipantRequest(channel=channel, participant=user.id))
            await event.answer("🔓")
            await event.edit(  # per utenti
                get_start().replace("{mention}", Menzione(user.id, user.first_name)).replace("{nome}", user.first_name).replace("{username}", "@"+user.username).replace("{saldo}", str(get_saldo(user.id))),
                buttons=[
                [Button.inline("💰SALDO💰", "saldo"), Button.inline("🛍SHOP🛍", "shop")],                                   
                [Button.url("⛩️REDIRECT⛩️", "https://t.me/MonstersChannel"), Button.inline("🔒TOS🔒", "tos")],
                [Button.inline("📋ALTRO📋", "altro"), Button.url("🆘️SUPPORTO🆘️", "https://t.me/Assistenza_Monsters_Bot")], 
                [Button.inline("📊STATISTICHE📊", "stats")]], link_preview=False)
        except:
            await event.answer("🔒", alert=True)
    elif event.data == b"saldo":
        if check_tos(user.id):
            await event.edit(
                f"💲Il tuo <u>saldo attuale</u>: {get_saldo(user.id)}€",
                buttons=[
                    [Button.inline("➕ Ricarica ➕", "rc")],
                    [Button.inline("📄 Cronologia acquisti", "crn")],
                    [Button.inline("🏡", "home")],
                ]
            )
        else:
            await event.answer("Devi accettare prima i ToS!", alert=True)
    elif event.data == b"rc":
        await event.edit(f"🛒Ricarica <u>senza commissioni⤵️</u>", buttons=[[Button.inline("🅿️PAYPAL🅿️", "rc_paypal")],
                                                                            [Button.inline("🅱️BITCOIN🅱️", "rc_bitcoin"),    
                                                                 Button.inline("😱GRATIS😱", "reff")],

[Button.inline("💳CARTA💳", "rc_carta")],
                                                                            [Button.inline("◀️", "saldo")]])

    elif event.data == b"rc_carta":
        await event.edit(f"""
‼️Donazione per @MonstersShopBot 


📈Qui potrai Sostenere il Progetto @MonstersShopBot""", buttons=[
            [Button.inline("5€", "rc_5"), Button.inline("10€", "rc_10")],
            [Button.inline("15€", "rc_15"), Button.inline("20€", "rc_20")],
            [Button.inline("◀️", "rc")]
        ])
    elif event.data == b"rc_5":
        await event.delete()
        await event.respond("⬇️Premi Il</b> Pulsante Per Donare⬇️", file=generate_invoice(price_label='5', price_amount=500, currency="EUR", title="5€", description="", payload="5", start_param='abc'))
    elif event.data == b"rc_10":
        await event.delete()
        await event.respond("⬇️Premi Il</b> Pulsante Per Donare⬇️", file=generate_invoice(price_label='10', price_amount=1000, currency="EUR", title="10€", description="", payload="10", start_param='abc'))
    elif event.data == b"rc_15":
        await event.delete()
        await event.respond("⬇️Premi Il</b> Pulsante Per Donare⬇️", file=generate_invoice(price_label='15', price_amount=1500, currency="EUR", title="15€", description="", payload="15", start_param='abc'))
    elif event.data == b"rc_20":
        await event.delete()
        await event.respond("⬇️Premi Il</b> Pulsante Per Donare⬇️", file=generate_invoice(price_label='20', price_amount=2000, currency="EUR", title="20€", description="", payload="20", start_param='abc'))
    elif event.data == b"rc_paypal":
        await event.edit(get_paypalmex(), buttons=[
            [Button.url("​💰Paga💰​", get_paypal().replace(" ", ""))],
            [Button.inline("✅️Pagamento inviato✅️", "pagato")],
            [Button.inline("◀️", "rc")]
        ], link_preview=False)

    elif event.data == b"pagato":
        if user.id not in LISTAPAGATI:
            LISTAPAGATI.append(user.id)
            await event.edit("📸 Ora invia come prova del pagamento uno screen che conferma ci sia stato línvio dei soldi !", buttons=[
                [Button.inline("❌ Annulla ❌", "del_process")]
            ])
        else:
            await event.answer("❌ Già sei in lista, invia lo screen ! ❌", alert=True)
    elif event.data == b"del_process":
        if user.id in LISTAPAGATI:
            LISTAPAGATI.remove(user.id)
        await event.edit("🏡 Torna alla home 🏡", buttons=[[Button.inline("🏡", "home")]])
    elif event.data == b"rc_bitcoin":
        await event.edit(get_btc(), buttons=[
            [Button.inline("✅️Pagamento inviato✅️", "pagato")],
            [Button.inline("◀️", "rc")]
        ], link_preview=False)

        
    elif event.data == b"shop":

        if not user.id in ADMIN:

            if check_tos(user.id):

                await event.edit(

                    get_shop(),

                    buttons=keyCategory(getKey())

                )

            else:

                await event.answer("Prima accetta i tos !", alert=True)

        else:

            await event.edit(

                get_shop(),

                buttons=keyCategory(getKey())

            )


    elif event.data == b"altro":
        await event.edit(
            f"👋Benvenuto nella Sezione 📋ALTRO📋",
            buttons=[
                [Button.url("​🧑🏻‍💻PROJECTS🧑🏻‍💻", "https://t.me/MonsterProjects"), Button.url("🏹CANALE🏹", "https://t.me/MonstersWar")],
                [Button.url("✅️FEEDBACK✅️", "https://t.me/+3sFHsjBsNMVjNDM0")],
                [Button.inline("🏡", "home")]])


    elif event.data == b"tos":
        if check_tos(user.id):
            await event.edit(tosmostra(), buttons=[[Button.inline("🏡", "home")]], link_preview=False)
        else:
            await event.edit(tosmostra(),
                             buttons=[[Button.inline("✅Accetta ToS✅", "acc_tos")], [Button.inline("🏡", "home")]],
                             link_preview=False)
    elif event.data == b"acc_tos":
        tos_acc(user.id)
        await event.edit("Tos accettati !", buttons=[[Button.inline("🏡", "home")]])
    elif event.data == b"edit_prodotti":
        await event.edit(
            f"⬇️Applica Qui Le Tue Modifiche⬇️",
            buttons=[
                [Button.inline("➕Aggiungi Prodotto➕", "add_prodotto")],
                [Button.inline("➕Aggiungi File/Account➕", "add_give")],
                [Button.inline("✖️Elimina Prodotto✖️", "delpro")],
                [Button.inline("◀️", "admin_panel")]])

    elif event.data == b"edit_categorie":
        await event.edit(
            f"⬇️Applica Qui Le Tue Modifiche⬇️",
            buttons=[
                [Button.inline("🛠️Sotto-Categorie🛠️", "sottocategory")],
                [Button.inline("➕Aggiungi una categoria➕", "add_category_duro")],
                [Button.inline("➕Aggiungi una descrizione➕", "add_desc")],
                [Button.inline("✖️Elimina Categoria✖️", "delc")],
                [Button.inline("◀️", "admin_panel")]])
    elif event.data == b"sottocategory":
        await event.edit(
            f"⬇️Applica Qui Le Tue Modifiche⬇️",
            buttons=[
                [Button.inline("➕Aggiungi SottoCategoria➕", "add_sotto")],
                [Button.inline("➕Metti prodotto in una SottoCategoria➕", "add_p_sotto")],
                [Button.inline("➕Aggiungi una descrizione➕", "add_descS")],
                [Button.inline("✖️Elimina SottoCategoria✖️", "delsotto")],
                [Button.inline("◀️", "admin_panel")]])
    elif event.data == b"add_category_duro":
        check_products = "add_category_duro"
        await event.edit("✅ » Invia nome categoria",
                         buttons=[
                             [Button.inline('◀️', 'admin_panel')]])
    elif event.data == b"add_sotto":
        check_products = "add_sotto"
        await event.edit("✅ » Invia nome sottocategoria",
                         buttons=[
                             [Button.inline('◀️', 'admin_panel')]])
    elif event.data == b"delsotto":
        check_products = "del_sotto"
        await event.edit("✅ » Invia il nome della sottocategoria da eliminare",
                         buttons=[
                             [Button.inline('◀️', 'admin_panel')]])
    elif event.data == b"add_p_sotto":
        check_products = "add_p_sotto"
        await event.edit("✅ » Invia il nome della sottocategoria in cui vuoi aggiungere il prodotto",
                         buttons=[
                             [Button.inline('◀️', 'admin_panel')]])
    elif event.data == b"add_descS":
        check_products = "add_descS"
        await event.edit("<b>📜 Invia nome sottocategoria a cui vuoi aggiungere una descrizione 📜</b>", buttons=[[Button.inline('◀️', 'admin_panel')]])
    elif event.data == b"add_desc":
        await event.edit("<b>📜 Scegli la categoria a cui aggiungere la categoria 📜</b>", buttons=keyCategoryAddD(getKAddD()))
    elif event.data.decode("utf-8").startswith("DESCRIZIONE"):
        p = event.data.decode("utf-8").split("_")[1]
        new_product["descrizionec"] = p
        check_products = "desc"
        await event.edit("✅ » Invia la descrizione (se vuoi toglierla scrivi None)",
                         buttons=[
                             [Button.inline('◀️', 'admin_panel')]])
    elif event.data == b"admin_panel":
        check_products = None
        await event.edit(f"<b>👮🏻‍♂ » Pannello admin</b>",
                         buttons=[
                             [Button.inline("🛠️Categorie🛠️", "edit_categorie")],
                             [Button.inline("🛠️Prodotti🛠️", "edit_prodotti")],
                             [Button.inline("📄​Comandi📄​", "comandilista")],
                             [Button.inline("👤Utenti👤", "stats")],
                             [Button.inline("❌Bannati❌", "bans")],
                             [Button.inline("🔐Attiva/Disattiva Canale🔐", "setc")],
                             [Button.inline("🏡", "home")]])

    elif event.data == b"comandilista":
        await event.edit(""" 
/ban userid 
/unban userid
/admin userid 
/unadmin userid 
/tos tos (imposta tos)
/ref prezzo (cambia la quota che viene data quando uno usa ref)
/add userid quota (aggiunge saldo)
/del userid quota (il contrario di add)
/mexstart mex (usabili: {mention}, {nome}, {username}, {saldo}) 
/linkpp link (aggiunge link paypal) 
/paypal testo (aggiunge testo paypal)
/bitcoin testo (aggiunge testo bitcoin)
/shop testo (aggiunge testo shop)
/post mex (messaggio globale)        
""", buttons=[[Button.inline("​🔙​", "admin_panel")]])
    elif event.data == b"bans":
        bans = await getBans()
        msg = "👥Utenti Bannati Nello Shop ⇣\n\n"
        if bans == []:
            msg = "❌ » Nessun utente bannato!"
        else:
            msg += "\n".join(map(str, bans))
        await event.edit(msg, buttons=[Button.inline("◀️", "admin_panel")])
    elif event.data == b"setc":
        if ccc:
            ccc = False
            await event.answer("❌", alert=True)
        else:
            ccc = True
            await event.answer("✅", alert=True)
    elif event.data == b"stats":
        if user.id in ADMIN:
            await event.edit(f"<b>👥UTENTI ATTIVI NEL BOT✅\n\n📊 Utenti Totali➯  ☆12{count()}☆</b>",
                             buttons=[
                                 [Button.inline("◀️", "home")]])
        else:
            await event.edit(f"<b>👥UTENTI ATTIVI NEL BOT✅\n\n📊 Utenti Totali➯  ☆12{count()}☆</b>",
                             buttons=[
                                 [Button.inline("◀️", "home")]])
    elif event.data == b"spc":
        text = ""
        for a, in conn.cursor().execute("SELECT chat_id FROM user").fetchall():
            try:
                ut = await client.get_entity(a)
                text += f"{ut.id} | {Menzione(ut.id, ut.first_name)}\n"
            except:
                text += str(ut.id) + "\n"
        if user.id in ADMIN:
            await event.edit(f"<b>👥UTENTI ATTIVI NEL BOT✅\n\n📊 Utenti Totali➯  ☆12{count()}☆</b>",
                             buttons=[
                                 [Button.inline("❌ Utenti Bannati ❌", "bans")],
                                 [Button.inline("◀️", "admin_panel")]])
        else:
            await event.answer("❌Non Sei Admin❌", alert=True)
    elif event.data == b"commands":
        await event.edit(
            f"<b>❓❓</b>\n\n<code>/ricarica + ID utente + saldo da aggiungere</code>\n<code>/rimuovi + ID utente + saldo da rimovere</code>\n<code>/post + messaggio da mandare come post</code>\n<code>/ban + ID utente </code>\n<code>/unban + ID utente </code>",
            buttons=[
                [Button.inline("🏡", "home")]])
    elif event.data == b"add_prodotto":
        if check_products == None:
            check_products = 1
            await event.edit("✅ » Inviami il nome del prodotto")
    elif event.data.decode("utf-8").startswith("category"):
        c = event.data.decode("utf-8").split("_")[1]
        error = 0
        try:
            due = keyboardccc(getProductsK(c))
        except:
            error += 1
        try:
            uno = sottokeyboard(c)
        except:
            error += 1
        tre = []
        try:
            for i in uno:
                tre.append(i)
            for u in due:
                tre.append(u)
        except:
            pass
        if not returnDesc(c):
            if error == 0:
                await event.edit(c, buttons=tre)
            else:
                await event.edit(c, buttons=[[Button.inline('◀️', 'shop')]])
        else:
            if error == 0:
                await event.edit(returnDesc(c), buttons=tre)
            else:
                await event.edit(returnDesc(c), buttons=[[Button.inline('◀️', 'shop')]])
    elif event.data.decode("utf-8").startswith("sotto"):
        c = event.data.decode("utf-8").split("_")[1]
        bottoni = getbuttonsotto(c)
        if not returnDescSOTTO(c):
            await event.edit(c, buttons=bottoni)
        else:
            await event.edit(returnDescSOTTO(c), buttons=bottoni)
    elif event.data.decode("utf-8").startswith("product"):
        user = await event.get_sender()
        p = event.data.decode("utf-8").split("_")[1]
        pr = getProducts(p)
        msg = (
                f"🔒Confermi l'acquisto di  {pr[0]} (x1)\n\n" +
                f"💰 ⇢ <code>{pr[2]}€</code>"
        )
        if p == pr[0]:
            await event.edit(msg, buttons=[[Button.inline('🛒 Acquista 🛒', f'buy_{pr[0]}_1'),   Button.inline('🔙indietro', 'shop')], 
                                           [Button.inline("➕", f"+_{p}_2"), Button.inline("➖", f"-_{p}_1")],
                                           [Button.inline('🔎 Verifica Disponibilità 🔍', f'dis_{pr[0]}')]]),
                                          
    elif event.data.decode().startswith("+") or event.data.decode().startswith("-"):
        p = event.data.decode().split("_")[1]
        n = event.data.decode().split("_")[2]
        pr = getProducts(p)
        st = int(n) - 1
        prezzo = round(float(pr[2]) * int(n), 2)
        p = event.data.decode("utf-8").split("_")[1]
        c = checker_file(p)
        cc = checker_testo(p)
        numm = None
        if not c and not cc:
            numm = 0
        elif cc:
            for r in conn.cursor().execute("SELECT testo FROM products WHERE name = ?", [p]).fetchall()[0]:
                if r == "account":
                    numm = account[p].__len__()
                else:
                    numm = 900.1
        elif c and cc:
            numm = 900.1
        elif c:
            numm = 900.1
        if st <= 0:
            st = 1
        if numm == 900.1:
            msg = (f"🔒Confermi l'acquisto di  {pr[0]} (x{str(n)})\n\n" +
                   f"💰 ⇢ <code>{prezzo}€</code>")
        elif int(n) <= numm:
            msg = (f"🔒Confermi l'acquisto di  {pr[0]} (x{str(n)})\n\n" +
                   f"💰 ⇢ <code>{prezzo}€</code>")
        else:
            await event.answer("❌Non puoi aggiungere il limite è stato superato!", alert=True)
        if p == pr[0] and int(n) <= numm:
            await event.edit(msg, buttons=[[Button.inline('🛒 Acquista 🛒', f'buy_{pr[0]}_{str(n)}'),  Button.inline('🔙indietro', 'shop')],
                                           [Button.inline("➕", f"+_{p}_{int(n) + 1}"),
                                            Button.inline("➖", f"-_{p}_{st}")],
                                           [Button.inline('🔎 Verifica Disponibilità 🔍', f'dis_{pr[0]}')]]),
                                       

    elif event.data.decode().startswith("delproduct"):
        delProduct(event.data.decode().split("_")[1])
        await event.edit("✅ » Prodotto eliminato",
                         buttons=[
                             [Button.inline('◀️', 'shop')]])

    elif event.data == b"delpro":
        prod = []
        for category in getKey():
            prodotti = getProductsKDEL(category)
            for x in prodotti:
                prod.append(x)
        await event.edit(
            f"🛍️Scegli Quale Prodotto Eliminare🛍️",
            buttons=keyboardDel(prod))
    elif event.data.decode("utf-8").startswith("buy"):
        user = await event.get_sender()
        p = event.data.decode("utf-8").split("_")[1]
        n = int(event.data.decode("utf-8").split("_")[2])
        saldo = get_saldo(user.id)
        product = getProducts(p)
        c = checker_file(p)
        cc = checker_testo(p)
        text = ""
        cred = ""
        scontr = ""
        prezzo = float(product[2]) * n
        if float(saldo) >= float(product[2]):
            if cc:
                if n > 1:
                    for x in range(0, n):
                        cred += get_account(p) + "\n"
                    text += f"<b>✅ Acquisto effettuato con successo</b>\n\nEcco il tuo account:\n\n{cred}"
                else:
                    for r in conn.cursor().execute("SELECT testo FROM products WHERE name = ?", [p]).fetchall()[0]:
                        if not r == "account":
                            text += r
                        else:
                            cred = get_account(p)
                            text += f"<b>✅ Acquisto effettuato con successo</b>\n\nEcco il tuo account:\n\n{cred}"
            else:
                text += "✅Iscritto✅"
            if not c and not cc:
                await event.answer("❌️Out Of Stock⇢ 0", alert=True)
            else:
                update_saldo(float(get_saldo(int(user.id))) - prezzo, user.id)
                try:
                    with open("lastId.txt", "r") as f:
                        lastId = int(f.read()) + 1
                    with open("lastId.txt", "w") as f:
                        f.write(str(lastId))
                except:
                    with open("lastId.txt", "w") as f:
                        lastId = 1
                        f.write("1")

                scontr = f"{p} | #{lastId} | x{n}"
                for f in ADMIN:
                    try:
                        await client.send_message(f,
                                                  f"<b>🧾Ricevuta</b>\n\n👤Utente » {Menzione(user.id, user.first_name)} ({user.id})\n🛍Prodotto » {scontr}\n💰Prezzo » {'%.2f' % prezzo}€")
                    except:
                        pass
                await event.respond(scontr, buttons=[[Button.inline('🏡', 'home')]])
                if c:
                    for r in conn.cursor().execute("SELECT file_premio FROM products WHERE name = ?", [p]).fetchall()[0]:
                        await event.delete()
                        await client.send_file(user.id, "file_premi/" + str(r), caption=text)
                else:
                    r = cur.execute("SELECT cron FROM user WHERE chat_id = ?", [user.id]).fetchone()[0]
                    if r == "None":
                        cur.execute("UPDATE user SET cron = ? WHERE chat_id = ?", [f"{scontr}", user.id])
                        conn.commit()
                    else:
                        cur.execute("UPDATE user SET cron = ? WHERE chat_id = ?", [f"{r}\n\n{scontr}", user.id])
                        conn.commit()
                    await event.edit(text)
        else:
            await event.answer("❌ ⇢ Saldo insufficiente", alert=True)
    elif event.data == b"add_give":
        key = await view(getProducts())
        await event.edit("<b>⚙️Scegli Quale Prodotto Modificare⚙️</b>", buttons=key)
    elif event.data.decode("utf-8").startswith("reset"):
        p = event.data.decode("utf-8").split("_")[1]
        try:
            conn.cursor().execute("UPDATE products SET testo = ? WHERE name = ?", ["vuoto", p])
        except:
            pass
        try:
            for r in conn.cursor().execute("SELECT file_premio FROM products WHERE name = ?", [p]).fetchall()[0]:
                os.remove("file_premi/" + str(r))
            conn.cursor().execute("UPDATE products SET file_premio = ? WHERE name = ?", ["vuoto", p])
            conn.commit()
        except:
            pass
            try:
                for a in account[p]:
                    account.remove(a)
                savesss()
            except:
                pass
        await event.answer("✅ » Resettato correttamente", alert=True)
    elif event.data.decode("utf-8").startswith("views"):
        user = await event.get_sender()
        p = event.data.decode("utf-8").split("_")[1]
        pr = getProducts(p)
        await event.edit("<b>📥Scegli Che Tipologia Di Prodotto Aggiungere📥</b>",
                         buttons=[
                             [Button.inline("📁File📁", f"file_{p}")],
                             [Button.inline("📚Testo📚", f"testo_{p}")],
                             [Button.inline("🔄Reset🔄", f"reset_{p}")],
                             [Button.inline("◀️", "add_give")]])
    elif event.data.decode("utf-8").startswith("dis"):
        user = await event.get_sender()
        p = event.data.decode("utf-8").split("_")[1]
        c = checker_file(p)
        cc = checker_testo(p)
        if not c and not cc:
            await event.answer("❌️Out Of Stock⇢ 0", alert=True)
        elif cc:
            for r in conn.cursor().execute("SELECT testo FROM products WHERE name = ?", [p]).fetchall()[0]:
                if r == "account":
                    await event.answer(f"✅️in Stock ⇢ {account[p].__len__()}", alert=True)
                else:
                    await event.answer(f"✅ ⇢ Prodotto Disponibile!", alert=True)
        elif c and cc:
            await event.answer(f"✅ ⇢ Prodotto Disponibile!", alert=True)
        elif c:
            await event.answer(f"✅ ⇢ Prodotto Disponibile!", alert=True)
    elif event.data.decode("utf-8").startswith("file"):
        p = event.data.decode("utf-8").split("_")[1]
        if check_products == None:
            check_products = 5
            new_product["faffa"] = p
            await event.edit("✅ » Invia il file")
    elif event.data.decode("utf-8").startswith("testo"):
        p = event.data.decode("utf-8").split("_")[1]
        await event.edit("<b>📜Scegli Cosa Aggiungere📜</b>", buttons=[[Button.inline("💈Account💈", f"account_{p}")],
                                                                       [Button.inline("✍🏻Testo✍🏻", f"scritto_{p}")],
                                                                       [Button.inline('◀️', 'add_give')]])
    elif event.data.decode("utf-8").startswith("account"):
        p = event.data.decode("utf-8").split("_")[1]
        if check_products == None:
            check_products = 6
            new_product["faffa"] = p
            conn.cursor().execute("UPDATE products SET testo = ? WHERE name = ?", ["account", p])
            conn.commit()
            await event.edit("✅ » Invia gli account")
    elif event.data.decode("utf-8").startswith("scritto"):
        p = event.data.decode("utf-8").split("_")[1]
        if check_products == None:
            check_products = 7
            new_product["faffa"] = p
            await event.edit("✅ » Invia il testo")
    elif event.data == b"delc":
        await event.edit("<b>📜Scegli Cosa Rimuovere📜</b>", buttons=keyCategoryDel(getKdel()))
    elif event.data.decode("utf-8").startswith("DEL"):
        p = event.data.decode("utf-8").split("_")[1]
        conn.cursor().execute("DELETE FROM category WHERE name = ?", [p])
        conn.cursor().execute("DELETE FROM products WHERE category = ?", [p])
        conn.commit()
        await event.edit("✅ » Categoria eliminata",
                         buttons=[
                             [Button.inline('◀️', 'admin_panel')]])
# ===============================#

print("Bot Status [ON]")
client.run_until_disconnected()
