# GUIA DE USO - Logica

> ## **Guía de instalacion**
! Asegurate de tener python instalado (preferentemente 3.11.6)
[Instalar Python](https://www.python.org/ftp/python/3.11.6/python-3.11.6-amd64.exe)
Powershell:
```
curl.exe https://raw.githubusercontent.com/syltr1x/ICS/main/ICS.zip -o ICS.zip
Expand-Archive -Path "ICS.zip" -DestinationPath "ICS"
pip install -r ICS/requirements.txt
```
> ## **Escritura de datos**
Base = write_¿?(dato, write)

Cuentas (Corrientes) > 
```
write_account('{"id":"0", "name":"root", "tel":"3482?", "balance":"0"}', '')
```
Cuentas (Particulares) > 
```
write_customer('{"id":"0", "name":"admin", "tel":"3482?", "lcplate":"'+["ABC123"]+'"}', '')
```
Trabajos > 
```
write_works('{"id":"0", "customer":"nombre apellido", "lcplate":"patente", "entrydt":"entrada", "diagnostic":"service", "exitdt":"salida", "price":"precio", "status":"pago"}', '')
```
Autos > 
```
write_cars('{"lcplate":"patente", "color":"rojo", "make":"chevrolet", "model":"astra", "year":"2001"}')
```
Producto > 
```
write_product('{"name":"inyector", "price":"8000", "stock":"20"}')
```
### Parametros:
```
dato = dato a borrar. En caso de no querer borrar nada: dato=""
write = dato a escribir. En caso de no querer escribir nada: write=""
```
> ## **Obtencion de datos (peticiones logicas)**

id > ```get_id(filename)```

Cuentas (Particulares) > ```get_customer(filtro, valor, modo)```

Cuentas (Corrientes) > ```get_account(filtro, valor, modo)```

Trabajos > ```get_works(filtro, valor, modo)```

Autos > ```get_cars(filtro, valor, modo)```

Producto > ```get_product(filtro, valor, modo)```

### Parametros:
```
filtro : filtra entre los distintos campos disponibles. Ej : name, tel, lcplate, lastname, etc.
valor : valor del filtro dado anteriormente
modo : busca igualdad o similitud : strict / relaxed
```
> ## **Eliminacion de datos (RDW)**
```
remove_data("customer.json", "Martin", "name") 
  > Elimina el usuario que tenga el nombre Martin de la lista de clientes
remove_data("works.json", "COY410", "lcplate")
  > Elimina el trabajo que tenga el dominio COY410 de la lista de trabajos
```
### Parametros:
```
filename : archivo del cual se quiere eliminar el dato
value : valor del campo seleccionado
field : campo seleccionado
```
> ## **Modificacion de Datos (MWD)**
```
mod_data("Martin", "name", "Carlos", "customer.json")
  > Modifica el nombre del cliente de Martin a Carlos
```
### Parametros:
```
value : valor actual de el campo a modificar
field : campo a modificar
newValue : nuevo valor del campo a modificar
filename : archivo del cual modificar los datos
```

> ## **Pasos para actualizar**
* Una vez realizados los cambios actualizar la version key del main
* Compilar el programa
* Actualizar la version key del repositorio
