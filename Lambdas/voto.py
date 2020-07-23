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
    # Nuestra variable de error
    error = "false"
    
    # Almacenamos las datos del evento
    user_event = event["queryStringParameters"]["nombre_usuario"]
    name_video_event = event["queryStringParameters"]["nombre_video"]
    vote_event = event["queryStringParameters"]["voto"]
    id_event = event["queryStringParameters"]["id_video"]
    
    try:
        with conn.cursor() as cur:
            # Antes de insertar el voto, comprobamos que el usuario vota por primera vez este video
            cur.execute("SELECT nombre_usuario FROM Votos WHERE nombre_usuario = %s AND id = %s", (user_event, id_event))
            user = cur.fetchone()
            
            # Si esta vacio significa que todavía no ha votado
            if not user:
                # Insertamos el voto en la tabla Votos
                cur.execute("INSERT INTO Votos (nombre_usuario, nombre_video, voto, id) VALUES (%s,%s,%s,%s)", (user_event,name_video_event,vote_event,id_event))
                conn.commit()
                
                # Actualizamos los votos totales del video según sea positivo o negativo
                if (vote_event == "1"):
                    cur.execute("UPDATE VotosVideos SET votos_positivos = votos_positivos + 1 WHERE id = %s", (id_event))
                    conn.commit()
                elif (vote_event == "-1"):
                    cur.execute("UPDATE VotosVideos SET votos_negativos = votos_negativos + 1 WHERE id = %s", (id_event))
                    conn.commit()
            # si no está vacío, significa que está votando lo mismo o quiere cambiar su voto
            else:
                cur.execute("SELECT nombre_usuario FROM Votos WHERE nombre_usuario = %s AND id = %s AND voto = %s", (user_event, id_event, vote_event))
                vote = cur.fetchone()
                
                # Si esta vacio significa que quiere cambiar su voto
                if not vote:
                    if (vote_event == "1"):
                        # Actualizamos su voto primero
                        cur.execute("UPDATE Votos SET voto = 1 WHERE nombre_usuario = %s AND id = %s", (user_event, id_event))
                        conn.commit()
                        # Actualizamos los votos totales del video
                        cur.execute("UPDATE VotosVideos SET votos_positivos = votos_positivos + 1 WHERE id = %s", (id_event))
                        conn.commit()
                        cur.execute("UPDATE VotosVideos SET votos_negativos = votos_negativos - 1 WHERE id = %s", (id_event))
                        conn.commit()
                    elif (vote_event == "-1"):
                        # Actualizamos su voto primero
                        cur.execute("UPDATE Votos SET voto = -1 WHERE nombre_usuario = %s AND id = %s", (user_event, id_event))
                        conn.commit()
                        # Actualizamos los votos totales del video
                        cur.execute("UPDATE VotosVideos SET votos_negativos = votos_negativos + 1 WHERE id = %s", (id_event))
                        conn.commit()
                        cur.execute("UPDATE VotosVideos SET votos_positivos = votos_positivos - 1 WHERE id = %s", (id_event))
                        conn.commit()
                # si no está vacio signfica que quiere votar lo mismo y no le dejamos
                else:
                    error = "true"
                
            
            
            # Recuperamos los votos positivos y negativos del video para mostrarlos actualizados en la web
            cur.execute("SELECT votos_positivos FROM VotosVideos WHERE id = %s", (id_event))
            votos_positivos = cur.fetchone()
            cur.execute("SELECT votos_negativos FROM VotosVideos WHERE id = %s", (id_event))
            votos_negativos = cur.fetchone()

            return {
                'statusCode': 200,
                'headers': { 'Access-Control-Allow-Origin' : '*' },
                'body':json.dumps({ 'votos_positivos' :  votos_positivos, 'votos_negativos' : votos_negativos, 'error' : error })
            }
    except pymysql.MySQLError as e:
        return {
            'statusCode': 200,
            'headers': { 'Access-Control-Allow-Origin' : '*' },
            'body':json.dumps({ 'accesoConcedido' :  str("Error en BBDD") })
        }