import hashlib
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from markupsafe import escape
from clases import producto, contrasena, usuario, restaurarUsuario
import conexion
import utils as UT
from flask_mail import Mail, Message


app = Flask(__name__)
app.secret_key = os.urandom(24)
mail= Mail(app)

app.config['MAIL_SERVER']='smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = 'ba65810f63f0c4'
app.config['MAIL_PASSWORD'] = '40c5ceef016106'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

@app.route('/', methods=['GET', 'POST'])
def Index():    
        return render_template('login.html')

@app.route('/vista', methods=['GET', 'POST'])
def agregar_vista():
    return render_template('vista.html')

@app.route('/vista1', methods=['GET', 'POST'])
def agregar_vistaadm():
    return render_template('vista_adm.html')

@app.route('/recuperar', methods=['GET', 'POST'])
def recuperar():
    #try:
        if request.method=='POST':
            user = escape(request.form['correo'])
            if UT.isEmailValid(user):
                query= "SELECT count(id) FROM  WHERE correo = ?"
                res = conexion.ejecutar_consulta_sel(query,(user))
                if res!=None:
                    #Configuracion del correo 
                    receiver = escape(request.form['correo'])
                    sender = "Tienda cia <from@example.com>"
                    print (receiver)
                    recipients = [receiver]
                    saludo='Correo de recuperacion de clave'
                    #Generar link
                    msg = Message(saludo, sender = sender, recipients = recipients)
                    msg.body = U"""Hola hemos recibido una solicitud por parte de este correo para recuperar 
                                la clave haga clic en el siguiente link sino ignore este mensaje"""
                    mail.send(msg)
                    #Envio link
                else:   
                    flash('Error el correo no esta registrado en la base de datos')
            else: #la clave no reune las caracteristicas
                flash('No es un formato de correo valido')
        inst = contrasena()  # Una instancia del formulario 
        return render_template('recusuario.html',form=inst)
    #except:
    #    pass

@app.route('/password', methods=['GET', 'POST'])
def add_password():
    try:
        if request.method=='POST':
            pws = escape(request.form['pws'])
            conf = escape(request.form['confirmacion'])
            if UT.isPasswordValid(pws):
                if UT.isPasswordValid(conf):
                    if pws==conf:
                        rpt = hashlib.md5(pws.encode())
                        pwd = rpt.hexdigest()
                        estado="A"
                        iduser=1
                        query= "UPDATE usuario set clave = ? , estado = ? WHERE id = ?"
                        res = conexion.ejecutar_consulta_acc(query,(pwd, estado , iduser))
                        if res!=None:
                            flash('Datos registrados con éxito')
                        else:   #else res
                            flash('Error al registrar los datos')
                    else: #diferente pws y conf
                        flash('La contraseña y su verificacion no coinciden')
                else: #la verificacion no reune las caracteristicas
                    flash('La confirmacion no es correcta')
            else: #la contraseña no reune las caracteristicas
                flash('La contraseña no es valida')
        inst = contrasena()  # Una instancia del formulario 
        return render_template('password.html',form=inst)
    except:
        pass

@app.route('/rproducto', methods=['GET', 'POST'])
def reg_producto():
    try:
        if request.method=='GET':
            inst = producto()  # Una instancia del formulario 
            return render_template('registroproducto.html',form=inst)
        else:
            nomP = escape(request.form['nomPro'])
            refP = escape(request.form['refPro'])
            canP = escape(request.form['canPro'])
            # imP = escape(request.form['imPro'])
            imP="imagen1.jpg"
            familia=1
            estado='A'
            #FALTA SUBIR LA IMAGEN AL DRIVE Y SACAR LA RUTA
            if int(canP)>=0:
                query = "INSERT INTO producto(nombre, referencia, cantidad, imagen, familia, estado) VALUES(?, ?, ?, ?, ?, ?)"
                res = conexion.ejecutar_consulta_acc(query,(nomP, refP, canP, imP, familia, estado))
                if res!=None:
                    sal = 'Datos registrados con éxito'
                else:
                    sal = 'Error al registrar los datos'
            else:
                sal="Cantidad invalida"
            flash(sal)
            inst = producto()  # Una instancia del formulario 
            return redirect(url_for('reg_producto'))
    except:
        pass



@app.route('/rusuario', methods=["GET", "POST"])
def reg_usuario():
    try:
        if request.method == 'GET':
            forinst = usuario()  # Una instancia del formulario 
            return render_template('registrousuario.html',form=forinst)
        else:            
            nombreU = escape(request.form['nombre'])
            apellidoU = escape(request.form['apellido'])
            identU = escape(request.form['ident'])
            correoU = escape(request.form['correo'])
            direccionU = escape(request.form['direccion'])
            celularU = escape(request.form['celular'])
            tipoU=1
            claveU=''
            estadoU=''
            linkU=''
            
            if int(identU)>=0:
                query = "INSERT INTO usuario(nombre, apellido, documento, correo, direccion, celular, tipoDoc, clave, estado, linkrecuperacion) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                res = conexion.ejecutar_consulta_acc(query,(nombreU, apellidoU, identU, correoU, direccionU, celularU, tipoU, claveU, estadoU, linkU))
                if res!=None:
                    sal = 'Usuario agregado satisfactoriamente'
                else:
                    sal = 'Error al registrar los datos del usuario'
            else:
                sal="No puede realizar el registro"
            flash(sal)
            forinst = usuario() 
            return redirect(url_for('reg_usuario'))
    except:
        pass


@app.route('/actusuario', methods=["GET", "POST"])
def act_usuario():
    return render_template('actUsuario.html')

@app.route('/galeria')
def mostrar_galeria():
    return render_template('galeria.html')

@app.route('/accesorios')
def mostrar_accesorio():
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
