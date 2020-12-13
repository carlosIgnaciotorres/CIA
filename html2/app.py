
import os
from flask import Flask, render_template, request
from markupsafe import escape
from clases import producto


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
    inst = producto()  # Una instancia del formulario 
    return render_template('registroproducto.html',form=inst)

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
