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
    
def lambda_handler(event , context):
    # Para comprobar que se han almacenado los datos correctamente en la base de datos
    subidaCorrecta = False
    
    # Almacenamos el nombre de usuario, tamaño del archivo, nombre del video, nombre del fichero y etiquetas
    user_event = event["queryStringParameters"]["nombre_usuario"]
    size_event  = event["queryStringParameters"]["size"]
    name_video_event = event["queryStringParameters"]["nombre_video"]
    labels_event = event["queryStringParameters"]["etiquetas"]
    file_path_event = event["queryStringParameters"]["url"]
    file_event = event["queryStringParameters"]["nombre_fichero"]
    
    # El parámetro adicional que falta
    time = datetime.datetime.utcnow()

    
    try:
        with conn.cursor() as cur:
            # Insertamos los datos en la base de datos
            cur.execute("INSERT INTO Videos (nombre_usuario, nombre_video, nombre_fichero, etiquetas_busqueda, size, ruta_archivo, fecha_subida) VALUES (%s,%s,%s,%s,%s,%s,%s)", (user_event, name_video_event, file_event, labels_event, size_event, file_path_event, time))
            conn.commit()
            
            # Creo su fila en la tabla de sus votos total
            num = 0
            cur.execute("SELECT id FROM Videos WHERE nombre_usuario = %s AND nombre_fichero = %s", (user_event,file_event))
            id = cur.fetchone()
            cur.execute("INSERT INTO VotosVideos (nombre_video, votos_positivos, votos_negativos, id) VALUES (%s,%s,%s,%s)", (name_video_event, num, num, id[0]))
            conn.commit()
            subidaCorrecta = True
            
            
            return {
                'statusCode': 200,
                'headers': { 'Access-Control-Allow-Origin' : '*' },
                'body':json.dumps({ 'subidaCorrecta' :  str(subidaCorrecta) })
            }
    except pymysql.MySQLError as e:    
        subidaCorrecta = False
            
        return {
            'statusCode': 200,
            'headers': { 'Access-Control-Allow-Origin' : '*' },
            'body':json.dumps({ 'subidaCorrecta' :  str(subidaCorrecta) })
        }