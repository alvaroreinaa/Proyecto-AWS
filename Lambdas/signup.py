import sys, logging, pymysql, json, boto3


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
    # Almacenamos los datos del nuevo usuario
    name_event = event["queryStringParameters"]["nombre_completo"]
    user_event = event["queryStringParameters"]["nombre_usuario"]
    email_event = event["queryStringParameters"]["correo_electronico"]
    password_event = event["queryStringParameters"]["password"]
    frase_event = event["queryStringParameters"]["frase_recuperacion"]
    tries = 0
    activo = 1
    
    try:
        with conn.cursor() as cur:
            # Introducimos en la tabla los datos del usuario
            cur.execute("INSERT INTO Usuarios (nombre_completo, nombre_usuario, correo_electronico, password, frase_recuperacion, intentos, activo) VALUES (%s,%s,%s,%s,%s,%s,%s)",(name_event, user_event, email_event, password_event, frase_event, tries, activo))
            conn.commit()
            
            return {
                'statusCode': 200,
                'headers': { 'Access-Control-Allow-Origin' : '*' },
                'body':json.dumps({ 'usuarioCreado' :  'Usuario creado con exito' })
            }
    except pymysql.MySQLError as e:    
        return {
            'statusCode': 200,
            'headers': { 'Access-Control-Allow-Origin' : '*' },
            'body':json.dumps({ 'usuarioCreado' :  "Nombre de usuario existente. Por favor, introduzca otro." })
        }
    