

from flask import Flask, render_template, request
from markupsafe import escape


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def Index():
    return render_template('login.html')

@app.route('/password', methods=['GET', 'POST'])
def add_password():
    return render_template('password.html')

@app.route('/rproducto', methods=['GET', 'POST'])
def reg_producto():
    return render_template('registroproducto.html')

@app.route('/rusuario', methods=["GET", "POST"])
def reg_usuario():
    return render_template('registrousuario.html')

@app.route('/galeria')
def mostrar_galeria():
    return render_template('galeria.html')

@app.route('/accesorios')
def mostrar_accesorio():
    return render_template('accesorio.html')

if __name__ == "__main__":   
   app.run(port=5000, debug=True)
