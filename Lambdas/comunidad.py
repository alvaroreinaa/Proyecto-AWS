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
    try:
        with conn.cursor() as cur:
            # Actualizamos la base de datos
            conn.commit()

            # Recuperamos los 5 videos más votados
            # - El titulo del video
            cur.execute("SELECT Videos.nombre_video FROM Videos LEFT JOIN VotosVideos ON Videos.id = VotosVideos.id ORDER BY votos_positivos DESC LIMIT 5")
            titulo = cur.fetchall()
            # - Las etiquetas del video
            cur.execute("SELECT Videos.etiquetas_busqueda FROM Videos RIGHT JOIN VotosVideos ON Videos.id = VotosVideos.id ORDER BY votos_positivos DESC LIMIT 5")
            etiquetas = cur.fetchall()
            # - El nombre de usuario que lo subió
            cur.execute("SELECT Videos.nombre_usuario FROM Videos LEFT JOIN VotosVideos ON Videos.id = VotosVideos.id ORDER BY votos_positivos DESC LIMIT 5")
            usuario = cur.fetchall()
            # - El tamaño del video
            cur.execute("SELECT Videos.size FROM Videos RIGHT JOIN VotosVideos ON Videos.id = VotosVideos.id ORDER BY votos_positivos DESC LIMIT 5")
            size = cur.fetchall()
            # - La fecha de subida del video
            cur.execute("SELECT Videos.fecha_subida FROM Videos LEFT JOIN VotosVideos ON Videos.id = VotosVideos.id ORDER BY votos_positivos DESC LIMIT 5")
            fecha = cur.fetchall()
            fecha = json.dumps(fecha, default = converter)
            # - El número de votos positivo del video
            cur.execute("SELECT votos_positivos FROM VotosVideos ORDER BY votos_positivos DESC LIMIT 5")
            votos_positivos = cur.fetchall()
            # - El número de votos negativos del video
            cur.execute("SELECT votos_negativos FROM VotosVideos ORDER BY votos_positivos DESC LIMIT 5")
            votos_negativos = cur.fetchall()
            # - El enlace del video para descargarlo
            cur.execute("SELECT Videos.ruta_archivo FROM Videos RIGHT JOIN VotosVideos ON Videos.id = VotosVideos.id ORDER BY votos_positivos DESC LIMIT 5")
            enlace = cur.fetchall()
            # - El ID asociado al video
            cur.execute("SELECT Videos.id FROM Videos LEFT JOIN VotosVideos ON Videos.id = VotosVideos.id ORDER BY votos_positivos DESC LIMIT 5")
            id = cur.fetchall()
            
            
        return {
            'statusCode': 200,
            'headers': { 'Access-Control-Allow-Origin' : '*' },
            'body':json.dumps({ 'titulo' :  titulo, 'etiquetas' : etiquetas, 'usuario' : usuario, 'size' : size, 'fecha' : fecha, 'votos_positivos' : votos_positivos, 'votos_negativos' : votos_negativos, 'enlace' : enlace,  'id' : id})
        }
    except pymysql.MySQLError as e:    
        return {
            'statusCode': 200,
            'headers': { 'Access-Control-Allow-Origin' : '*' },
            'body':json.dumps({ 'error' :  str("error") })
        }