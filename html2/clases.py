from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, IntegerField, FileField
from wtforms.validators import DataRequired 

class producto(FlaskForm):
    nomPro = StringField('Nombre producto *',validators=[DataRequired(message='Nombre es requerido, no lo deje en blanco')])
    refPro = StringField('Referencia producto *',validators=[DataRequired(message='Referencia es requerido, no lo deje en blanco')])
    canPro = IntegerField('Cantidad producto *',validators=[DataRequired(message='Cantidad es requerido, no lo deje en blanco')])
    imPro = FileField()
    registrar = SubmitField('Registrar')
    actualizar = SubmitField('Actualizar')


class contrasena(FlaskForm):
    pws=PasswordField('Contraseña *',validators=[DataRequired(message='Contraseña es requerida, no lo deje en blanco')])
    confirmacion=PasswordField('Confirmación *',validators=[DataRequired(message='Confirmación es requerida, no lo deje en blanco')])
    asignar = SubmitField('Asignar contraseña')
    

class usuario(FlaskForm):
    nombre = StringField('Nombre usuario *',validators=[DataRequired(message='Nombre usuario requerido para continuar')])
    apellido = StringField('Apellido usuario *',validators=[DataRequired(message='El apellido del usuario es requerido para continuar')])
    ident = IntegerField('Identificación *',validators=[DataRequired(message='La identificación es requerida para continuar')])
    correo = StringField('Correo electrónico *',validators=[DataRequired(message='El correo electrónico es requerido para continuar')])
    direccion = StringField('Dirección usuario *',validators=[DataRequired(message='La dirección es requerido para continuar')])
    celular = StringField('Celular usuario *',validators=[DataRequired(message='El celular es requerido para continuar')])
    registrar = SubmitField('Registrar')

class restaurarUsuario(FlaskForm):
    correo = StringField('Contraseña *',validators=[DataRequired(message='Contraseña es requerida, no lo deje en blanco')])
    enviar = SubmitField('Enviar Correo')