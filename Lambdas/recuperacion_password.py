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
    # Nuestra variable para saber si se ha realizado la operacion correctamente
    exito = False
    
    # Almacenamos el usuario, contraseña y opcion pasados por evento
    user_event = event["queryStringParameters"]["nombre_usuario"]
    sentence_event = event["queryStringParameters"]["frase_recuperacion"]
    option_event = event["queryStringParameters"]["opcion"] 

    try:
        with conn.cursor() as cur:
            if (option_event == "password"):
                # Miramos en la BBDD si existen un usuario con ese nombre y esa frase de recuperación
                cur.execute("SELECT frase_recuperacion FROM Usuarios WHERE nombre_usuario=%s AND frase_recuperacion=%s", (user_event, sentence_event))
                users = cur.fetchall()
                
                # Si esta vacía, significa que el usuario o la frase es incorrecta
                if not users:
                    exito = "Usuario o frase incorrecta"
                # Si es correcta la frase y usuario, devolvemos al usuario su contraseña
                else:
                    cur.execute("SELECT password FROM Usuarios WHERE nombre_usuario=%s AND frase_recuperacion=%s", (user_event, sentence_event))
                    passwd = cur.fetchone()
                    exito = passwd[0]
            elif (option_event == "cuenta"):
                # Miramos en la BBDD si el usuario tiene la cuenta deshabilitada
                cur.execute("SELECT activo FROM Usuarios WHERE nombre_usuario=%s", (user_event))
                active = cur.fetchone()
                
                #Si esta vacía, significa que el usuario
                if not active:
                    exito = "Usuario no encontrado"
                # Si no está vacía, significa que el usuario existe
                else:
                    # Si tiene 1, significa que esta activada
                    if active[0] == '1':
                        exito = "Su cuenta no esta desactivada"
                    else:
                        # Miramos en la BBDD si existen un usuario con ese nombre y esa frase de recuperación
                        cur.execute("SELECT nombre_usuario FROM Usuarios WHERE nombre_usuario=%s AND frase_recuperacion=%s", (user_event, sentence_event))
                        users = cur.fetchall()
                        
                        # Si esta vacía, significa que la frase es incorrecta
                        if not users:
                            exito = "Frase incorrecta"
                        # Si es correcta la frase y usuario, activamos al usuario su cuenta
                        else:
                            cur.execute("UPDATE Usuarios SET activo = 1 WHERE nombre_usuario=%s", (users))
                            cur.execute("UPDATE Usuarios SET intentos = 0 WHERE nombre_usuario=%s", (users))
                            conn.commit()
                            exito = "Cuenta recuperada con exito"
                    
            return {
                'statusCode': 200,
                'headers': { 'Access-Control-Allow-Origin' : '*' },
                'body':json.dumps({ 'exito' :  str(exito) })
            }
    except pymysql.MySQLError as e:    
        return {
            'statusCode': 200,
            'headers': { 'Access-Control-Allow-Origin' : '*' },
            'body':json.dumps({ 'exito' :  str(exito) })
        }
    