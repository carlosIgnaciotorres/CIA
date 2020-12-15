from flask import Blueprint

db = Blueprint('db', __name__, url_prefix="/db")

from . import views