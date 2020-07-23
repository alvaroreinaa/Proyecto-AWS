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

    # Almacenamos las datos del evento
    id_event = event["queryStringParameters"]["id_video"]
    
    try:
        with conn.cursor() as cur:
            conn.commit()
            # Recuperamos los usuarios y los comentarios que han comentado en el video
            cur.execute("SELECT nombre_usuario FROM Comentarios WHERE id = %s", (id_event))
            users = cur.fetchall()
            cur.execute("SELECT comentario FROM Comentarios WHERE id = %s", (id_event))
            comments = cur.fetchall()
            

            return {
                'statusCode': 200,
                'headers': { 'Access-Control-Allow-Origin' : '*' },
                'body':json.dumps({ 'nombre_usuarios' :  users, 'comentarios' : comments })
            }
    except pymysql.MySQLError as e:
        print(e)
        return {
            'statusCode': 200,
            'headers': { 'Access-Control-Allow-Origin' : '*' },
            'body':json.dumps({ 'error' :  str("Error en BBDD") })
        }
    