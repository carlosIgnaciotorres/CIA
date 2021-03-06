import hashlib
from . import db
import  conexion as CON
import json
from datetime import datetime


@db.route('/crearusuario/<string:nombre>/<string:apellido>/<string:documento>/<string:correo>/<string:direccion>/<string:celular>')
def crearusuario(nombre, apellido,documento,correo,direccion,celular):
    tipoU=1
    estadoU="A"
    query = "INSERT INTO usuario(nombre, apellido, documento, correo, direccion, celular, tipoDoc,  estado ) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?)"
    res = CON.ejecutar_consulta_acc(query,(nombre, apellido, documento, correo, direccion, celular, tipoU,  estadoU ))
    if res!=None:
        sal = 'True'
    else:
        sal = 'False'
    return sal

@db.route('/usuario/<int:id>')
def usuario(id):
    query= "SELECT id, correo, nombre, apellido, celular, documento, direccion, estado FROM usuario  "
    print(CON.cifrardatos(query))
    print()
    print(CON.descifrardatos(CON.cifrardatos(query)))
    if int(id) > 0:
        query =query + 'WHERE id = '+ str(id)
        res = CON.ejecutar_consulta_sel(query,None)
    else:
        res = CON.ejecutar_consulta_sel(query, None)
    json_res = json.dumps(res)
    return json_res

@db.route('/existeusuario/<string:correo>')
def existeusuario(correo):
    ans = -1
    query= f"SELECT id FROM usuario WHERE correo = '{correo}'" 
    print(f" SQL: {query}")
    res = CON.ejecutar_consulta_sel(query,None)
    print(res)
    if res==None or len(res)==0:
        ans = -1
    else:
        ans=res[0][0]
    return str(ans) 

@db.route('/loginusuario/<string:correo>/<string:clave>')
def loginusuario(correo,clave):
    ans = -1
    rpt = hashlib.md5(clave.encode())
    pwd = rpt.hexdigest()
    pwd[::-1]
    estado="A"
    query= f"SELECT id FROM usuario WHERE correo = '{correo}' and clave ='{pwd}' and not estado='I' " 
    print(f" SQL: {query}")
    res = CON.ejecutar_consulta_sel(query,None)
    print(res)
    if res==None or len(res)==0:
        ans = -1
    else:
        ans=res[0][0]
    return str(ans) 

@db.route('/borrarusuario/<int:iduser>')
def borrarusuario(iduser):
    ans = "True"
    borrado='B'
    query= "UPDATE usuario SET estado= ? WHERE id = ?" 
    print(f" SQL: {query}")
    res = CON.ejecutar_consulta_acc(query,(borrado, iduser))
    if res==None or len(res)==0:
        ans = "False"
    return ans 

@db.route('/actualizarusuario/<int:iduser>/<string:correo>/<string:nombre>/<string:apellido>/<string:celular>/<string:documento>/<string:direccion>')
def actualizarusuario(iduser, correo, nombre, apellido, celular, documento, direccion):
    ans = "True"
    borrado='B'
    query= f"UPDATE usuario SET correo = ?, nombre = ?, apellido = ?, celular = ?, documento = ?, direccion = ? WHERE id = ?" 
    print(f" SQL: {query}")
    res = CON.ejecutar_consulta_acc(query,(correo, nombre, apellido, celular, documento, direccion, iduser))
    if res==None or len(res)==0:
        ans = "False"
    return ans 

@db.route('/inactivarusuario/<int:iduser>')
def inactivarusuario(iduser):
    ans = "True"
    borrado='I'
    query= "UPDATE usuario SET estado= ? WHERE id = ?" 
    print(f" SQL: {query}")
    res = CON.ejecutar_consulta_acc(query,(borrado, iduser))
    if res==None or len(res)==0:
        ans = "False"
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
    ans = "True"
    query= "SELECT count(id)  FROM usuario WHERE linkrecuperacion = '" +link + "'"
    res = CON.ejecutar_consulta_sel(query,None)
    if res==None or len(res)==0:
        ans = "False"
    return ans

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

@db.route('getCompletName/<int:iduser>')
def getCompletName(iduser):
    query= "SELECT nombre, apellido  FROM usuario WHERE  id = "+str(iduser)
    res = CON.ejecutar_consulta_sel(query,None)
    print(f'SQL: {query}/n/n result:{res}')
    if res==None or len(res)==0:
        ans = 'None'
    else: 
        ans= res[0][0]+" "+res[0][1]
    return ans 

@db.route('/actclave/<int:iduser>/<string:clave>')
def actclave(userid,clave):
    rpt = hashlib.md5(clave.encode())
    pwd = rpt.hexdigest()
    pwd[::-1]
    estado="A"
    query= "UPDATE usuario set clave = ? , estado = ? WHERE id = ?"
    res = CON.ejecutar_consulta_acc(query,(pwd, estado , int(userid)))
    if res!=None:
        ans = 'Datos registrados con éxito'
    else:   #else res
        ans= 'Error al registrar los datos'
    return ans

@db.route('/producto/<int:id>')
def galeria(id):
    query= "SELECT id, nombre, referencia, imagen, cantidad FROM producto WHERE estado = 'A'"
    lista=[]
    if int(id) > 0:
        query = query + ' and id = '+ str(id)
        res = CON.ejecutar_consulta_sel(query, None)
    else:
        res = CON.ejecutar_consulta_sel(query, None)
        count=0
    """ for row in res:
        lista[count]=[row]
        count+=1 """
    
    # for (row in res):
    #     lista.add(row)
    json_res = json.dumps(res)
    jdecode=json.loads(json_res)
    #return json_res+ "   -   "+ str(len(jdecode)) +" --- "+str(jdecode[3][3])
    return json_res

@db.route('/productocomo/<string:dato>')
def galeriacomo(dato):
    dato='%'+dato+'%'
    query= "SELECT id, nombre, referencia, imagen, cantidad FROM producto WHERE estado = 'A' and (nombre like ? or referencia like ?)"
    lista=[]
    res = CON.ejecutar_consulta_sel(query, (dato,dato))
    json_res = json.dumps(res)
    jdecode=json.loads(json_res)
    #return json_res+ "   -   "+ str(len(jdecode)) +" --- "+str(jdecode[3][3])
    return json_res

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

@db.route('/borrarProducto/<int:idproducto>')
def borrarProducto(idproducto):
    query = f"UPDATE  producto set estado ='I' WHERE id = {idproducto}"
    res = CON.ejecutar_consulta_acc(query, None)
    if res!=None:
        sal = 'El producto fue borrado Correctamente'
    else:
        sal = 'El producto no se pudo Borrar'
    return sal
    
@db.route('/actualizarproducto/<int:idproducto>/<string:nombre>/<string:referencia>/<int:cantidad>')
def actualizarproducto(idproducto, nombre,referencia,cantidad):
    query = "UPDATE  producto set nombre=?, referencia=?, cantidad=?  WHERE id=?"
    res = CON.ejecutar_consulta_acc(query,(nombre, referencia, cantidad,  idproducto))
    if res!=None:
        sal = 'Datos actualizados con éxito'
    else:
        sal = 'Error al registrar los datos'
    return sal
        
@db.route('/actualizarcantidad/<int:idproducto>/<int:cantidad>')
def actualizarcantidad(idproducto, cantidad):
    query = "UPDATE  producto set cantidad=?  WHERE id=?"
    res = CON.ejecutar_consulta_acc(query,( cantidad,  idproducto))
    if res!=None:
        sal = 'Datos actualizados con éxito'
    else:
        sal = 'Error al registrar los datos'
    return sal

@db.route('/crearhistorico/<string:idpro>/<int:iduser>/<int:cantidadant>/<string:cantidadnueva>')
def crearhistorico(idpro,iduser,cantidadant,cantidadnueva):
    
    query = "INSERT INTO historico (producto, usuario, cantidadant, cantidadnueva, Fecha ) VALUES (?,?,?,?,? );"
    res = CON.ejecutar_consulta_acc(query,(idpro, iduser, cantidadant, cantidadnueva, datetime.now()))
    if res!=None:
        sal = 'Datos registrados con éxito'
    else:
        sal = 'Error al registrar los datos'
    return sal

@db.route('/cantidadprod/<int:idproducto>')
def cantidadprod(idproducto):
    ans=0
    query = "SELECT  cantidad FROM producto  WHERE id="+str(idproducto)
    res = CON.ejecutar_consulta_sel(query,None)
    print(res)
    if res==None or len(res)==0:
        ans = 0
    else:
        ans=res[0][0]
    return str(ans) 

@db.route('/ultimoprod/')
def ultimoprod():
    ans=0
    query = "SELECT  max(id) FROM producto "
    res = CON.ejecutar_consulta_sel(query,None)
    print(res)
    if res==None or len(res)==0:
        ans = 0
    else:
        ans=res[0][0]
    return str(ans) 