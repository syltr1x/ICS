import json, time

def get_id(data):
    if data == "account.json": data = open("data/account.json").read()
    if data == "customer.json": data = open("data/customer.json").read()
    if data == "work.json": data = open("data/work.json").read()

    dato = json.loads(data[:-1][1:].replace("},", "}},").split("},")[-1])
    return str(int(dato["id"])+1)

def get_customer(filter, value, mode):
    with open("data/customer.json", "r") as cDF: data = cDF.read(); cDF.close()
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
    with open("data/account.json") as aDF: data = aDF.read(); aDF.close()
    data = data[:-1][1:].replace("},","}},").split("},")
    datos = []
    for dato in data:
        item = json.loads(dato)
        if mode == "strict" and value.lower() == item[filter].lower(): datos.append(item)
        elif mode == "relaxed" and value.lower() in item[filter].lower(): datos.append(item)
    return datos

def get_works(filter, value, mode):
    with open("data/work.json", "r") as wDF: data = wDF.read(); wDF.close()
    data = data[:-1][1:].replace("},","}},").split("},")
    datos = []
    for dato in data:
        item = json.loads(dato)
        if mode == "strict" and value.lower() == item[filter].lower(): datos.append(item)
        elif mode == "relaxed" and value.lower() in item[filter].lower(): datos.append(item)
        elif data.index(dato) == len(data)-1 and datos == []: return "Err: No existen trabajos..."
    return datos

def get_cars(filter, value, mode):
    with open("data/car.json","r") as vDF: data = vDF.read(); vDF.close()
    data = data[:-1][1:].replace("},","}},").split("},")
    datos = []
    for dato in data:
        item = json.loads(dato)
        if mode == "strict" and value == item[filter]: datos.append(item)
        elif mode == "relaxed" and value.lower() in item[filter].lower(): datos.append(item)
        elif data.index(dato) == len(data)-1 and datos == []: return "Err: No existen autos..."
    return datos
        
def get_product(filter, value, mode):
    with open("data/inventory.json","r") as pDF: data = pDF.read(); pDF.close()
    data = data[:-1][1:].replace("},","}},").split("},")
    datos = []
    for dato in data:
        item = json.loads(dato)
        if mode == "strict" and value.lower() == item[filter].lower(): datos.append(item)
        elif mode == "relaxed" and value.lower() in item[filter].lower(): datos.append(item)
        elif data.index(dato) == len(data)-1 and datos == []: return "Err: No existen productos..."
    return datos

def write_cars(dato, write):
    dF = open("data/car.json", "r")
    data = dF.read()[:-1][1:].replace("},","}},").split("},")
    data.append(write) if write != "" else None
    dato = str(dato)[:-1][1:]
    for d in data:
        if str(json.loads(d)) == dato: data.remove(d); break
    dF.close()
    dF = open("data/car.json", "w")
    dF.write("[")
    for dato in data:
        item = json.loads(dato)
        if data.index(dato) != len(data)-1: dF.write('\n    {\n        "lcplate":"'+item["lcplate"]+'",\n        "color":"'+item["color"]+'",\n        "make":"'+item["make"]+'",\n        "model":"'+item["model"]+'",\n        "year":"'+item["year"]+'"\n    },')
        else: dF.write('\n    {\n        "lcplate":"'+item["lcplate"]+'",\n        "color":"'+item["color"]+'",\n        "make":"'+item["make"]+'",\n        "model":"'+item["model"]+'",\n        "year":"'+item["year"]+'"\n    }\n]')
    dF.close()

def write_customer(dato, write):
    dF = open("data/customer.json", "r")
    data = dF.read()[:-1][1:].replace("},","}},").split("},")
    data.append(write) if write != "" else None
    dato = str(dato)[:-1][1:]
    for d in data:
        if str(json.loads(d)) == dato: data.remove(d); break
    dF.close()
    dF = open("data/customer.json", "w")
    dF.write("[")
    for dato in data:
        item = json.loads(dato)
        if data.index(dato) != len(data)-1: dF.write('\n    {\n        "id":"'+item["id"]+'",\n        "name":"'+item["name"]+'",\n        "lastname":"'+item["lastname"]+'",\n        "tel":"'+item["tel"]+'"\n    },')
        else: dF.write('\n    {\n        "id":"'+item["id"]+'",\n        "name":"'+item["name"]+'",\n        "lastname":"'+item["lastname"]+'",\n        "tel":"'+item["tel"]+'"\n    }\n]')
    dF.close()

def write_account(dato, write):
    dF = open("data/account.json", "r")
    data = dF.read()[:-1][1:].replace("},","}},").split("},")
    data.append(write) if write != "" else None
    dato = str(dato)[:-1][1:]
    for d in data:
        if str(json.loads(d)) == dato: data.remove(d); break
    dF.close()
    dF = open("data/account.json", "w")
    dF.write("[")
    for dato in data:
        item = json.loads(dato)
        if data.index(dato) != len(data)-1: dF.write('\n    {\n        "id":"'+item["id"]+'",\n        "name":"'+item["name"]+'",\n        "tel":"'+item["tel"]+'",\n        "balance":"'+item["balance"]+'"\n    },')
        else: dF.write('\n    {\n        "id":"'+item["id"]+'",\n        "name":"'+item["name"]+'",\n        "tel":"'+item["tel"]+'",\n        "balance":"'+item["balance"]+'"\n    }\n]')
    dF.close()

def write_works(dato, write):
    dF = open("data/work.json", "r")
    data = dF.read()[:-1][1:].replace("},","}},").split("},")
    data.append(write) if write != "" else None
    dato = str(dato)[:-1][1:]
    for d in data:
         if str(json.loads(d)) == dato: data.remove(d); break
    dF.close()
    dF = open("data/work.json", "w")
    dF.write("[")
    for dato in data:
        item = json.loads(dato)
        item["work"] = str(item["work"]).replace("'", '"').replace("}, {", "}}, {{")[:-1][1:].split("}, {")
        dF.write('\n    {\n        "id":"'+item["id"]+'",\n        "customer":"'+item["customer"]+'",\n        "lcplate":"'+item["lcplate"]+'",\n        "entrydt":"'+item["entrydt"]+'",\n        "diagnostic":"'+item["diagnostic"]+'",\n        "exitdt":"'+item["exitdt"]+'",\n        "work":[')
        for x in item["work"]:
            i = str(x).replace("'", '"')
            i = json.loads(i)
            if 0 == item["work"].index(x): dF.write('\n            {\n                "item":"'+i["item"]+'",\n                "price":"'+i["price"]+'",\n                "quantity":"'+i["quantity"]+'"\n            }\n            ,')
            elif len(item["work"])-1 != item["work"].index(x): dF.write('{\n                "item":"'+i["item"]+'",\n                "price":"'+i["price"]+'",\n                "quantity":"'+i["quantity"]+'"\n            }\n            ,')
            else: dF.write('{\n                "item":"'+i["item"]+'",\n                "price":"'+i["price"]+'",\n                "quantity":"'+i["quantity"]+'"\n            }')
        if len(data)-1 != data.index(dato): dF.write('\n        ],\n        "price":"'+item["price"]+'",\n        "status":"'+item["status"]+'"\n    },')
        else: dF.write('\n        ],\n        "price":"'+item["price"]+'",\n        "status":"'+item["status"]+'"\n    }\n]')

def write_product(dato, write):
    dF = open("data/inventory.json", "r")
    data = dF.read()[:-1][1:].replace("},","}},").split("},")
    data.append(write) if write != "" else None
    dato = str(dato)[:-1][1:]
    for d in data:
        if str(json.loads(d)) == dato: data.remove(d); break
    dF.close()
    dF = open("data/inventory.json", "w")
    dF.write("[")
    for dato in data:
        item = json.loads(dato)
        if data.index(dato) != len(data)-1: dF.write('\n    {\n        "item":"'+item["item"]+'",\n        "price":"'+item["price"]+'",\n        "stock":"'+item["stock"]+'"\n    },')
        else: dF.write('\n    {\n        "item":"'+item["item"]+'",\n        "price":"'+item["price"]+'",\n        "stock":"'+item["stock"]+'"\n    }\n]')
    dF.close()

def write_history(dato, write):
    dF = open("data/history.json", "r")
    data = dF.read()
    data = data[:-1][1:].replace("},","}},").split("},") if data != "" else []
    data.append(write) if write != "" else None
    dato = str(dato)[:-1][1:]
    for d in data:
         if str(json.loads(d)) == dato: data.remove(d); break
    dF.close()
    timedate = str(time.localtime()).split(',')
    year = timedate[0][-4:].replace("=","")
    month = timedate[1][-2:].replace("=","")
    day = timedate[2][-2:].replace("=","")
    hour = timedate[3][-2:].replace("=","")+":"+timedate[4][-2:].replace("=","")+":"+timedate[5][-2:].replace("=","")

    datetime = day+"/"+month+"/"+year+" , "+hour
    dF = open("data/history.json", "w")
    dF.write("[")
    for dato in data:
        item = json.loads(dato)
        item["work"] = str(item["work"]).replace("'", '"').replace("}, {", "}}, {{")[:-1][1:].split("}, {")
        dF.write('\n    {\n        "id":"'+item["id"]+'",\n        "customer":"'+item["customer"]+'",\n        "lcplate":"'+item["lcplate"]+'",\n        "entrydt":"'+item["entrydt"]+'",\n        "diagnostic":"'+item["diagnostic"]+'",\n        "exitdt":"'+datetime+'",\n        "work":[')
        for x in item["work"]:
            i = str(x).replace("'", '"')
            i = json.loads(i)
            if 0 == item["work"].index(x): dF.write('\n            {\n                "item":"'+i["item"]+'",\n                "price":"$'+i["price"]+'",\n                "quantity":"'+i["quantity"]+'"\n            }\n            ,')
            elif len(item["work"])-1 != item["work"].index(x): dF.write('{\n                "item":"'+i["item"]+'",\n                "price":"$'+i["price"]+'",\n                "quantity":"'+i["quantity"]+'"\n            }\n            ,')
            else: dF.write('{\n                "item":"'+i["item"]+'",\n                "price":"$'+i["price"]+'",\n                "quantity":"'+i["quantity"]+'"\n            }')
        if len(data)-1 != data.index(dato): dF.write('\n        ],\n        "price":"'+item["price"]+'",\n        "status":"'+item["status"]+'"\n    },')
        else: dF.write('\n        ],\n        "price":"'+item["price"]+'",\n        "status":"'+item["status"]+'"\n    }\n]')

def remove_data(filename, value, field):
    if filename == "car.json":
        dato = get_cars(field, value, "strict")
        write_cars(dato, "")
    if filename == "customer.json":
        dato = get_customer(field, value, "strict")
        write_customer(dato, "")
    if filename == "work.json":
        dato = get_works(field, value, "strict")
        write_works(dato, "")
    if filename == "inventory.json":
        dato = get_product(field, value, "strict")
        write_product(dato, "")
    if filename == "account.json":
        dato = get_account(field, value, "strict")
        write_account(dato, "")

def mod_data(value, filter, field, newValue, filename):
    with open(f"data/{filename}", "r") as dF: data = dF.read(); dF.close()
    data = data[:-1][1:].replace("},","}},").split("},")
    for dato in data:
        item = json.loads(dato)
        if item[filter] == value:
            remove_data(filename, value, filter)
            if filename == "car.json":
                item[field] = newValue
                write_cars("", '{"lcplate":"'+item["lcplate"]+'", "color":"'+item["color"]+'", "make":"'+item["make"]+'", "model":"'+item["model"]+'", "year":"'+item["year"]+'"}')
            elif filename == "account.json":
                item[field] = newValue
                write_account("", '{"id":"'+item["id"]+'", "name":"'+item["name"]+'", "tel":"'+item["tel"]+'", "balance":"'+item["balance"]+'"}')
            elif filename == "customer.json":
                item[field] = newValue
                write_customer("", '{"id":"'+item["id"]+'", "name":"'+item["name"]+'", "lastname":"'+item["lastname"]+'", "tel":"'+item["tel"]+'"}')
            elif filename == "work.json":
                item[field] = newValue
                write_works("", '{"id":"'+item["id"]+'", "customer":"'+item["customer"]+'", "lcplate":"'+item["lcplate"]+'", "entrydt":"'+item["entrydt"]+'", "diagnostic":"'+item["diagnostic"]+'", "exitdt":"'+item["exitdt"]+'", "work":'+str(item["work"]).replace("'", '"')+', "price":"'+item["price"]+'", "status":"'+item["status"]+'"}')
            elif filename == "inventory.json":
                item[field] = newValue
                write_product("", '{"item":"'+item["item"]+'", "price":"'+item["price"]+'", "stock":"'+item["stock"]+'"}')
            break