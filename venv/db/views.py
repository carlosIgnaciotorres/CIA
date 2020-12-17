import hashlib
from . import db
import  conexion as CON
import json
from datetime import datetime


@db.route('/crearusuario/<string:nombre>/<string:apellido>/<string:documento>/<string:correo>/<string:direccion>/<string:celular>')
def crearusuario(nombre, apellido,documento,correo,direccion,celular):
    try:
        if 'usr_id' in session:
            tipoU=1
            estadoU="A"
            query = "INSERT INTO usuario(nombre, apellido, documento, correo, direccion, celular, tipoDoc,  estado ) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?)"
            res = CON.ejecutar_consulta_acc(query,(nombre, apellido, documento, correo, direccion, celular, tipoU,  estadoU ))
            if res!=None:
                sal = 'True'
            else:
                sal = 'False'
            return sal
        else:
            return redirect(url_for('/'))
    except:
        return 'Error en Views crearusuario'
    

@db.route('/usuario/<int:id>')
def usuario(id):
    try:
        if 'usr_id' in session:
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
    except:
        return 'Error en Views usuario'

@db.route('/existeusuario/<string:correo>')
def existeusuario(correo):
    try:
        if 'usr_id' in session:
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
    except:
        return 'Error en Views existeusuario'

@db.route('/loginusuario/<string:correo>/<string:clave>')
def loginusuario(correo,clave):
    try:
        if 'usr_id' in session:
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
    except:
        return 'Error en Views usuario'

@db.route('/borrarusuario/<int:iduser>')
def borrarusuario(iduser):
    try:
        if 'usr_id' in session:
            ans = "True"
            borrado='B'
            query= "UPDATE usuario SET estado= ? WHERE id = ?" 
            print(f" SQL: {query}")
            res = CON.ejecutar_consulta_acc(query,(borrado, iduser))
            if res==None or len(res)==0:
                ans = "False"
            return ans 
    except:
        return 'Error en Views usuario'

@db.route('/actualizarusuario/<int:iduser>/<string:correo>/<string:nombre>/<string:apellido>/<string:celular>/<string:documento>/<string:direccion>')
def actualizarusuario(iduser, correo, nombre, apellido, celular, documento, direccion):
    try:
        if 'usr_id' in session:
            ans = "True"
            borrado='B'
            query= f"UPDATE usuario SET correo = ?, nombre = ?, apellido = ?, celular = ?, documento = ?, direccion = ? WHERE id = ?" 
            print(f" SQL: {query}")
            res = CON.ejecutar_consulta_acc(query,(correo, nombre, apellido, celular, documento, direccion, iduser))
            if res==None or len(res)==0:
                ans = "False"
            return ans 
    except:
        return 'Error en Views usuario'

@db.route('/inactivarusuario/<int:iduser>')
def inactivarusuario(iduser):
    try:
        if 'usr_id' in session:
            ans = "True"
            borrado='I'
            query= "UPDATE usuario SET estado= ? WHERE id = ?" 
            print(f" SQL: {query}")
            res = CON.ejecutar_consulta_acc(query,(borrado, iduser))
            if res==None or len(res)==0:
                ans = "False"
            return ans 
    except:
        return 'Error en Views usuario'

@db.route('/genlink/<string:correo>')
def genlink(correo):
    try:
        if 'usr_id' in session:
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
    except:
        return 'Error en Views usuario'                                     

@db.route('/pruebalink/<string:link>')
def pruebalink(link):
    try:
        if 'usr_id' in session:
            ans = "True"
            query= "SELECT count(id)  FROM usuario WHERE linkrecuperacion = '" +link + "'"
            res = CON.ejecutar_consulta_sel(query,None)
            if res==None or len(res)==0:
                ans = "False"
            return ans
    except:
        return 'Error en Views usuario'

@db.route('/tipoUser/<int:iduser>')
def tipousuario(iduser):
    try:
        if 'usr_id' in session:
            ans = 'Administrador'
            query= "SELECT count(id)  FROM usuario WHERE estado='X' and id = "+str(iduser)
            res = CON.ejecutar_consulta_sel(query,None)
            if res==None or len(res)==0:
                ans = 'None'
            if res[0][0]==0:
                ans="Usuario"
            return ans 
    except:
        return 'Error en Views usuario'

@db.route('getCompletName/<int:iduser>')
def getCompletName(iduser):
    try:
        if 'usr_id' in session:
            query= "SELECT nombre, apellido  FROM usuario WHERE  id = "+str(iduser)
            res = CON.ejecutar_consulta_sel(query,None)
            print(f'SQL: {query}/n/n result:{res}')
            if res==None or len(res)==0:
                ans = 'None'
            else: 
                ans= res[0][0]+" "+res[0][1]
            return ans 
    except:
        return 'Error en Views usuario'

@db.route('/actclave/<int:iduser>/<string:clave>')
def actclave(userid,clave):
    try:
        if 'usr_id' in session:
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
    except:
        return 'Error en Views usuario'

@db.route('/producto/<int:id>')
def galeria(id):
    try:
        if 'usr_id' in session:
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
    except:
        return 'Error en Views usuario'

@db.route('/crearproducto/<string:nombre>/<string:referencia>/<int:cantidad>/<string:nombreImg>')
def crearproducto(nombre,referencia,cantidad,nombreImg):
    try:
        if 'usr_id' in session:
            familia=1
            estado='A'
            query = "INSERT INTO producto(nombre, referencia, cantidad, imagen, familia, estado) VALUES(?, ?, ?, ?, ?, ?)"
            res = CON.ejecutar_consulta_acc(query,(nombre, referencia, cantidad, nombreImg, familia, estado))
            if res!=None:
                sal = 'Datos registrados con éxito'
            else:
                sal = 'Error al registrar los datos'
            return sal
    except:
        return 'Error en Views usuario'

@db.route('/borrarProducto/<int:idproducto>')
def borrarProducto(idproducto):
    try:
        if 'usr_id' in session:
            familia=1
            estado='A'
            query = "UPDATE  producto set estado ='I' WHERE id = ?"
            res = CON.ejecutar_consulta_acc(query,( int(idproducto)))
            if res!=None:
                sal = 'True'
            else:
                sal = 'False'
            return sal
    except:
        return 'Error en Views usuario'
    
@db.route('/actualizarproducto/<int:idproducto>/<string:nombre>/<string:referencia>/<int:cantidad>/<string:nombreImg>')
def actualizarproducto(nombre,referencia,cantidad,nombreImg):
    try:
        if 'usr_id' in session:
            familia=1
            estado='A'
            query = "UPDATE  producto set nombre=?, referencia=?, cantidad=?, imagen=? WHERE id=?"
            res = CON.ejecutar_consulta_acc(query,(nombre, referencia, cantidad, nombreImg, id))
            if res!=None:
                sal = 'Datos actualizados con éxito'
            else:
                sal = 'Error al registrar los datos'
            return sal
    except:
        return 'Error en Views usuario'