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
    # El id de nuestro video
    id_event = event["queryStringParameters"]["id_video"]
    
    try:
        with conn.cursor() as cur:
            # Actualizamos la base de datos
            conn.commit()
            
            # Recuperamos los campos que vamos a mostrar a los usuarios
            # - El titulo del video
            cur.execute("SELECT nombre_video FROM Videos WHERE id = %s", (id_event))
            titulo = cur.fetchall()
            # - El enlace del video
            cur.execute("SELECT ruta_archivo FROM Videos WHERE id = %s", (id_event))
            enlace = cur.fetchall()
            # - El numero de votos positivos que tiene el video
            cur.execute("SELECT votos_positivos FROM VotosVideos WHERE id = %s", (id_event))
            votos_positivos = cur.fetchall()
            # - El numero de votos negativos que tiene el video
            cur.execute("SELECT votos_negativos FROM VotosVideos WHERE id = %s", (id_event))
            votos_negativos = cur.fetchall()
            # - El nombre del usuario que hizo el comentario
            cur.execute("SELECT nombre_usuario FROM Comentarios WHERE id = %s", (id_event))
            comentador = cur.fetchall()
            # - El contenido del comentario que realizó el usuario
            cur.execute("SELECT comentario FROM Comentarios WHERE id = %s", (id_event))
            comentario = cur.fetchall()
            
            
        return {
            'statusCode': 200,
            'headers': { 'Access-Control-Allow-Origin' : '*' },
            'body':json.dumps({ 'titulo' :  titulo, 'enlace' : enlace, 'votos_positivos' : votos_positivos, 'votos_negativos' : votos_negativos, 'comentador' : comentador, 'comentario' : comentario})
        }
    except pymysql.MySQLError as e:    
        return {
            'statusCode': 200,
            'headers': { 'Access-Control-Allow-Origin' : '*' },
            'body':json.dumps({ 'error' :  str("error") })
        }