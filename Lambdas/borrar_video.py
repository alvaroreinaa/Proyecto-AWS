import sys, logging, pymysql, json
import boto3



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
    # Almacenamos el id del video para poder borrarlo de la base de datos 
    id_event = event["queryStringParameters"]["id"]
    
    try:
        with conn.cursor() as cur:
            # Recuperamos datos antes de borrar para eliminar el video del S3
            cur.execute("SELECT nombre_usuario FROM Videos WHERE id = %s", (id_event))
            user_name = cur.fetchone()
            cur.execute("SELECT nombre_fichero FROM Videos WHERE id = %s", (id_event))
            file_name = cur.fetchone()
            # Ejecutamos la consulta para borrar el video y todo lo relacionado con este
            cur.execute("DELETE FROM Videos WHERE id = %s", (id_event))
            conn.commit()
            cur.execute("DELETE FROM Comentarios WHERE id = %s", (id_event))
            conn.commit()
            cur.execute("DELETE FROM Votos WHERE id = %s", (id_event))
            conn.commit()
            cur.execute("DELETE FROM VotosVideos WHERE id = %s", (id_event))
            conn.commit()
            
            # Configuración de nuestro bucket
            bucket_name = "webdistribuidos"
            file_name = 'usuarios/' + str(user_name[0]) + '/' + str(file_name[0])
            
            # Borramos el video y su thumbnail
            s3 = boto3.resource("s3")
            s3.Object(bucket_name, file_name).delete()
            s3.Object(bucket_name, file_name + "_thumb.gif").delete()
            
        return {
            'statusCode': 200,
            'headers': { 'Access-Control-Allow-Origin' : '*' },
            'body':json.dumps({ 'borrado': str("True")})
        }
    except pymysql.MySQLError as e:    
        return {
            'statusCode': 200,
            'headers': { 'Access-Control-Allow-Origin' : '*' },
            'body':json.dumps({ 'borrado' :  str("False") })
        }
