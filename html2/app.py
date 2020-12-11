# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
from markupsafe import escape


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def Index():    
    # Ruta de index
    # 1 se verifican que los campos de login esten correctos y no tengan datos extraños
        return render_template('login.html')

@app.route('/password', methods=['GET', 'POST'])
def add_password():
    # Ruta de Password, aquí solo se puede llegar por link de correo
    # 1 se verifica que el parametro <solicitud> sea valido
    # 2 Se busca el correo en la base de datos segun la solicitud
    # 3 se pide el nuevo password y confirmación
    # 4 se verrifica que coincidan y reunan las caracteristicas minimas
    # 5 Si 4 es correcto se procede a almacenar el nuevo password y se inicia sesion en la pagnina de la galeria
    # 6 Si 4 es incorrecto se vuelve al paso 3
    return render_template('password.html')

@app.route('/rproducto', methods=['GET', 'POST'])
def reg_producto():
    # Ruta registro de producto (administrador)
    # 1 se solicitan los diferentes campos del producto
    # 2 Validacion de datos
    # 3 se almacena el producto en la base de datos con un Id automático
    # 4 se limpia la pantalla para crear un producto nuevo 
    return render_template('registroproducto.html')

@app.route('/recusuario', methods=["GET", "POST"])
def recu_usuario():
    # Ruta de recuperar usuario, aquí solo se puede llegar desde Login (Olvido su contraseña)
    # 1 se lee el campo de usuario (correo)
    # 2 Se busca el correo en la base de datos segun la solicitud
    # 3 Si el correo existe se genera un registro para nuevo password y se envia al email
    # 4 Si 3 es incorrecto se vuelve al paso 2
    return render_template('recusuario.html')

@app.route('/rusuario', methods=["GET", "POST"])
def reg_usuario():
    # Ruta registro de usuario (administrador)
    # 1 se solicitan los diferentes campos del usuario
    # 2 Validacion de datos
    # 3 se almacena el nuevo usuario en la base de datos con un Id automático 
    # y con el campo sin validar 
    # 4 la aplicacion envia un mail, para verificar el usuario 
    # 5 se limpia la pantalla para crear un usuario nuevo 
    return render_template('registrousuario.html')

@app.route('/actusuario', methods=["GET", "POST"])
def act_usuario():
    # Ruta actualizar de usuario (administrador) recibe un id de usuario
    # 1 se muestran los valores de los diferentes campos del usuario 
    # 2 Validacion de datos ingresados y modificados
    # 3 se almacena el nuevo usuario en la base de datos con el Id recibido
    # 4 se limpia la pantalla para crear un usuario 
    return render_template('registrousuario.html')

@app.route('/galeria')
def mostrar_galeria():
    # Ruta galeria de usuario o administrador
    # 1 es la ventana de inicio despues de hacer login y se encarga de mostrar 
    # los diferentes accesorios del almacen mostrando la información de los mismos 
    # con un buscador para ir a la base de datos y buscar los articulos
    # 2 Si se busca por algun termino se ba a la base de datos y se busca como un like
    # 3 se reflejan los resultados de la busqueda
    return render_template('galeria.html')

@app.route('/accesorio')
def mostrar_accesorio():
    # Ruta accesorio de usuario o administrador
    # 1 es la ventana a la que se llega tras hacer clic en un objeto de la galeria 
    # mostrando la información de los mismos, si es administrador tiene dos botones 
    # uno para editar y otro para borrar.
    # 2 tanto usuario como administrador pueden modificar la cantidad y esta debe 
    # ser mayor o igual a cero
    # 3 cuando presiona cerrar se guardan los cambios en cantidad para los usuarios 
    return render_template('accesorio.html')

@app.route('/admin', methods=['GET', 'POST'])
def mostrar_admin():
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']
        return render_template('Administrador.html')
    else:
        return render_template('login.html')    

if __name__ == "__main__":   
   app.run(port=5000, debug=True)
