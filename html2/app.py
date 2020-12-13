
import os
from flask import Flask, render_template, request, flash
from markupsafe import escape
from clases import producto
import conexion



app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/', methods=['GET', 'POST'])
def Index():    
        return render_template('login.html')

@app.route('/vista', methods=['GET', 'POST'])
def agregar_vista():
    return render_template('vista.html')

@app.route('/vista1', methods=['GET', 'POST'])
def agregar_vistaadm():
    return render_template('vista_adm.html')

@app.route('/password', methods=['GET', 'POST'])
def add_password():
    return render_template('password.html')

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
                    #VACIAR CAMPOS
                    sal = 'Datos registrados con éxito'
                else:
                    sal = 'Error al registrar los datos'
            else:
                sal="Cantidad invalida"
            flash(sal)
            inst = producto()  # Una instancia del formulario 
            return render_template('registroproducto.html',form=inst)
    except:
        pass



@app.route('/rusuario', methods=["GET", "POST"])
def reg_usuario():
    return render_template('registrousuario.html')

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
        contraseña = request.form['contraseña']
        return render_template('Administrador.html')
    else:
        return render_template('login.html')    

if __name__ == "__main__":   
   app.run(port=5000, debug=True)
