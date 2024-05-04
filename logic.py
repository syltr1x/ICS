import json, time, os, subprocess as sp, ctypes, sys

def create_config():
    version_key = str(sp.check_output('curl.exe https://raw.githubusercontent.com/syltr1x/ICS/main/version_mgt/vkey', shell=True))[2:] # Obtener clave de version
    sp.check_output('curl.exe https://raw.githubusercontent.com/syltr1x/ICS/main/vehicles.json -o data/vehicles.json', shell=True) # Obtener lista de vehiculos
    file = open('data/config.json', 'w')
    file.write('{\n    "vkey":"'+version_key+'",\n    "path":"",\n    "mode":"system",\n    "theme":"red",\n    "mechanics":""\n}')
    file.close()
    open('data/account.json', 'w').close()
    open('data/balance.json', 'w').close()
    open('data/budget.json', 'w').close()
    open('data/car.json', 'w').close()
    open('data/customer.json', 'w').close()
    open('data/history.json', 'w').close()
    open('data/inventory.json', 'w').close()
    open('data/work.json', 'w').close()

def get_config():
    if not os.path.exists('data'):
        os.mkdir('data')
        os.mkdir('data/temp')
        create_config()
    config = json.loads(open('data/config.json', 'r', encoding='utf-8').read())
    return config

def mod_config(datos):
    file = open("data/config.json", "r", encoding='utf8'); data = json.loads(file.read()); file.close()
    for dato in datos:
        if dato["field"] == "theme":
            theme = dato["value"]
            if theme.lower() != "red" and theme != "blue" and theme != "green" and theme != "purple" and theme != "yellow":
                colors = {"rojo":"red", "azul":"blue", "verde":"green", "morado":"purple", "amarillo":"yellow"}
                dato["value"] = colors[theme.lower()]
            else: dato["value"] = theme.lower()
        if dato["field"] == "mode":
            mode = dato["value"]
            if mode.lower() != "system" and mode.lower() != "dark" and mode.lower() != "light":
                modes = {"oscuro":"dark", "sistema":"system", "claro":"light"}
                dato["value"] = modes[mode.lower()]
            else: dato["value"] = mode.lower()
        data[dato["field"]] = dato["value"]
    file = open("data/config.json", "w", encoding='utf8')
    file.write('{\n    "vkey":"'+data["vkey"]+'",\n    "path":"'+data["path"].replace("\\","\\\\")+'",\n    "mode":"'+data["mode"]+'",\n    "theme":"'+data["theme"]+'",\n    "mechanics":"'+data["mechanics"]+'"\n}')
    file.close()

def get_date():
    data = str(time.localtime()).split(',')
    year = data[0][-4:].replace("=","")
    month = data[1][-2:].replace("=","")
    day = data[2][-2:].replace("=","")
    return f"{day}/{month}/{year}"

def get_id(data):
    if data == "account.json": data = open("data/account.json", "r", encoding='utf-8').read()
    if data == "customer.json": data = open("data/customer.json", "r", encoding='utf-8').read()
    if data == "work.json": data = open("data/work.json", "r", encoding='utf-8').read()
    if data == "budget.json": data = open("data/budget.json", "r", encoding='utf-8').read()
    if len(data) < 4: return "0"
    dato = json.loads(data[:-1][1:].replace("},", "}},").split("},")[-1])
    return str(int(dato["id"])+1)

def order_id(filename):
    if filename != "account.json" and filename != "customer.json" and filename != "work.json" and filename != "history.json" and filename != "balance.json": return 0
    file = open(f"data/{filename}", "r", encoding='utf8')
    dato = file.read()
    dato = dato[:-1][1:].replace("},", "}},").split("},") if filename != "balance.json" else dato[:-1][1:].replace(",{", ",{{").split(",{")
    file.close()
    cntr = "0"
    data = []
    if type(dato) != list and len(dato) < 5: return 0
    if type(dato) == list and dato == [''] or []: return 0
    open(f'data/{filename}', 'w', encoding='utf8').write('')
    # Order para Balance
    if filename == "balance.json":
        dates = []
        for d in dato:
            movements = []
            d = json.loads(d)
            cntr = 0
            for m in d["movements"]:
                m["id"] = cntr
                cntr += 1
                movements.append(m)
            d["movements"] = movements
            dates.append(d)
        file = open(f"data/{filename}", 'w', encoding='utf8')
        file.write("[")
        for d in dates:
            if dates.index(d) != 0: file.write('\n    ,{\n        "date":"'+d["date"]+'",\n        "balance":"'+d["balance"]+'",\n        "movements":[')
            else: file.write('\n    {\n        "date":"'+d["date"]+'",\n        "balance":"'+d["balance"]+'",\n        "movements":[')
            for m in d["movements"]:
                if d["movements"].index(m) != len(d["movements"])-1: file.write('\n            {'+f'"id":"{m["id"]}", "client":"{m["client"]}", "mecanico":"{m["mecanico"]}", "price":"{m["price"]}", "desc":"{m["desc"]}"'+'},')
                else: file.write('\n            {'+f'"id":"{m["id"]}", "client":"{m["client"]}", "mecanico":"{m["mecanico"]}", "price":"{m["price"]}", "desc":"{m["desc"]}"'+'}')
            file.write(']' if len(d["movements"])-1 < 0 else '\n        ]')
            file.write('\n    }')
        file.write('\n]')
        return 0
    # Order para el resto de archivos
    for d in dato:
        d = json.loads(d)
        d["id"] = cntr
        if filename == "account.json": data.append('{"id":"'+d["id"]+'", "name":"'+d["name"]+'", "balance":"'+d["balance"]+'", "contact":'+str(d["contact"]).replace("'", '"')+', "cars":'+str(d["cars"]).replace("'", '"')+'}')
        elif filename == "customer.json": data.append('{"id":"'+d["id"]+'", "name":"'+d["name"]+'", "lastname":"'+d["lastname"]+'", "birthday":"'+d["birthday"]+'", "contact":'+str(d["contact"]).replace("'", '"')+', "cars":'+str(d["cars"]).replace("'", '"')+'}')
        elif filename == "work.json": data.append('{"id":"'+d["id"]+'", "customer":"'+d["customer"]+'", "lcplate":"'+d["lcplate"]+'", "entrydt":"'+d["entrydt"]+'", "technician":"'+d["technician"]+'", "diagnostic":"'+d["diagnostic"]+'", "exitdt":"'+d["exitdt"]+'", "work":"'+str(d["work"])+'", "price":"'+d["price"]+'", "pd":"'+d["pd"]+'", "payed":"'+d["payed"]+'", "status":"'+d["status"]+'"}')
        elif filename == "history.json": data.append('{"id":"'+d["id"]+'", "customer":"'+d["customer"]+'", "lcplate":"'+d["lcplate"]+'", "entrydt":"'+d["entrydt"]+'", "technician":"'+d["technician"]+'", "diagnostic":"'+d["diagnostic"]+'", "exitdt":"'+d["exitdt"]+'", "work":"'+str(d["work"])+'", "price":"'+d["price"]+'", "pd":"'+d["pd"]+'", "payed":"'+d["payed"]+'", "status":"'+d["status"]+'"}')
        elif filename == "budget.json": data.append('{"id":"'+d["id"]+'", "customer":"'+d["customer"]+'", "lcplate":"'+d["lcplate"]+'", "technician":"'+d["technician"]+'", "entrydt":"'+d["entrydt"]+'", "diagnostic":"'+d["diagnostic"]+'", "work":'+str(d["work"]).replace("'", '"')+', "price":"'+d["price"]+'", "pd":"'+d["pd"]+'"}')
        cntr = str(int(cntr)+1)
    for i in data:
        if filename == "account.json": write_account('', i)
        elif filename == "customer.json": write_customer('', i)
        elif filename == "work.json": write_works('', i)
        elif filename == "history.json": write_history('', i)
        elif filename == "budget.json": write_budget('', i)
            
def update_prices(id, file):
    data = str(time.localtime()).split(',')
    year = data[0][-4:].replace("=","")
    month = data[1][-2:].replace("=","")
    day = data[2][-2:].replace("=","")
    date = day+"/"+month+"/"+year
    jobs = []
    jp = 0
    work = get_works("id", id, "strict")[0] if file == "works" else get_budget("id", id, "strict")[0]
    data = work["work"]
    dato = open("data/inventory.json", "r").read()[:-1][1:].replace("},","}},").split("},")
    for i in data:
        for x in dato:
            x = json.loads(x)
            if i["item"].lower() == x["item"].lower():
                jobs.append({"item":i["item"], "price":str(int(x["price"])*int(i["quantity"])), "quantity":i["quantity"]})
                jp = jp + int(x["price"])*int(i["quantity"])
    remove_data('work.json' if file == "works" else 'budget.json', id, 'id')
    if file == "works": write_works("", '{"id":"'+id+'", "customer":"'+work["customer"]+'", "lcplate":"'+work["lcplate"]+'", "entrydt":"'+work["entrydt"]+'", "technician":"'+work["technician"]+'", "diagnostic":"'+work["diagnostic"]+'", "exitdt":"'+work["exitdt"]+'", "work":'+str(jobs).replace("'", '"')+', "price":"'+str(jp)+'", "pd":"'+date+'", "payed":"'+work["payed"]+'", "status":"'+work["status"]+'"}')
    else: write_budget("", '{"id":"'+id+'", "customer":"'+work["customer"]+'", "lcplate":"'+work["lcplate"]+'", "entrydt":"'+work["entrydt"]+'", "technician":"'+work["technician"]+'", "diagnostic":"'+work["diagnostic"]+'", "work":'+str(jobs).replace("'", '"')+', "price":"'+str(jp)+'", "pd":"'+date+'"}')

def pay_work(date, id, pay, data, mecanico):
    if pay != "total":
        mod_data(id, "id", "payed", str(int(get_works("id", id, "strict")[0]["payed"])+pay), "work.json")
    else:
        mod_data(id, "id", "payed", get_works("id", id, "strict")[0]["price"], "work.json")
        mod_data(id, "id", "status", "pagado", "work.json")
    price = pay if pay != "total" else get_works("id", id, "strict")[0]["price"]
    if type(get_balance("date", date, "strict")) == str:
        movements = [{"id":"0", "client":get_works("id", id, "strict")[0]["customer"], "mecanico":mecanico, "price":str(pay), "desc":data}]
        write_balance('', '{"date":"'+date+'", "balance":"'+str(price)+'", "movements":'+str(movements).replace("'",'"')+'}')
    else:
        add_balance(date, get_works("id", id, "strict")[0]["customer"], mecanico, price, data)

def add_balance(date, client, tech, price, desc):
    movements = []
    dato = open('data/balance.json', "r", encoding='utf8').read()
    dato = dato[:-1][1:].replace(",{", ",{{").split(",{")
    for d in dato:
        if json.loads(d)["date"] == date:
            movements = json.loads(d)["movements"]
            break
    nbalance = str(int(get_balance("date", date, "strict")[0]["balance"])+int(price))
    movements.append({"id":str(len(movements)),"client":client, "mecanico":tech, "price":str(price), "desc":desc})
    mod_data(date, "date", "movements", movements, "balance.json")
    mod_data(date, "date", "balance", nbalance, "balance.json")

def del_balance(date, id):
    dato = open('data/balance.json', "r", encoding='utf8').read()
    dato = dato[:-1][1:].replace(",{", ",{{").split(",{")
    for d in dato:
        d = json.loads(d)
        if date == d["date"]:
            balance = d["balance"]
            movements = d["movements"]
            break
    for m in movements: 
        if id == m["id"]:
            price = m["price"]
            movements.remove(m)
            break
    mod_data(date, "date", "movements", movements, "balance.json")
    mod_data(date, "date", "balance", str(int(balance)-int(price)), "balance.json")

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin(updater_path):
    if is_admin():
        sp.Popen([updater_path, get_config()["path"]])

    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        run_as_admin(updater_path)

def update_app():
    updater_filename = "updater.exe"
    updater_path = os.path.join(os.path.dirname(get_config()["path"]), updater_filename)
    os.system(f'powershell -c "curl.exe https://raw.githubusercontent.com/syltr1x/ICS/main/{updater_filename} -o {updater_path}"')
    run_as_admin(updater_path)
    sp.Popen([updater_path, get_config()["path"]])
    exit()
    
def get_customer(filter, value, mode):
    with open("data/customer.json", "r", encoding="utf-8") as cDF: data = cDF.read(); cDF.close()
    data = data[:-1][1:].replace("},", "}},").split("},")
    datos = []
    for dato in data:
        item = json.loads(dato)
        if mode == "strict" and filter == "lcplate":
            for plate in item["lcplate"]:
                if value.lower() == plate.lower(): datos.append(item)
        if mode == "relaxed" and filter == "lcplate":
            for plate in item["lcplate"]:
                if value.lower() in plate.lower(): datos.append(item)
        elif mode == "strict" and value.lower() == item[filter].lower(): datos.append(item)
        elif mode == "relaxed" and value.lower() in item[filter].lower(): datos.append(item)
        elif data.index(dato) == len(data)-1 and datos == []: return "Err: No existen clientes..."
    return datos

def get_account(filter, value, mode):
    with open("data/account.json", encoding="utf-8") as aDF: data = aDF.read(); aDF.close()
    data = data[:-1][1:].replace("},","}},").split("},")
    datos = []
    for dato in data:
        item = json.loads(dato)
        if mode == "strict" and value.lower() == item[filter].lower(): datos.append(item)
        elif mode == "relaxed" and value.lower() in item[filter].lower(): datos.append(item)
    return datos

def get_budget(filter, value, mode):
    with open("data/budget.json", "r", encoding="utf-8") as wDF: data = wDF.read(); wDF.close()
    data = data[:-1][1:].replace("},","}},").split("},")
    datos = []
    for dato in data:
        item = json.loads(dato)
        if mode == "strict" and value.lower() == item[filter].lower(): datos.append(item)
        elif mode == "relaxed" and value.lower() in item[filter].lower(): datos.append(item)
        elif data.index(dato) == len(data)-1 and datos == []: return "Err: No existen presupuestos..."
    return datos

def get_works(filter, value, mode):
    with open("data/work.json", "r", encoding="utf-8") as wDF: data = wDF.read(); wDF.close()
    data = data[:-1][1:].replace("},","}},").split("},")
    datos = []
    for dato in data:
        item = json.loads(dato)
        if mode == "strict" and value.lower() == item[filter].lower(): datos.append(item)
        elif mode == "relaxed" and value.lower() in item[filter].lower(): datos.append(item)
        elif data.index(dato) == len(data)-1 and datos == []: return "Err: No existen trabajos..."
    return datos

def get_cars(filter, value, mode):
    with open("data/car.json","r", encoding="utf-8") as vDF: data = vDF.read(); vDF.close()
    data = data[:-1][1:].replace("},","}},").split("},")
    datos = []
    for dato in data:
        item = json.loads(dato)
        if mode == "strict" and value == item[filter]: datos.append(item)
        elif mode == "relaxed" and value.lower() in item[filter].lower(): datos.append(item)
        elif data.index(dato) == len(data)-1 and datos == []: return "Err: No existen autos..."
    return datos
        
def get_product(filter, value, mode):
    with open("data/inventory.json","r", encoding="utf-8") as pDF: data = pDF.read(); pDF.close()
    data = data[:-1][1:].replace("},","}},").split("},")
    datos = []
    for dato in data:
        item = json.loads(dato)
        if mode == "strict" and value.lower() == item[filter].lower():
            datos.append(item)
        elif mode == "relaxed" and value.lower() in item[filter].lower(): datos.append(item)
        elif data.index(dato) == len(data)-1 and datos == []: return "Err: No existen productos..."
    return datos

def get_balance(filter, value, mode):
    with open("data/balance.json", "r", encoding="utf-8") as bDF: data = bDF.read(); bDF.close()
    data = data[:-1][1:].replace(",{", ",{{").split(",{")
    datos = []
    for dato in data:
        item = json.loads(dato)
        if mode == "strict" and value.lower() == item[filter].lower():datos.append(item)
        elif mode == "relaxed" and value.lower() in item[filter].lower():datos.append(item)
        elif data.index(dato) == len(data)-1 and datos == []: return "Err: No existe Balance"
    return datos

def get_history(filter, value, mode):
    with open("data/history.json", "r", encoding="utf-8") as hDF: data = hDF.read(); hDF.close()
    data = data[:-1][1:].replace("},", "}},").split("},")
    datos = []
    for dato in data:
        item = json.loads(dato)
        if mode == "strict" and value.lower() == item[filter].lower():datos.append(item)
        elif mode == "relaxed" and value.lower() in item[filter].lower():datos.append(item)
        elif data.index(dato) == len(data)-1 and datos == []: return "Err: No existe Historial"
    return datos

def write_cars(dato, write):
    dF = open("data/car.json", "r", encoding="utf-8")
    data = dF.read()
    data = data[:-1][1:].replace("},","}},").split("},") if len(data) > 5 else []
    data.append(write) if write != "" else None
    dato = str(dato)[:-1][1:]
    for d in data:
        if str(json.loads(d)) == dato: data.remove(d); break
    dF.close()
    dF = open("data/car.json", "w", encoding='utf-8')
    dF.write("[")
    for dato in data:
        item = json.loads(dato)
        if data.index(dato) != len(data)-1: dF.write('\n    {\n        "lcplate":"'+item["lcplate"]+'",\n        "color":"'+item["color"]+'",\n        "make":"'+item["make"]+'",\n        "model":"'+item["model"]+'",\n        "type":"'+item["type"]+'",\n        "year":"'+item["year"]+'"\n    },')
        else: dF.write('\n    {\n        "lcplate":"'+item["lcplate"]+'",\n        "color":"'+item["color"]+'",\n        "make":"'+item["make"]+'",\n        "model":"'+item["model"]+'",\n        "type":"'+item["type"]+'",\n        "year":"'+item["year"]+'"\n    }')
    dF.write('\n]')
    dF.close()

def write_customer(dato, write):
    file = open("data/customer.json", "r", encoding="utf-8")
    data = file.read()
    data = data[:-1][1:].replace("},","}},").split("},") if len(data) > 5 else []
    data.append(write) if write != "" else None
    dato = str(dato)[:-1][1:]
    data = [x for x in data if x != '']
    for d in data:
        if str(json.loads(d)) == dato: data.remove(d); break
    file.close()
    dF = open("data/customer.json", "w", encoding='utf-8')
    dF.write("[")

    for dato in data:
        item = json.loads(dato)
        item["contact"] = str(item["contact"]).replace("'", '"').replace("}, {", "}}, {{")[:-1][1:].split("}, {")
        dF.write('\n    {\n        "id":"'+item["id"]+'",\n        "name":"'+item["name"]+'",\n        "lastname":"'+item["lastname"]+'",\n        "birthday":"'+item["birthday"]+'",\n        "contact":[')
        if item["contact"] != [] and item["contact"] != ['']:
            for x in item["contact"]:
                i = str(x).replace("'", '"')
                i = json.loads(i)
                if 0 != item["contact"].index(x): dF.write('\n            ,{\n                "media":"'+i["media"]+'",\n                "value":"'+i["value"]+'"\n            }')
                else: dF.write('\n            {\n                "media":"'+i["media"]+'",\n                "value":"'+i["value"]+'"\n            }')
            dF.write('\n        ],\n        "cars":[')
        else: dF.write('],\n        "cars":[')
        if item["cars"] != []: 
            for y in item["cars"]: dF.write(f'"{y}", ' if item["cars"].index(y) != len(item["cars"])-1 else f'"{y}"]')
        else: dF.write(']') 
        dF.write('\n    },' if data.index(dato) != len(data)-1 else '\n    }')
    dF.write('\n]')
    dF.close()

def write_account(dato, write):
    dF = open("data/account.json", "r", encoding="utf-8")
    data = dF.read()
    data = data[:-1][1:].replace("},","}},").split("},") if len(data) > 5 else []
    data.append(write) if write != "" else None
    dato = str(dato)[:-1][1:]
    data = [x for x in data if x != '']
    for d in data:
        if str(json.loads(d)) == dato: data.remove(d); break
    dF.close()
    dF = open("data/account.json", "w", encoding='utf-8')
    dF.write("[")
    for dato in data:
        item = json.loads(dato)
        item["contact"] = str(item["contact"]).replace("'", '"').replace("}, {", "}}, {{")[:-1][1:].split("}, {")
        dF.write('\n    {\n        "id":"'+item["id"]+'",\n        "name":"'+item["name"]+'",\n        "balance":"'+item["balance"]+'",\n        "contact":[')
        if item["contact"] != [] and item["contact"] != [""]:
            for x in item["contact"]:
                i = str(x).replace("'", '"')
                i = json.loads(i)
                if 0 != item["contact"].index(x): dF.write('\n            ,{\n                "media":"'+i["media"]+'",\n                "value":"'+i["value"]+'"\n            }')
                else: dF.write('\n            {\n                "media":"'+i["media"]+'",\n                "value":"'+i["value"]+'"\n            }')
            dF.write('\n        ],\n        "cars":[')
        else: dF.write('],\n        "cars":[')
        if item["cars"] != []: 
            for y in item["cars"]: dF.write(f'"{y}", ' if item["cars"].index(y) != len(item["cars"])-1 else f'"{y}"]')
        else: dF.write(']')
        dF.write('\n    },' if data.index(dato) != len(data)-1 else '\n    }')
    dF.write('\n]')
    dF.close()

def write_balance(dato, write):
    dF = open("data/balance.json", "r", encoding="utf-8")
    data = dF.read()
    data = data[:-1][1:].replace(",{",",{{").split(",{") if len(data) > 5 else []
    data.append(write) if write != "" else None
    dato = str(dato)[:-1][1:]
    data = [x for x in data if x != '']
    for d in data:
        if str(json.loads(d)) == dato: data.remove(d); break
    dF.close()
    dF = open("data/balance.json", "w", encoding="utf-8")
    dF.write("[")
    for dato in data:
        item = json.loads(dato)
        if data.index(dato) == 0: dF.write('\n    {\n        "date":"'+item["date"]+'",\n        "balance":"'+item["balance"]+'",\n        "movements":[')
        else: dF.write('\n    ,{\n        "date":"'+item["date"]+'",\n        "balance":"'+item["balance"]+'",\n        "movements":[')
        if len(item["movements"]) >= 1:
            for x in item["movements"]:
                i = str(x).replace("'",'"')
                i = json.loads(i)
                if item["movements"].index(x) != len(item["movements"])-1: dF.write('\n            {"id":"'+i["id"]+'", "client":"'+i["client"]+'", "mecanico":"'+i["mecanico"]+'", "price":"'+i["price"]+'", "desc":"'+i["desc"]+'"},')
                else: dF.write('\n            {"id":"'+i["id"]+'", "client":"'+i["client"]+'", "mecanico":"'+i["mecanico"]+'", "price":"'+i["price"]+'", "desc":"'+i["desc"]+'"}\n        ]')
        else:
            dF.write(']')
        dF.write('\n    }')
    dF.write('\n]')

def write_works(dato, write):
    dF = open("data/work.json", "r", encoding="utf-8")
    data = dF.read()
    data = data[:-1][1:].replace("},","}},").split("},") if len(data) > 5 else []
    data.append(write) if write != "" else None
    dato = str(dato)[:-1][1:]
    data = [x for x in data if x != '']
    for d in data:
        if str(json.loads(d)) == dato: data.remove(d); break
    dF.close()
    dF = open("data/work.json", "w", encoding='utf-8')
    dF.write("[")
    for dato in data:
        item = json.loads(dato)
        item["work"] = str(item["work"]).replace("'", '"').replace("}, {", "}}, {{")[:-1][1:].split("}, {")
        dF.write('\n    {\n        "id":"'+item["id"]+'",\n        "customer":"'+item["customer"]+'",\n        "lcplate":"'+item["lcplate"]+'",\n        "entrydt":"'+item["entrydt"]+'",\n        "technician":"'+item["technician"]+'",\n        "diagnostic":"'+item["diagnostic"]+'",\n        "exitdt":"'+item["exitdt"]+'",\n        "work":[')
        for x in item["work"]:
            i = str(x).replace("'", '"')
            i = json.loads(i)
            if 0 != item["work"].index(x): dF.write('\n            ,{\n                "item":"'+i["item"]+'",\n                "price":"'+i["price"]+'",\n                "quantity":"'+i["quantity"]+'"\n            }')
            else: dF.write('\n            {\n                "item":"'+i["item"]+'",\n                "price":"'+i["price"]+'",\n                "quantity":"'+i["quantity"]+'"\n            }')
        if len(data)-1 != data.index(dato): dF.write('\n        ],\n        "price":"'+item["price"]+'",\n        "pd":"'+item["pd"]+'",\n        "payed":"'+item["payed"]+'",\n        "status":"'+item["status"]+'"\n    },')
        else: dF.write('\n        ],\n        "price":"'+item["price"]+'",\n        "pd":"'+item["pd"]+'",\n        "payed":"'+item["payed"]+'",\n        "status":"'+item["status"]+'"\n    }')
    dF.write('\n]')

def write_budget(dato, write):
    dF = open("data/budget.json", "r", encoding="utf-8")
    data = dF.read()
    data = data[:-1][1:].replace("},","}},").split("},") if len(data) > 5 else []
    data.append(write) if write != "" else None
    dato = str(dato)[:-1][1:]
    data = [x for x in data if x != '']
    for d in data:
        if str(json.loads(d)) == dato: data.remove(d); break
    dF.close()
    dF = open("data/budget.json", "w", encoding='utf-8')
    dF.write("[")
    for dato in data:
        item = json.loads(dato)
        item["work"] = str(item["work"]).replace("'", '"').replace("}, {", "}}, {{")[:-1][1:].split("}, {")
        dF.write('\n    {\n        "id":"'+item["id"]+'",\n        "customer":"'+item["customer"]+'",\n        "lcplate":"'+item["lcplate"]+'",\n        "entrydt":"'+item["entrydt"]+'",\n        "technician":"'+item["technician"]+'",\n        "diagnostic":"'+item["diagnostic"]+'",\n        "work":[')
        for x in item["work"]:
            i = str(x).replace("'", '"')
            i = json.loads(i)
            if 0 != item["work"].index(x): dF.write('\n            ,{\n                "item":"'+i["item"]+'",\n                "price":"'+i["price"]+'",\n                "quantity":"'+i["quantity"]+'"\n            }')
            else: dF.write('\n            {\n                "item":"'+i["item"]+'",\n                "price":"'+i["price"]+'",\n                "quantity":"'+i["quantity"]+'"\n            }')
        if len(data)-1 != data.index(dato): dF.write('\n        ],\n        "price":"'+item["price"]+'",\n        "pd":"'+item["pd"]+'"\n    },')
        else: dF.write('\n        ],\n        "price":"'+item["price"]+'",\n        "pd":"'+item["pd"]+'"\n    }')
    dF.write('\n]')

def write_product(dato, write):
    dF = open("data/inventory.json", "r", encoding="utf-8")
    data = dF.read()
    data = data[:-1][1:].replace("},","}},").split("},") if len(data) > 5 else []
    data.append(write) if write != "" else None
    dato = str(dato)[:-1][1:]
    data = [x for x in data if x != '']
    for d in data:
        if str(json.loads(d)) == dato: data.remove(d); break
    dF.close()
    dF = open("data/inventory.json", "w", encoding='utf-8')
    dF.write("[")
    for dato in data:
        item = json.loads(dato)
        if data.index(dato) != len(data)-1: dF.write('\n    {\n        "item":"'+item["item"]+'",\n        "price":"'+item["price"]+'",\n        "stock":"'+item["stock"]+'"\n    },')
        else: dF.write('\n    {\n        "item":"'+item["item"]+'",\n        "price":"'+item["price"]+'",\n        "stock":"'+item["stock"]+'"\n    }')
    dF.write('\n]')
    dF.close()

def write_history(dato, write):
    dF = open("data/history.json", "r", encoding="utf-8")
    data = dF.read()
    data = data[:-1][1:].replace("},","}},").split("},") if len(data) > 5 else []
    data.append(write) if write != "" else None
    dato = str(dato)[:-1][1:]
    data = [x for x in data if x != '']
    for d in data:
         if str(json.loads(d)) == dato: data.remove(d); break
    dF.close()
    timedate = str(time.localtime()).split(',')
    year = timedate[0][-4:].replace("=","")
    month = timedate[1][-2:].replace("=","")
    day = timedate[2][-2:].replace("=","")
    hour = timedate[3][-2:].replace("=","")+":"+timedate[4][-2:].replace("=","")+":"+timedate[5][-2:].replace("=","")

    datetime = day+"/"+month+"/"+year+" , "+hour
    dF = open("data/history.json", "w", encoding='utf-8')
    dF.write("[")
    for dato in data:
        item = json.loads(dato)
        if item["exitdt"] == "--/--/---- , --:--:--": item["exitdt"] = datetime
        item["work"] = str(item["work"]).replace("'", '"').replace("}, {", "}}, {{")[:-1][1:].split("}, {")
        dF.write('\n    {\n        "id":"'+item["id"]+'",\n        "customer":"'+item["customer"]+'",\n        "lcplate":"'+item["lcplate"]+'",\n        "entrydt":"'+item["entrydt"]+'",\n        "technician":"'+item["technician"]+'",\n        "diagnostic":"'+item["diagnostic"]+'",\n        "exitdt":"'+item["exitdt"]+'",\n        "work":[')
        for x in item["work"]:
            i = str(x).replace("'", '"')
            i = json.loads(i)
            if 0 != item["work"].index(x): dF.write('\n            ,{\n                "item":"'+i["item"]+'",\n                "price":"'+i["price"]+'",\n                "quantity":"'+i["quantity"]+'"\n            }')
            else: dF.write('\n            {\n                "item":"'+i["item"]+'",\n                "price":"'+i["price"]+'",\n                "quantity":"'+i["quantity"]+'"\n            }')
        if len(data)-1 != data.index(dato): dF.write('\n        ],\n        "price":"'+item["price"]+'",\n        "pd":"'+item["pd"]+'",\n        "payed":"'+item["payed"]+'",\n        "status":"'+item["status"]+'"\n    },')
        else: dF.write('\n        ],\n        "price":"'+item["price"]+'",\n        "pd":"'+item["pd"]+'",\n        "payed":"'+item["payed"]+'",\n        "status":"'+item["status"]+'"\n    }')
    dF.write('\n]')

def remove_data(filename, value, field):
    if filename == "car.json":
        dato = get_cars(field, value, "strict")
        write_cars(dato, "")
    elif filename == "customer.json":
        dato = get_customer(field, value, "strict")
        write_customer(dato, "")
    elif filename == "work.json":
        dato = get_works(field, value, "strict")
        write_works(dato, "")
    elif filename == "budget.json":
        dato = get_budget(field, value, "strict")
        write_budget(dato, "")
    elif filename == "inventory.json":
        dato = get_product(field, value, "strict")
        write_product(dato, "")
    elif filename == "account.json":
        dato = get_account(field, value, "strict")
        write_account(dato, "")
    elif filename == "balance.json":
        dato = get_balance(field, value, "strict")
        write_balance(dato, "")
    elif filename == "history.json":
        dato = get_history(field, value, "strict")
        write_history(dato, "")

def mod_data(value, filter, field, newValue, filename):
    with open(f"data/{filename}", "r") as dF: data = dF.read(); dF.close()
    data = data[:-1][1:].replace("},","}},").split("},") if filename != "balance.json" else data[:-1][1:].replace(",{",",{{").split(",{")
    for dato in data:
        item = json.loads(dato)
        if item[filter] == value:
            remove_data(filename, value, filter)
            if filename == "car.json":
                item[field] = newValue
                write_cars("", '{"lcplate":"'+item["lcplate"]+'", "color":"'+item["color"]+'", "make":"'+item["make"]+'", "model":"'+item["model"]+'", "type":"'+item["type"]+'", "year":"'+item["year"]+'"}')
            elif filename == "balance.json":
                item[field] = newValue
                write_balance("", '{"date":"'+item["date"]+'", "balance":"'+item["balance"]+'", "movements":'+str(item["movements"]).replace("'", '"')+'}')
            elif filename == "history.json":
                item[field] = newValue
                write_history("", '{"id":"'+item["id"]+'", "customer":"'+item["customer"]+'", "lcplate":"'+item["lcplate"]+'", "entrydt":"'+item["entrydt"]+'", "diagnostic":"'+item["diagnostic"]+'", "exitdt":"'+item["exitdt"]+'", "work":'+str(item["work"]).replace("'", '"')+', "price":"'+item["price"]+'", "status":"'+item["status"]+'"}')
            elif filename == "account.json":
                item[field] = newValue
                write_account("", '{"id":"'+item["id"]+'", "name":"'+item["name"]+'", "balance":"'+item["balance"]+'", "contact":'+str(item["contact"]).replace("'", '"')+', "cars":'+str(item["cars"]).replace("'", '"')+'}')
            elif filename == "customer.json":
                item[field] = newValue
                write_customer("", '{"id":"'+item["id"]+'", "name":"'+item["name"]+'", "lastname":"'+item["lastname"]+'", "birthday":"'+item["birthday"]+'", "contact":'+str(item["contact"]).replace("'", '"')+', "cars":'+str(item["cars"]).replace("'", '"')+'}')
            elif filename == "work.json":
                item[field] = newValue
                write_works("", '{"id":"'+item["id"]+'", "customer":"'+item["customer"]+'", "lcplate":"'+item["lcplate"]+'", "technician":"'+item["technician"]+'", "entrydt":"'+item["entrydt"]+'", "diagnostic":"'+item["diagnostic"]+'", "exitdt":"'+item["exitdt"]+'", "work":'+str(item["work"]).replace("'", '"')+', "price":"'+item["price"]+'", "payed":"'+item["payed"]+'", "pd":"'+item["pd"]+'", "status":"'+item["status"]+'"}')
            elif filename == "budget.json":
                item[field] = newValue
                write_budget("", '{"id":"'+item["id"]+'", "customer":"'+item["customer"]+'", "lcplate":"'+item["lcplate"]+'", "technician":"'+item["technician"]+'", "entrydt":"'+item["entrydt"]+'", "diagnostic":"'+item["diagnostic"]+'", "work":'+str(item["work"]).replace("'", '"')+', "price":"'+item["price"]+'", "pd":"'+item["pd"]+'"}')
            elif filename == "inventory.json":
                item[field] = newValue
                write_product("", '{"item":"'+item["item"]+'", "price":"'+item["price"]+'", "stock":"'+item["stock"]+'"}')
            break