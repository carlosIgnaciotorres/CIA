from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, IntegerField, FileField
from wtforms.validators import DataRequired 

class producto(FlaskForm):
    nomPro = StringField('Nombre producto *',validators=[DataRequired(message='Nombre es requerido, no lo deje en blanco')])
    refPro = StringField('Referencia producto *',validators=[DataRequired(message='Referencia es requerido, no lo deje en blanco')])
    canPro = IntegerField('Cantidad producto *',validators=[DataRequired(message='Cantidad es requerido, no lo deje en blanco')])
    imPro = FileField()
    registrar = SubmitField('Registrar')


