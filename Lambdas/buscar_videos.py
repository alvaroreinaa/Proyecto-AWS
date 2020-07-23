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
    # Almacenamos las palabras de búsqueda para poder recuperar un vídeo con esas palabras en el titulo o  etiquetas
    parameters_event = event["queryStringParameters"]["parametros"]
    parameters_event = parameters_event.split(" ")
    
    # Generamos una Query para recuperar todos los datos de cada video 
    # y añadimos todas las palabras para poder recuperar los videos de la BBDD
    query_videos = "SELECT Videos.nombre_video, Videos.etiquetas_busqueda, Videos.nombre_usuario, Videos.size, Videos.fecha_subida, Videos.ruta_archivo, Videos.id FROM Videos WHERE "
    for word in parameters_event:
        if (parameters_event.index(word) == (len(parameters_event) - 1)):
            query_videos = query_videos + "Videos.nombre_video LIKE " + "'" + '%' + word + '%' + "' "  + "OR " 
            query_videos = query_videos + "Videos.etiquetas_busqueda LIKE " + "'" + '%' + word + '%' + "' " 
        else:
            query_videos = query_videos + "Videos.nombre_video LIKE " + "'" + '%' + word + '%' + "' "  + "OR " 
            query_videos = query_videos + "Videos.etiquetas_busqueda LIKE " + "'" + '%' + word + '%' + "' "  + "OR " 
    
    # Los parámetros divididos decada video
    titulo = []
    etiquetas = []
    usuario = []
    size = []
    fecha = []
    enlace = []
    id = []
    votos_positivos = []
    votos_negativos = []

    try:
        with conn.cursor() as cur:
            # Actualizamos la base de datos
            conn.commit()

            # Recuperamos todos los campos de los videos cuyo titulo o etiquetas se encuentre en los parametros
            cur.execute(query_videos)
            videos = cur.fetchall()
            
            # Almacenamos los parametros de cada video
            for video in range(len(videos)):
                titulo.append(videos[video][0])
                etiquetas.append(videos[video][1])
                usuario.append(videos[video][2])
                size.append(videos[video][3])
                fecha.append(videos[video][4])
                enlace.append(videos[video][5])
                id.append(videos[video][6])

            # Los votos de cada vídeo recuperado
            for id_video in id:
                query_votosPositivos = "SELECT votos_positivos FROM VotosVideos WHERE id=" + str(id_video)
                cur.execute(query_votosPositivos)
                votos_positivos.append(cur.fetchone())
                
                query_votosNegativos = "SELECT votos_negativos FROM VotosVideos WHERE id=" + str(id_video)
                cur.execute(query_votosNegativos)
                votos_negativos.append(cur.fetchone())
                
            # Convertimos la fecha
            fecha = json.dumps(fecha, default = converter)


            
            
        return {
            'statusCode': 200,
            'headers': { 'Access-Control-Allow-Origin' : '*' },
            'body':json.dumps({ 'titulo' :  titulo, 'etiquetas' : etiquetas, 'usuario' : usuario, 'size' : size, 'fecha' : fecha, 'votos_positivos' : votos_positivos, 'votos_negativos' : votos_negativos, 'enlace' : enlace,  'id' : id})
        }
    except pymysql.MySQLError as e:  
        print(e)
        return {
            'statusCode': 200,
            'headers': { 'Access-Control-Allow-Origin' : '*' },
            'body':json.dumps({ 'error' :  str("error") })
        }