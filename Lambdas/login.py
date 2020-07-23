import sys, logging, pymysql, json


# Características de nuestra base de datos
rds_host = "database-1.cxbdsjdsqeq5.us-east-1.rds.amazonaws.com"
username = "admin"
password ="root1234"
dbname = "Youtube"

try:
    conn = pymysql.connect(rds_host, user=username, passwd=password, db=dbname, connect_timeout=10)
except pymysql.MySQLError as e:
    print (e)
    sys.exit()
    
def lambda_handler(event , context):
    # Nuestra variable para saber si los datos introducidos son válidos
    accesoConcedido = False
    
    # Almacenamos el usuario y contraseña pasados por evento
    user_event = event["queryStringParameters"]["nombre_usuario"]
    password_event = event["queryStringParameters"]["password"]
    
    try:
        with conn.cursor() as cur:
            # Primero miramos en la BBDD si existen un usuario con ese nombre
            cur.execute("SELECT nombre_usuario FROM Usuarios WHERE nombre_usuario=%s", (user_event))
            users = cur.fetchall()

            # Si esta vacía, significa que no existe y le denegamos el acceso
            if not users:
                accesoConcedido = "Usuario no encontrado"
            # Si no, significa que se encuentra y comprobamos la contraseña
            else:
                # Miramos si el usuario ha llegado a tres intentos
                cur.execute("SELECT intentos FROM Usuarios WHERE nombre_usuario=%s", (user_event))
                attempts = cur.fetchone()
                
                if (attempts[0] >= 3):
                    accesoConcedido = "Numero de intentos superados. Cuenta deshabilitada"
                else:
                    cur.execute("SELECT password FROM Usuarios WHERE nombre_usuario=%s AND password=%s", (user_event,password_event))
                    passwd = cur.fetchone()
                    
                    # Si la contraseña no es correcta
                    if not passwd:
                        accesoConcedido = "Password incorrecta"
                        # Actualizamos los intentos de acceso, incrementando en uno
                        cur.execute("UPDATE Usuarios SET intentos=intentos + 1 WHERE nombre_usuario=%s", (user_event))
                        conn.commit()
                        # Miramos si el usuario ha llegado a tres intentos
                        cur.execute("SELECT intentos FROM Usuarios WHERE nombre_usuario=%s", (user_event))
                        attempts = cur.fetchone()
                        
                        # Si tiene tres intentos, deshabilitamos la cuenta
                        if attempts[0] >= 3:
                            accesoConcedido = "Numero de intentos superados. Cuenta deshabilitada"
                            cur.execute("UPDATE Usuarios SET activo = 0 WHERE nombre_usuario=%s", (user_event))
                            conn.commit()
                        # Si no, no hacemos nada
                        else: 
                            pass
                    # Si es correcta, le damos acceso y reiniciamos los intentos
                    else:
                        accesoConcedido = True
                        cur.execute("UPDATE Usuarios SET intentos=0 WHERE nombre_usuario=%s", (user_event))
                        conn.commit()
                    
            return {
                'statusCode': 200,
                'headers': { 'Access-Control-Allow-Origin' : '*' },
                'body':json.dumps({ 'accesoConcedido' :  str(accesoConcedido) })
            }
    except pymysql.MySQLError as e:    
        return {
            'statusCode': 200,
            'headers': { 'Access-Control-Allow-Origin' : '*' },
            'body':json.dumps({ 'accesoConcedido' :  str("Error en BBDD") })
        }