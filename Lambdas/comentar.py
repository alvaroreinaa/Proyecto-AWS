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
    # Para saber si se ha subido correctamente el comentario
    error = "false"
    
    # Almacenamos los parámetros pasados por evento
    user_event = event["queryStringParameters"]["nombre_usuario"]
    name_video_event = event["queryStringParameters"]["nombre_video"]
    comment_event = event["queryStringParameters"]["comentario"]
    id_event = event["queryStringParameters"]["id_video"]
    
    try:
        with conn.cursor() as cur:
            # Insertamos el comentario en la BBDD
            cur.execute("INSERT INTO Comentarios (nombre_usuario, nombre_video, comentario, id) VALUES (%s,%s,%s,%s)", (user_event,name_video_event,comment_event,id_event))
            conn.commit()
            
            return {
                'statusCode': 200,
                'headers': { 'Access-Control-Allow-Origin' : '*' },
                'body':json.dumps({ 'error' :  str(error) })
            }
    except pymysql.MySQLError as e:
        error = "true"
        return {
            'statusCode': 200,
            'headers': { 'Access-Control-Allow-Origin' : '*' },
            'body':json.dumps({ 'error' :  str(error) })
        }
    