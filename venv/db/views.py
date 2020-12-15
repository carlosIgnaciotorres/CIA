import hashlib
from . import db
import  conexion as CON
import json
from datetime import datetime

@db.route('/producto/<int:id>')
def galeria(id):
    query= "SELECT id, nombre, referencia, imagen, cantidad FROM producto WHERE estado = 'A'"
    if int(id) > 0:
        query = query + ' and id = '+ str(id)
        res = CON.ejecutar_consulta_sel(query, None)
    else:
        res = CON.ejecutar_consulta_sel(query, None)
    json_res = json.dumps(res)
    return json_res

@db.route('/usuario/<int:id>')
def usuario(id):
    query= "SELECT id, correo, nombre, apellido, celular, documento, direccion, estado FROM usuario  "
    if int(id) > 0:
        query =query + 'WHERE id = '+ str(id)
        res = CON.ejecutar_consulta_sel(query,None)
    else:
        res = CON.ejecutar_consulta_sel(query, None)
    json_res = json.dumps(res)
    return json_res

@db.route('/existeusuario/<string:correo>')
def existeusuario(correo):
    ans = "True"
    query= "SELECT count(id) FROM usuario WHERE correo = "+ correo
    res = CON.ejecutar_consulta_sel(query,None)
    if res==None or len(res)==0:
        ans = 'False'
    if res[0][0]==0:
        ans="False"
    return ans 

@db.route('/genlink/<string:correo>')
def genlink(correo):
    query= "SELECT id,  estado  FROM usuario WHERE correo = '" +correo + "'"
    res = CON.ejecutar_consulta_sel(query,None)
    if res==None or len(res)==0:
        pwd = ""
        link = ""
    else:
        iduser = res[0][0]
        estado = res[0][1]
        fecha =  datetime.now()
        if estado !='I':
            link = str(iduser)+estado+str(fecha)
            rpt = hashlib.md5(link.encode())
            pwd = rpt.hexdigest()
            query= "UPDATE usuario set linkrecuperacion = ?  WHERE id = ?"
            print(f'SQL:{query} /n datos:{pwd} --- {iduser}')
            dat = CON.ejecutar_consulta_acc(query,(pwd,  iduser))
            print(f'datos : {dat}')
    return pwd                                        

@db.route('/pruebalink/<string:link>')
def pruebalink(link):
    ans = True
    query= "SELECT count(id)  FROM usuario WHERE linkrecuperacion = '" +link + "'"
    res = CON.ejecutar_consulta_sel(query,None)
    if res==None or len(res)==0:
        ans = False
    return str(ans)

@db.route('/tipoUser/<int:iduser>')
def tipousuario(iduser):
    ans = 'Administrador'
    query= "SELECT count(id)  FROM usuario WHERE estado='X' and id = "+str(iduser)
    res = CON.ejecutar_consulta_sel(query,None)
    if res==None or len(res)==0:
        ans = 'None'
    if res[0][0]==0:
        ans="Usuario"
    return ans 

@db.route('/actclave/<int:iduser>/<string:clave>')
def actclave(userid,clave):
    rpt = hashlib.md5(clave.encode())
    pwd = rpt.hexdigest()
    estado="A"
    query= "UPDATE usuario set clave = ? , estado = ? WHERE id = ?"
    res = CON.ejecutar_consulta_acc(query,(pwd, estado , int(userid)))
    if res!=None:
        ans = 'Datos registrados con éxito'
    else:   #else res
        ans= 'Error al registrar los datos'
    return ans

@db.route('/crearproducto/<string:nombre>/<string:referencia>/<int:cantidad>/<string:nombreImg>')
def crearproducto(nombre,referencia,cantidad,nombreImg):
    familia=1
    estado='A'
    query = "INSERT INTO producto(nombre, referencia, cantidad, imagen, familia, estado) VALUES(?, ?, ?, ?, ?, ?)"
    res = CON.ejecutar_consulta_acc(query,(nombre, referencia, cantidad, nombreImg, familia, estado))
    if res!=None:
        sal = 'Datos registrados con éxito'
    else:
        sal = 'Error al registrar los datos'
    return sal