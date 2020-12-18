import hashlib
import os
from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint, session
from markupsafe import escape
from clases import producto, contrasena, usuario, restaurarUsuario
import utils as UT
from flask_mail import Mail, Message
from db import db, views
from werkzeug.utils import secure_filename
import conexion
import json



app = Flask(__name__)
app.secret_key = os.urandom(24)
app.register_blueprint(db)
#mail= Mail(app)
""" 
app.config['MAIL_SERVER']='smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = 'ba65810f63f0c4'
app.config['MAIL_PASSWORD'] = '40c5ceef016106'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False  """
app.add_url_rule('/imagenes/<path:filename>', endpoint='imagenes',
                 view_func=app.send_static_file)
app.config['UPLOAD_FOLDER']="./static/imagenes"
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'ciatienda.cia@gmail.com'
app.config['MAIL_PASSWORD'] = 'Misiontic2020'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail= Mail(app)

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
                res = views.existeusuario(user)
                #print(res)
                if int(res)>0:
                    #Configuracion del correo 
                    receiver = request.form['correo']
                    sender = "Tienda cia <from@example.com>"
                    print (receiver)
                    recipients = [receiver]
                    saludo='Correo de recuperacion de clave'
                    link=views.genlink(receiver)
                    #Generar link
                    msg = Message(saludo, sender = sender, recipients = recipients)
                    # msg.body = U"""Hola hemos recibido una solicitud por parte de este correo para recuperar 
                    #             la clave haga clic en el siguiente link sino ignore este mensaje"""
                    msg.html='<p>Hola hemos recibido una solicitud por parte de este correo para recuperar'
                    msg.html += 'la clave, haga clic en el siguiente <a href="http://127.0.0.1:5000/password/'
                    msg.html += str(res)+"/"+link +'">link </a>  sino fue usted ignore este mensaje<p>'
                    mail.send(msg)
                    return render_template('login.html')
                    #Envio link
                else:   
                    flash('Error el correo no esta registrado en la base de datos')
            else: #la clave no reune las caracteristicas
                flash('No es un formato de correo valido')
        inst = restaurarUsuario()  # Una instancia del formulario 
        return render_template('recusuario.html',form=inst)
    #except:
    #    pass

@app.route('/password/<int:iduser>/<string:link>', methods=['GET', 'POST'])
def add_password(iduser,link):
    try:
        if request.method=='POST':
            pws = escape(request.form['pws'])
            conf = escape(request.form['confirmacion'])
            if UT.isPasswordValid(pws):
                if UT.isPasswordValid(conf):
                    if pws==conf:
                        iduser=iduser
                        res=views.actclave(iduser,pws)
                        flash(res)
                        flash('Clave asignada con éxito') 
                        return render_template('login.html')
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
    #try:
        if request.method=='GET':
            inst = producto()  # Una instancia del formulario 
            return render_template('registroproducto.html',form=inst)
        else:
            nomP = escape(request.form['nomPro'])
            refP = escape(request.form['refPro'])
            canP = escape(request.form['canPro'])
            imP = request.files['imPro']
            filename = secure_filename(imP.filename)
            imP.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            familia=1
            estado='A'
            #FALTA SUBIR LA IMAGEN AL DRIVE Y SACAR LA RUTA
            if int(canP)>=0:
                sal= views.crearproducto(nomP,refP,canP,filename)
            else:
                sal="Cantidad invalida"
            flash(sal)
            inst = producto()  # Una instancia del formulario 
            return redirect(url_for('reg_producto'))
    #except:
    #    pass

@app.route('/actproducto/<int:idproducto>', methods=["GET", "POST"])
def act_producto(idproducto):
    #try:
        if request.method=='GET':
            data=views.galeria(int(idproducto))
            jdata=json.loads(data)
            tamano=len(jdata)
            inst = producto() 
            return render_template('Administrador.html',form=inst,contacto = jdata, tam=tamano)
        else:
            print("Estoy entrando por POST     ")
            nomP = escape(request.form['nomPro'])
            refP = escape(request.form['refPro'])
            canP = escape(request.form['canPro'])
            # imP = request.files['imPro']
            # filename = secure_filename(imP.filename)
            # imP.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            familia=1
            estado='A'
            idpro = 3 
            if int(canP)>=0:
                query= "UPDATE producto set nombre = ? , referencia = ? , cantidad = ? , imagen = ? , familia = ? , estado = ? WHERE id = ?"
                res = conexion.ejecutar_consulta_acc(query,(nomP, refP, canP, imP, familia, estado, idpro))
                if res!=None:
                    sal = 'Actualización exitosa'
                else:
                    sal = 'Error al actualizar los datos'
            else:
                sal="Cantidad invalida"
            flash(sal)
            inst = producto()  # Una instancia del formulario 
            return redirect(url_for('admin'))
    #except:
    #    pass

@app.route('/rusuario', methods=["GET", "POST"])
def reg_usuario():
    #try:
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
            
            if int(identU)>=0:
                res = views.crearusuario(nombreU, apellidoU, identU, correoU, direccionU, celularU)
                if res=="True":
                    sal = 'Usuario agregado satisfactoriamente'
                    #Configuracion del correo 
                    receiver = request.form['correo']
                    sender = "Tienda cia <ciatienda.cia@gmail.com>"
                    print (receiver)
                    recipients = [receiver]
                    saludo='Bienvenido al nuevo gestor de inventarios CIA'
                    link=views.genlink(receiver)
                    #Generar link
                    msg = Message(saludo, sender = sender, recipients = recipients)
                    # msg.body = U"""Hola hemos recibido una solicitud por parte de este correo para recuperar 
                    #             la clave haga clic en el siguiente link sino ignore este mensaje"""
                    msg.html='Hola, '+nombreU+' '+apellidoU+' hoy hemos queremos saludarte y darte la bienvenida al'
                    msg.html += ' equipo de CIA, para nosotros es importante que formes parte de nuestro grupo. El siguiente paso es que'
                    msg.html += ' actualices tu contraseña, para ello en este correo te ponemos un link, para&nbsp; acceder al '
                    msg.html += ' sitio de cambio de contraseña, hasta que no asignes una no podras '
                    msg.html += 'disfrutar de esta gran herramienta.'
                    msg.html += 'Es muy importante que tengas en cuenta que por seguridad la contraseña debe cumplir con una serie de requisitos:'
                    msg.html += 'Debe tener al menos 8 caracteres y un máximo de 16.'
                    msg.html += 'Debe contener al menos 1 caracter en mayúscula (A-Z).'
                    msg.html += 'Debe contener al menos 1 caracter en min&uacute;scula (a-z).'
                    msg.html += 'Debe contener al menos 1 caracter num&eacute;rico (0-9).'
                    msg.html += 'Debe contener al menos 1 caracter especial ($,.&lt;&gt;).'
                    msg.html += 'Haga clic en el siguiente <a href="http://127.0.0.1:5000/password/'
                    msg.html += str(res)+"/"+link +'">link </a>  Le deseamos un gran día<p>'
                    mail.send(msg)
                else:
                    sal = 'Error al registrar los datos del usuario'
            else:
                sal="No puede realizar el registro"
            flash(sal)
            forinst = usuario() 
            return redirect(url_for('reg_usuario'))
    #except:
    #    pass

#Muestra el listado de todos los usuarios registrados en la base de datos

@app.route('/rusuariou', methods=["GET", "POST"])
def registroU():      
            query ='SELECT * FROM usuario'
            sal = conexion.ejecutar_consulta_sel(query)
            data = sal
            return render_template('listarusuarios.html', contactos = data)

#Permite editar la información del usuario en el formulario
@app.route('/edit/<id>')
def get_contact(id):    
    
    query = 'SELECT id, nombre, apellido, documento, correo, direccion, celular FROM usuario WHERE id= ?'
    res = conexion.ejecutar_consulta_acc(query,(id))
    data = list(res)
    
    return render_template('actUsuario.html', contacto = data[0])

#Actualiza la información en el formulario editado y guarda en la base de datos
@app.route('/update/<id>', methods=["POST"])
def actualizar_contacto(id):
    try:
        if request.method == 'POST':
            nombre1 = request.form['nombre']
            apellido1 = request.form['apellido']
            documento1 = request.form['documento']
            correo1 = request.form['correo']
            direccion1 = request.form['direccion']
            telefono1 = request.form['celular']
            query = "UPDATE usuario SET  nombre = ?, apellido = ?, documento = ?, correo = ?, celular = ?,  direccion = ? WHERE id = ?"
            print(query + '+' + id)
            con = conexion.ejecutar_consulta_acc(query,(nombre1, apellido1, documento1, correo1, telefono1,  direccion1, id)) 
            data = con
            flash('Conctacto actualizado satisfactorialmente')
            return redirect(url_for('registroU'))
    except:
        pass
#Elimina el registor del usuario en la base de datos
@app.route('/delete/<string:id>')
def delete_contact(id):
    
    query = 'DELETE FROM usuario WHERE id ={0}'.format(id)
    sal = conexion.ejecutar_consulta_sel(query)
    data = sal
    flash('Contacto removido satisfactorialmente')
    return redirect(url_for('registroU'))


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
        session.clear()
        idusr=int(views.loginusuario(usuario,password))
        if idusr>0:
            session['usr_id'] = idusr
            session['usr_mail'] = usuario
            session['tipo'] = views.tipousuario(idusr)
            session['nombre']=views.getCompletName(idusr)
            inst = producto() 

            data=views.galeria(0)
            jdata=json.loads(data)
            tamano=len(jdata)
            print("Me apuesto una-----")
            print(jdata)
            return render_template('Administrador.html',form=inst, contacto = jdata, tam=tamano)
        else:
            flash('Datos Invalidos') 
            return render_template('login.html')
    else:
        data=views.galeria(0)
        jdata=json.loads(data)
        tamano=len(jdata)
            #print("Estoy aquí     "+jdata[0])
        inst = producto() 
        return render_template('Administrador.html',form=inst,contacto = jdata, tam=tamano)    

if __name__ == "__main__":   
   app.run(port=5000, debug=True)
