# Restaurant System for Kitchen

Sistema de comandas para restaurant, armado del pedido, seguimiento desde la orden hasta la entrega. Incluye calculo de tiempo de demora.

## Installation

### Dependencias, directorios 
Este es un proyecto en Django, así que en antes que todo debemos tener python instalado el equipo. [Python](https://www.python.org/)

Ahora se creara un directorio y dentro de este, un entorno virtual de python ([Python-venv](https://docs.python.org/3/tutorial/venv.html))
```bash
python3 -m venv my_venv
```

Hay que activar el entorno virtual para usar las dependencias que instalaremos alli.
```bash
source /my_venv/bin/activate       # for Linux
source /my_venv/Scripts/activate   # for de Windows
```
Luego solo hay que instalar recursivamente las dependencias del projecto, las cuales se encuentran en el archivo 'requirements.txt'
```bash
pip install -r requirements.txt
```

### Base de Datos
Una vez completado este proceso, se procede a instalar la base de datos.
Se utilizara PostgreSQL pero se puede adaptar a otras base de datos relacionales.

Como requisito se debe contar con PostgreSQL instalado en su equipo, crear usuario y base de datos los cuales serán usados en el archivo 'settings.py'.
```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'NOMBRE_BD',
        'USER': 'USUARIO_DB',
        'PASSWORD': 'PASSWORD',
        'HOST': 'localhost',
        'PORT': '',
    }
}
```

## Ejecutar

Ya con la base de datos conectada, se debe migrar los modelos del proyecto a la base de datos, para esto se usa el siguiente comando.
```bash
python manage.py makemigrations
python manage.py migrate
```
Si todo sale bien, ahora podremos crear un usuario con permisos de administrador
```bash
python manage.py createsuperuser
```
Finalmente se corre el proyecto en el puerto por defecto de Django
```bash
python manage.py runserver
```

## Usage

Este sistema cuenta con
##### -Registro: 
Formulario de registro de usuario, cuanta con contraseña encriptada, validaciones de formato. No entrega mensajes informativos.
#### - Inicio de Sesión:
Formulario de ingreso de sesión con credenciales de usuario previamente registrado.
#### - Carrito
Carrito de compras donde se listan los productos deseados para un pedido, se puede aumentar o disminuir la cantidad de un producto. Cada producto tiene su precio, el cual el carrito se encarga de sumar para obtener el total.
El carrito queda guardado en sesión, por lo que si un usuario abandona la pagina, su pedido se mantendrá en su sesión.
#### Comandas
Cada comanda es la formalización de un pedido. Esta contiene los productos, quien la emitió, la hora a la cual se emite y a la que se entrega, además de un estado para poder saber en que fase se encuentra.
#### Comanda Activa
Se listan las comandas que tiene el atributo estado en activo. 
#### Historial de Comandas
Lista con todas las comandas, aquellas que estén con estado finalizado tienen el tiempo de demora.

## Acerca del proyecto
Proyecto realizado para ver factibilidad de realizarlo de con fines de venta.

Maas informacion en [Sistema-comandas](www.cristianosorio.com/projects/sistemas-comandas)
