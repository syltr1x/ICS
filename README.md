> # **Guía de instalacion**
! Asegurate de tener [python instalado](https://www.python.org/ftp/python/3.11.6/python-3.11.6-amd64.exe) (preferentemente 3.11.6)

Windows (ejecutable):
[Instalador](https://raw.githubusercontent.com/syltr1x/ICS/main/version_mgt/installer.exe)

Powershell:
```
iwr -useb https://raw.githubusercontent.com/syltr1x/ICS/main/version_mgt/installer.ps1 | iex
```
Linux and MacOS:
```
curl -fsSL https://raw.githubusercontent.com/syltr1x/ICS/main/version_mgt/installer.sh | sh
```
# **Guía para Contribuidor**
> ## **Escritura de datos**
Base = write_¿?(dato, write)

Cuentas (Corrientes) > 
```
write_account('{"id":"0", "name":"root", "balance":"", "contact":[{"media":"instagram","value":"admin_0"}], "cars":["AAA000"]}', '')
```
Cuentas (Particulares) > 
```
write_customer('{"id":"0", "name":"admin", "lastname":"instrator", "birthday":"--/--/----", "contact":[{"media":"instagram","value":"admin_0"}], "cars":["AAA000"]}', '')
```
Presupuestos > 
```
write_budget('{"id":"0", "customer":"nombre apellido", "lcplate":"patente", "technician":"mecanico", "entrydt":"entrada", "diagnostic":"service", "work":[], "price":"120", "pd":"pago"}', '')
```
Trabajos > 
```
write_works('{"id":"0", "customer":"nombre apellido", "lcplate":"patente", "technician":"mecanico", "entrydt":"entrada", "diagnostic":"service", "exitdt":"--/--/----", "work":[], "price":"120", "pd":"pago", "status":""}', '')
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

> ## **Pasos para actualizar**<br>
* Tener en cuenta la estructura que indica las actualizaciones en la key:<br>
**Todos los valores se indican con 0(False) y 1(True)**<br>
key_abcde
a=main (indica si se debe actualizar el archivo main.pyw)<br>
b=logic (indica si se debe actualizar el archivo logic.py)<br>
c=frames (indica se se tiene que actualizar la carpeta frames)<br>
d=img (indica si se tiene que actualizar la carpeta img)<br>
e=reqs (indica si se tiene que actualizar el archivo requirements.txt)<br>
* Una vez realizados los cambios actualizar la version key del main<br>
* Actualizar la version key del repositorio
