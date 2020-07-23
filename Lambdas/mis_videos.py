import sys, logging, pymysql, json, datetime

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

# Función que convierte de datetime (sql) a string
def converter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()
        
def lambda_handler(event , context):
    # Almacenamos el nombre de usuario para recuperar sus videos 
    user_event = event["queryStringParameters"]["nombre_usuario"]
    
    try:
        with conn.cursor() as cur:
            # Actualizamos la base de datos
            conn.commit()
            
            # Recuperamos los campos que vamos a mostrar al usuario en la tabla
            # - El titulo del video
            cur.execute("SELECT nombre_video FROM Videos WHERE nombre_usuario = %s", (user_event))
            titulo = cur.fetchall()
            # - Las etiquetas del video
            cur.execute("SELECT etiquetas_busqueda FROM Videos WHERE nombre_usuario = %s", (user_event))
            etiquetas = cur.fetchall()
            # - El tamaño del video
            cur.execute("SELECT size FROM Videos WHERE nombre_usuario = %s", (user_event))
            size = cur.fetchall()
            # - La fecha de subida del video
            cur.execute("SELECT fecha_subida FROM Videos WHERE nombre_usuario = %s", (user_event))
            fecha = cur.fetchall()
            fecha = json.dumps(fecha, default = converter)
            # - El enlace del video para descargarlo
            cur.execute("SELECT ruta_archivo FROM Videos WHERE nombre_usuario = %s", (user_event))
            enlace = cur.fetchall()
            # - El ID asociado al video
            cur.execute("SELECT id FROM Videos WHERE nombre_usuario = %s", (user_event))
            id = cur.fetchall()
            
            
        return {
            'statusCode': 200,
            'headers': { 'Access-Control-Allow-Origin' : '*' },
            'body':json.dumps({ 'titulo' :  titulo, 'etiquetas' : etiquetas, 'size' : size, 'fecha' : fecha, 'enlace' : enlace, 'id' : id})
        }
    except pymysql.MySQLError as e:    
        return {
            'statusCode': 200,
            'headers': { 'Access-Control-Allow-Origin' : '*' },
            'body':json.dumps({ 'error' :  str("error") })
        }