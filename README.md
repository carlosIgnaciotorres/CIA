# CIA
## Control de Inventarios de Accesorios

### SISTEMA DE INVENTARIOS PARA TIENDA DE ACCESORIOS  
Actualmente nuestra problemática consiste en que ocasionalmente no contamos con el estado de real del inventario de la tienda en un momento dado,  lo cual genera inconformidad con nuestros clientes generando una mala imagen de nuestra misión como empresa. Requerimos de una aplicación web para la gestión del inventario de accesorios de nuestra tienda, la cual nos permite conocer en cualquier momento el stock disponible en bodega.
La aplicación debe proveer las siguientes funcionalidades:
Registrar usuarios. Este registro solo debe ser realizado por el administrador, el cual se supone es una cuenta que existe desde el despliegue de la aplicación. Para este registro, el administrador debe autenticarse contra la aplicación y luego seleccionar la opción registrar, en donde debería suministrar la siguiente información para registrar un nuevo usuario: nombre de usuario, contraseña y correo electrónico.  La aplicación debe enviar un e-mail al correo del nuevo usuario registrado con las credenciales asignadas.
Proveer un portal de acceso, donde los usuario puedan acceder al sistema, si se autentican, usando usuario y contraseñas, exitosamente. Esto debe cumplir con los requerimientos mínimos de seguridad.
Ofrecer la opción para recuperar la contraseña en caso de olvido para los usuarios. Esta opción puede ser implementada, por ejemplo, por medio del envío de un e-mail al correo electrónico registrado para el usuario.
Ofrecer la opción para la creación, actualización y eliminación de productos. Esto solo debe ser realizado por el administrador. Es decir, el usuario administrador puede crear, actualizar y/o dar de baja a un accesorio. En la creación de un artículo se debería ingresar referencia (un identificador para el producto), nombre del producto, cantidad,  y una imagen del producto.
Un usuario autenticado puede buscar un producto usando una palabra clave para el nombre y esta búsqueda mostrará una galería de imágenes.
Un usuario autenticado puede actualizar las cantidades de un producto particular. Es decir, se debe permitir actualizar la cantidad de un producto haciendo click en la respectiva imagen del producto.
Vista inicio de sesión


# Desarrollo: 
## Requerimientos
### Requerimientos funcionales

1.	CRUD de productos.
2.	Manejo por perfil de usuarios (administrador y almacenista).
3.	Mostrar catálogo de los productos con información de cada uno.
4.	Permitir al administrador actualizar el catálogo de productos.
5.	Proporcionar a los usuarios registrados la opción de cambiar la cantidad de los productos.

## Casos de uso

|ID requerimiento |CIA-001|
|----------------|----------|
|Nombre del requerimiento | Iniciar Sesión|
|Actores | Administrador o Usuario|
|Prerrequisitos|El usuario se debe encontrar registrado en la base de datos, con todos sus datos completos de acuerdo a los requisitos solicitados por la aplicación.|
|Descripción |El usuario debe ingresar usuario y contraseña que tiene registrados en la base de datos, con los cuales se pueda autenticar ante el servidor.  El sistema valida los datos ingresados contra los que tiene almacenados y devuelve una respuesta, validando la información suministrada.|
|Resultado | El sistema acepta o rechaza la conexión del usuario |

|ID requerimiento| CIA-002|
|----------------|----------|
|Nombre del requerimiento|Registro de Usuario|
|Actores|Administrador (Principal), usuario(Secundario)|
|Prerrequisitos|El administrador del sistema debe tener todos los datos requeridos del usuario que pretende realizar el registro en la plataforma de Control de Inventarios de Accesorios.|
|Descripción|El sistema solicita una serie de campos obligatorios que deben ser llenados por el usuario administrador para poder realizar el registro, una vez se envían los datos, el sistema valida que cumplan con los requisitos mínimos y crea un usuario nuevo en la base de datos con estado sin validar correo y envia un mail al usuario para realizar la confirmación del mismo. |
|Resultado|El sistema acepta o rechaza los datos brindados, creando un nuevo usuario en el caso afirmativo, pero sin validar.|


|ID requerimiento|CIA-003|
|----------------|----------|
|Nombre del requerimiento|Validación de Usuario|
|Actores|Usuario o Administrador|
|Prerrequisitos|El sistema debe tener registrado un usuario con estado correo sin validar.|
|Descripción|El usuario lee desde su correo un mensaje de validación y acepta el mismo mediante un link que confirma la existencia o no del correo del usuario|
|Resultado|El estado del usuario en la base de datos cambia a validado si se hace clic en el link del correo en caso contrario continúa sin validar. Se pedirá una nueva contraseña y la verificación de la misma|


|ID requerimiento|CIA-004|
|----------------|----------|
|Nombre del requerimiento|Recuperar contraseña|
|Actores|Usuario o administrador|
|Prerrequisitos|El sistema debe tener registrado un usuario con estado correo validado.|
|Descripción|El usuario lee desde su correo un mensaje de solicitud de cambio de contraseña y acepta el mismo mediante un link que confirma la solicitud o no en el correo del usuario|
|Resultado|Si se hace clic en el link del correo, se pedirá una nueva contraseña y la verificación de la misma. Si no hace clic en el link del correo la contraseña no cambia y no se hace recuperación de la misma |


|ID requerimiento|CIA-005 |
|----------------|----------|
|Nombre del requerimiento|Crear Producto|
|Actores|Administrador|
|Prerrequisitos|El administrador del sistema debe tener todos los datos requeridos como referencia, nombre, cantidad e imagen del producto que desea crear en la plataforma de Control de Inventarios de Accesorios.|
|Descripción|El sistema solicita una serie de campos obligatorios que deben ser llenados por el usuario administrador para poder realizar la creación del producto. Una vez se envían los datos, el sistema valida que cumplan con los requerimientos y crea un producto nuevo en la base de datos.|
|Resultado|El sistema acepta o rechaza los datos brindados, creando un nuevo producto en el caso afirmativo. En caso negativo, muestra un mensaje de error en la validación de datos.|


|ID requerimiento|CIA-006| 
|----------------|----------|
|Nombre del requerimiento|Actualizar Producto|
|Actores|Administrador|
|Prerrequisitos|El administrador del sistema debe tener los datos requeridos del producto para poder actualizarlo.|
|Descripción|El sistema solicita al administrador el nombre o referencia del producto que desea actualizar, seguidamente el sistema valida que el producto exista, en caso positivo se procede  ingresar los datos a actualizar del producto, estos datos son verificados para ver si cumplen con los requisitos y por último se actualiza el producto.|
|Resultado|El sistema acepta o rechaza los datos brindados, haciendo la actualización del producto en caso positivo. En caso negativo, muestra un mensaje de error en la actualización  por fallo con la validación de datos.|


|ID requerimiento|CIA-007 |
|----------------|----------|
|Nombre del requerimiento|Eliminar Producto|
|Actores|Administrador|
|Prerrequisitos|El administrador del sistema debe tener datos como la referencia o nombre del producto para poder eliminarlo.|
|Descripción|El sistema solicita al administrador el nombre o referencia del producto que desea eliminar, seguidamente el sistema valida que el producto exista y en caso positivo se procede a eliminar el producto.|
|Resultado|El sistema elimina el producto en caso de que exista. En caso de no existir, el sistema muestra un mensaje de no existencia del producto.|


|ID requerimiento|CIA-008 |
|----------------|----------|
|Nombre del requerimiento|Buscar producto|
|Actores|Usuario o Administrador|
|Prerrequisitos|El usuario ya debe haber ingresado el login, debe tener el nombre o referencia del producto.|
|Descripción|El sistema solicita al usuario el nombre o referencia del producto que desea buscar, seguidamente el sistema valida que el producto exista y en caso positivo se procede a mostrar una galería de imágenes con los producto, con todos sus atributos y su cantidad.|
|Resultado|El sistema muestra el producto en caso de que exista. En caso de no existir, el sistema muestra un mensaje de no existencia del producto.|

|ID requerimiento|CIA-009 |
|----------------|----------|
|Nombre del requerimiento|Actualizar Cantidades de Producto|
|Actores|Usuario o Administrador|
|Prerrequisitos|El usuario para ejecutar la acción debe ser puede ser Usuario o Administrador, tener el nombre o referencia del producto a actualizar.|
|Descripción|El sistema solicita al usuario o administrador el nombre o referencia del producto que desea actualizar, seguidamente el sistema valida que el producto exista y en caso positivo se procede a validar la nueva cantidad de productos, validará si el valor es positivo, cuando estas validaciones sean negativa muestra un mensaje que menciona el procedimiento no es válido.|
|Resultado|Si la cantidad es positiva esta será la nueva cantidad del producto y si es negativa no se ejecutará el cambio y sacará un mensaje.|




