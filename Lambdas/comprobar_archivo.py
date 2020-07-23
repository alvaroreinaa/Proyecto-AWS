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
    error = False
    
    # Almacenamos el nombre de usuario y nombre del fichero 
    user_event = event["queryStringParameters"]["nombre_usuario"]
    file_event = event["queryStringParameters"]["nombre_fichero"]
    
    try:
        with conn.cursor() as cur:
            # Comprobamos que el usuario no haya subido ningun video con ese nombre de fichero
            cur.execute("SELECT nombre_fichero FROM Videos WHERE nombre_usuario = %s AND nombre_fichero = %s", (user_event,file_event))
            file = cur.fetchall()
            
            if not file:
                pass
            else:
                error = True
            
            return {
                'statusCode': 200,
                'headers': { 'Access-Control-Allow-Origin' : '*' },
                'body':json.dumps({ 'error' :  str(error) })
            }
    except pymysql.MySQLError as e:    
        error = True
            
        return {
            'statusCode': 200,
            'headers': { 'Access-Control-Allow-Origin' : '*' },
            'body':json.dumps({ 'error' :  str(error) })
        }