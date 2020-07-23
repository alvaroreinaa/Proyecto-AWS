var hash = window.location.hash.substring(1);
var hashes = hash.split("/");

// Una vez este cargada toda la pagina web
$(document).ready (() => {
  var asd=$.get(
    "https://657n59afr9.execute-api.us-east-1.amazonaws.com/Video",
    {id_video: hashes[1]},
    function (datasource){
      generarPagina(datasource);
    }
  );

  recuperarComentarios();
});

// Funcion que recupera los comentarios del video
function recuperarComentarios()
{
  var awd=$.get(
    "https://ri897rw0k6.execute-api.us-east-1.amazonaws.com/Recuperar_comentarios",
    {id_video: hashes[1]},
    function (datasource){
      var count = Object.keys(datasource.nombre_usuarios).length;
      generarComentarios(datasource,count);
    }
  );
}

function redirectToCommunity()
{
  window.location.href = "../templates/comunidad.html#" + hashes[0];
}

function redirectToProfile()
{
  window.location.href = "../templates/misvideos.html#" + hashes[0];
}

// Funcion para pintar la pagina
function generarPagina(datasource)
{
  document.getElementById("nombre_video").innerHTML = datasource.titulo;
  document.getElementById("video").setAttribute('src', datasource.enlace);
  document.getElementById("video").setAttribute('poster', datasource.enlace + "_thumb.gif");
  document.getElementById("voto_positivo").innerHTML = datasource.votos_positivos;
  document.getElementById("voto_negativo").innerHTML = datasource.votos_negativos;
}

// Funcion que manda el voto y actualiza los votos del video
function uploadVote(vote)
{
  var titulo = document.getElementById("nombre_video").innerText;

  var asd=$.get(
    "https://3a83ixcvt8.execute-api.us-east-1.amazonaws.com/Voto",
    {nombre_usuario: hashes[0], nombre_video: titulo, voto: vote, id_video: hashes[1]},
    function (data){
      document.getElementById("voto_positivo").innerHTML = data.votos_positivos;
      document.getElementById("voto_negativo").innerHTML = data.votos_negativos;

      if (data.error == "true")
      {
        alert("Usted ya ha votado esta opcion, pero puede cambiar su voto");
      }
    }
  );
}

// Para asignar un voto positivo
function uploadPositive()
{
  var vote = "1";
  uploadVote(vote);
}

// Para asignar un voto negativo
function uploadNegative()
{
  var vote = "-1";
  uploadVote(vote);
}

// Funcion que almacena el comentario respecto al video cuando se hace click en el boton
$(document).ready(function(){
  $("button").click(function(){
    var titulo = document.getElementById("nombre_video").innerText;
	  var vcomentario=document.getElementById("comentario").value;

    if (vcomentario == '')
    {
      alert("No se puden publicar comentarios vacios.");
    }
    else
    {
      var answer=$.get(
          "https://izbuqq1dql.execute-api.us-east-1.amazonaws.com/Comentar",
          {nombre_usuario: hashes[0], nombre_video: titulo, comentario: vcomentario, id_video: hashes[1]},
          function(data) {
            if (data.error == "true")
            {
              alert("Error al publicar el comentario");
            }
            else
            {
              document.getElementById("comentario").value = "";
              recuperarComentarios();
            }
          }
      )
    }
  });
});

// Funcion que genera los comentarios que se han hecho del video actualmente
function generarComentarios(datasource, count)
{
  let section = document.getElementById("comentarios");
  section.innerHTML = "";

  // Si el datasource tiene comentarios, los mostramos
  if (count > 0)
  {
    // Muestra todos los comentarios del video
    for (let i = 0; i < count;i++)
    {
      let usuario = document.createElement('label');
      let comentario = document.createElement('p');

      usuario.innerHTML = datasource.nombre_usuarios[i];
      comentario.innerHTML = datasource.comentarios[i];

      section.appendChild(usuario);
      section.appendChild(comentario);
    }
  }
}
