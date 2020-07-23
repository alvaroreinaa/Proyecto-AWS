var user = window.location.hash.substring(1);

// Una vez este cargda toda la pagina web, recuperamos los datos de los videos
$(document).ready (() => {
  var asd=$.get(
    "https://rqq3tmu0b3.execute-api.us-east-1.amazonaws.com/Comunidad",
    {},
    function (datasource){
      var count = Object.keys(datasource.titulo).length;
      pintarTablaComunidad(datasource,count);
    }
  );
});

function redirectToProfile()
{
  window.location.href = "../templates/perfil.html#" + user;
}

// Función para crear los headers de las tablas
function crearHeaders(headers)
{
  let rowHeaders = document.createElement('tr');
  headers.forEach((h) => {
    let header = document.createElement('th');
    header.innerText = h;
    rowHeaders.appendChild(header);
  });

  return rowHeaders;
}

// Función para crear las filas de las tablas
function crearFila(tbody)
{
  let row = document.createElement('tr');
  tbody.append(row);
  return row;
}

// Función para insertar las celdas de cada columna en la fila
function insertarCeldas(row, cells)
{
  cells.forEach((c) => {
    row.appendChild(c);
  });
}

// Funcion para limpiar nuestras fechas de caracteres
function cleanDate(date)
{
  for(var x = 0; x < Object.keys(date).length; x++)
  {
      date[x] = date[x].replace('[', ' ');
      date[x] = date[x].replace('[', ' ');
      date[x] = date[x].replace('"', ' ');
      date[x] = date[x].replace('"', ' ');
      date[x] = date[x].replace(']', ' ');
      date[x] = date[x].replace(']', ' ');
  }
}

// Funcion para pintar nuestros videos en la tabla
function pintarTablaComunidad(datasource, count)
{
  let thead = $('#theadComunidad');
  thead.empty();
  thead.append(crearHeaders(['Titulo', 'Etiquetas', 'Usuario', 'Size', 'Fecha de subida', 'Votos', 'Reproduccion']));

  let tbody = $('#tbodyComunidad');
  tbody.empty();

  // Convertimos la fecha (string) a un array para poder iterar
  datasource.fecha = datasource.fecha.split(",");
  cleanDate(datasource.fecha);

  // Si el datasource tiene videos, mostramos la tabla
  if (count > 0)
  {
    // Muestra todos los videos del usuario
    for (let i = 0; i < count;i++)
    {
      let row = crearFila(tbody);

      let tituloTd = document.createElement('td');
      let etiquetasTd = document.createElement('td');
      let usuarioTd = document.createElement('td');
      let sizeTd = document.createElement('td');
      let fechaSubidaTd = document.createElement('td');
      let votoPositivo = document.createElement('p');
      let votoNegativo = document.createElement('p');
      let votoTd = document.createElement('td');
      let descargar = document.createElement('a');
      let verOnline = document.createElement('a');
      let enlaceTd = document.createElement('td');


      tituloTd.innerText = datasource.titulo[i];
      etiquetasTd.innerText = datasource.etiquetas[i];
      usuarioTd.innerText = datasource.usuario[i];
      sizeTd.innerText = (parseFloat(datasource.size[i] / 1000000).toFixed(2)) + " MB";
      fechaSubidaTd.innerText = datasource.fecha[i];

      votoPositivo.innerHTML = "<b>Votos Positivos</b>:" + datasource.votos_positivos[i];
      votoNegativo.innerHTML = "<b>Votos Negativos</b>:" + datasource.votos_negativos[i];
      votoTd.appendChild(votoPositivo);
      votoTd.appendChild(votoNegativo);

      descargar.href = datasource.enlace[i];
      descargar.innerHTML = "Descargar" + "<br>";
      enlaceTd.appendChild(descargar);

      verOnline.href = "../templates/video.html#" + user + "/" + datasource.id[i];
      verOnline.innerHTML = "Ver online";
      enlaceTd.appendChild(verOnline);

      insertarCeldas(row, [tituloTd, etiquetasTd, usuarioTd, sizeTd, fechaSubidaTd, votoTd, enlaceTd]);
    }
  }
  // si no, muestra una alerta
  else
  {
    $('#tablaComunidad').hide();
    alert("Actualmente no hay videos disponibles");
  }
}


// Funcion para buscar videos de la BBDD con los parámetros introducidos por el usuario
function findVideos()
{
  var input = document.getElementById("busqueda").value;

  if (input == "")
  {
    var asd=$.get(
      "https://rqq3tmu0b3.execute-api.us-east-1.amazonaws.com/Comunidad",
      {},
      function (datasource){
        var count = Object.keys(datasource.titulo).length;
        pintarTablaComunidad(datasource,count);
      }
    );
  }
  else {
    var asd=$.get(
      "https://imlgxtcith.execute-api.us-east-1.amazonaws.com/Buscar_videos",
      {"parametros" : input},
      function (datasource){
        if (datasource.error == "error")
        {
          alert("Consulta no valida")
        }
        else {
          var count = Object.keys(datasource.titulo).length;
          if (count == 0)
          {
            alert("No existen videos con esa busqueda")
          }
          else {
            pintarTablaComunidad(datasource,count);
          }
        }
      }
    );
  }

}
