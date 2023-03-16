import json

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

def get_works(filter, value, mode):
    with open("data/works.json", "r") as wDF: data = wDF.read(); wDF.close()
    data = data[:-1][1:].replace("},","}},").split("},")
    datos = []
    for dato in data:
        item = json.loads(dato)
        if mode == "strict" and value.lower() == item[filter].lower(): datos.append(item)
        elif mode == "relaxed" and value.lower() in item[filter].lower(): datos.append(item)
        elif data.index(dato) == len(data)-1 and datos == []: return "Err: No existen trabajos..."
    return datos

def get_cars(filter, value, mode):
    with open("data/cars.json","r") as vDF: data = vDF.read(); vDF.close()
    data = data[:-1][1:].replace("},","}},").split("},")
    datos = []
    for dato in data:
        item = json.loads(dato)
        if mode == "strict" and value.lower() == item[filter].lower(): datos.append(item)
        elif mode == "relaxed" and value.lower() in item[filter].lower(): datos.append(item)
        elif data.index(dato) == len(data)-1 and datos == []: return "Err: No existen autos..."
    return datos
        
def write_cars(lcplate, color, fuel, make, model, year):
    with open("data/cars.json", "r") as dF: data = dF.read(); dF.close()
    data = data[:-1][1:].replace("},","}},").split("},")
    with open("data/cars.json", "w") as dF:
        dF.write("[")
        for dato in data:
            item = json.loads(dato)
            dF.write('\n    {\n        "lcplate":"'+item["lcplate"]+'",\n        "color":"'+item["color"]+'",\n        "fuel":"'+item["fuel"]+'",\n        "make":"'+item["make"]+'",\n        "model":"'+item["model"]+'",\n        "year":"'+item["year"]+'"\n    },')
        dF.write('\n    {\n        "lcplate":"'+lcplate+'",\n        "color":"'+color+'",\n        "fuel":"'+fuel+'",\n        "make":"'+make+'",\n        "model":"'+model+'",\n        "year":"'+year+'"\n    }\n]')
    dF.close()

def write_customer(id, name, lastname, lcplate):
    with open("data/customer.json", "r") as dF: data = dF.read(); dF.close()
    data = data[:-1][1:].replace("},","}},").split("},")
    with open("data/customer.json", "w") as  dF:
        dF.write("[")
        for dato in data:
            item = json.loads(dato)
            dF.write('\n    {\n        "id":"'+item["id"]+'",\n        "name":"'+item["name"]+'",\n        "lastname":"'+item["lastname"]+'",\n        "lcplate":[\n            '+str(item["lcplate"])[:-1][1:].replace("'",'"')+'\n        ]\n    },')
        if id.lower() == "none": lid = int(item["id"])+1
        else: lid = int(id)
        if "[" in str(lcplate.split(",")): 
            lcplate = str(lcplate.split(","))[:-1][1:].replace("', '",'", "').replace("'",'"')
        else: lcplate = f'"{lcplate}"'
        dF.write('\n    {\n        "id":"'+str(lid)+'",\n        "name":"'+name+'",\n        "lastname":"'+lastname+'",\n        "lcplate":[\n            '+lcplate+'\n        ]\n    }\n]')
    dF.close()

def write_works(customer, lcplate, entrydt, diagnostic, exitdt, price, status):
    with open("data/works.json", "r") as dF: data = dF.read(); dF.close()
    data = data[:-1][1:].replace("},","}},").split("},")
    with open("data/works.json", "w") as dF:
        dF.write("[")
        for dato in data:
            item = json.loads(dato)
            dF.write('\n    {\n        "customer":"'+item["customer"]+'",\n        "lcplate":"'+item["lcplate"]+'",\n        "entrydt":"'+item["entrydt"]+'",\n        "diagnostic":[\n            '+str(item["diagnostic"])[:-1][1:].replace("'",'"')+'\n        ],\n        "exitdt":"'+item["exitdt"]+'",\n        "price":"'+item["price"]+'",\n        "status":"'+item["status"]+'"\n    },')
        diagnostic = str(diagnostic)[:-1][1:].replace("', '",'", "').replace("'",'"')
        dF.write('\n    {\n        "customer":"'+customer+'",\n        "lcplate":"'+lcplate+'",\n        "entrydt":"'+entrydt+'",\n        "diagnostic":[\n            '+diagnostic+'\n        ],\n        "exitdt":"'+exitdt+'",\n        "price":"'+price+'",\n        "status":"'+status+'"\n    }\n]')
    dF.close()
    
def remove_data(filename, value, field):
    if filename == "cars.json":
        with open(f"data/{filename}", "r") as dF: data = dF.read(); dF.close()
        data = data[:-1][1:].replace("},","}},").split("},")
        for dato in data:
            item = json.loads(dato)
            if value == item[field]: data.remove(dato); break
        with open(f"data/{filename}", "w") as dF:
            dF.write("[")
            for dato in data:
                item = json.loads(dato)
                if data.index(dato) < len(data)-1: dF.write('\n    {\n        "lcplate":"'+item["lcplate"]+'",\n        "color":"'+item["color"]+'",\n        "fuel":"'+item["fuel"]+'",\n        "make":"'+item["make"]+'",\n        "model":"'+item["model"]+'",\n        "year":"'+item["year"]+'"\n    },')
                elif data.index(dato) == len(data)-1: dF.write('\n    {\n        "lcplate":"'+item["lcplate"]+'",\n        "color":"'+item["color"]+'",\n        "fuel":"'+item["fuel"]+'",\n        "make":"'+item["make"]+'",\n        "model":"'+item["model"]+'",\n        "year":"'+item["year"]+'"\n    }\n]')
        dF.close()
    if filename == "customer.json":
        with open(f"data/{filename}", "r") as dF: data = dF.read(); dF.close()
        data = data[:-1][1:].replace("},","}},").split("},")
        for dato in data:
            item = json.loads(dato)
            if value == item[field]: data.remove(dato); break
        with open(f"data/{filename}", "w") as dF:
            dF.write("[")
            for dato in data:
                item = json.loads(dato)
                if data.index(dato) < len(data)-1: dF.write('\n    {\n        "id":"'+item["id"]+'",\n        "name":"'+item["name"]+'",\n        "lastname":"'+item["lastname"]+'",\n        "lcplate":[\n            '+str(item["lcplate"]).replace(" ","")[:-1][1:].replace("'",'"')+'\n        ]\n    },')
                elif data.index(dato) == len(data)-1: dF.write('\n    {\n        "id":"'+item["id"]+'",\n        "name":"'+item["name"]+'",\n        "lastname":"'+item["lastname"]+'",\n        "lcplate":[\n            '+str(item["lcplate"]).replace(" ","")[:-1][1:].replace("'",'"')+'\n        ]\n    }\n]')
    if filename == "works.json":
        with open(f"data/{filename}", "r") as dF: data = dF.read(); dF.close()
        data = data[:-1][1:].replace("},","}},").split("},")
        for dato in data:
            item = json.loads(dato)
            if value == item[field]: data.remove(dato); break
        with open(f"data/{filename}", "w") as dF:
            dF.write("[")
            for dato in data:
                item = json.loads(dato)
                if data.index(dato) < len(data)-1: dF.write('\n    {\n        "customer":"'+item["customer"]+'",\n        "lcplate":"'+item["lcplate"]+'",\n        "entrydt":"'+item["entrydt"]+'",\n        "diagnostic":[\n            '+str(item["diagnostic"])[:-1][1:].replace("'",'"')+'\n        ],\n        "exitdt":"'+item["exitdt"]+'",\n        "price":"'+item["price"]+'",\n        "status":"'+item["status"]+'"\n    },')
                elif data.index(dato) == len(data)-1: dF.write('\n    {\n        "customer":"'+item["customer"]+'",\n        "lcplate":"'+item["lcplate"]+'",\n        "entrydt":"'+item["entrydt"]+'",\n        "diagnostic":[\n            '+str(item["diagnostic"])[:-1][1:].replace("'",'"')+'\n        ],\n        "exitdt":"'+item["exitdt"]+'",\n        "price":"'+item["price"]+'",\n        "status":"'+item["status"]+'"\n    }\n]')

def mod_data(value, field, newValue, filename):
    with open(f"data/{filename}", "r") as dF: data = dF.read(); dF.close()
    data = data[:-1][1:].replace("},","}},").split("},")
    for dato in data:
        item = json.loads(dato)
        if value in str(item[field])[:-2][2:]:
            id = str(get_customer(field, value, "relaxed"))[:-1][1:].replace("'", '"')
            id = json.loads(id)["id"]
            print(id)
            if filename == "cars.json":
                item[field] = newValue
                lcplate = item["lcplate"]
                color = item["color"]
                fuel  = item["fuel"]
                make = item["make"]
                model = item["model"]
                year = item["year"]
                write_cars(lcplate, color, fuel, make, model, year)
            elif filename == "customer.json":
                remove_data(filename, id, "id")
                item[field] = newValue
                id = item["id"]
                name = item["name"]
                lastname  = item["lastname"]
                lcplate = item["lcplate"]
                write_customer(id, name, lastname, lcplate)
            elif filename == "works.json":
                item[field] = newValue
                customer = item["customer"]
                lcplate = item["lcplate"]
                entrydt = item["entrydt"]
                diagnostic = item["diagnostic"]
                exitdt = item["exitdt"]
                price = item["price"]
                status = item["status"]
                write_works(customer, lcplate, entrydt, diagnostic, exitdt, price, status)

#mod_data("901AKA", "lcplate", "9090AB", "customer.json")