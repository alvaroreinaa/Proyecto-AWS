# Proyecto AWS
Página web que simula una aplicación tipo Youtube realizada con los servicios RDS/Lambda/ApiGateway/S3 que ofrece AWS.

## Funcionalidades
- Login y registro de usuarios. 
  - Cuenta con opción de recuperación de contraseñas y bloqueo de cuentas al introducir mal estas.
- Por cada usuario, accede a una página web que permite subir videos, gestionarlos, y acceder a la pestaña de comunidad
  - **Subir**: Cuenta con un formulario para indicar el título, descripción, etiquetas del video y una comprobación de que este no está subido y el formato es el correcto. Si se trata de un vídeo, creará un thumbnail de este para su previsualización. Todos los vídeos se guardan en una carpeta privada que posee cada usuario en el S3.
  - **Gestionar**: Permite al usuario ver todos los vídeos que ha subido, con la posibilidad de borrarlos y acceder a ellos para reproducirlos, ver sus comentarios y valoraciones. Cuenta con una barra de búsqueda para buscar según etiquetas o nombre del vídeo.
  - **Comunidad**: Accede a una página que muestra los 5 vídeos más votados en orden descendente de todos los subidos por los usuarios con toda su información. Se pueden reproducir, abriendose en una pestaña nueva que mostrará las valoraciones y comentarios de este. 
Cuenta con una barra de búsqueda para buscar según etiquetas o nombre del vídeo. Esta búsqueda es de todos los existentes en la BBDD, ya que no se realiza la carga completa de todos esto en la comunidad, pudiendo así aparecer vídeos que no están en el top 5.
- En las valoraciones, solo se pueden realizar una voto positivo/negativo por usuario, aunque se puede cambiar a la valoración contraria si lo desea. 

## Nota
Actualmente las lambdas, RDS, ApiGateway y S3 no existen, pero el código sería exactamente el mismo teniendo que configurar usted los servicios (VPCs, Roles, Security groups,...etc) de AWS y sustituirlos por los míos.
