var user = window.location.hash.substring(1);

// Una vez este cargda toda la pagina web, recuperamos los datos de mis videos
$(document).ready (() => {
  var asd=$.get(
    "https://78kaz8akog.execute-api.us-east-1.amazonaws.com/Mis_videos",
    {nombre_usuario: user},
    function (datasource){
      var count = Object.keys(datasource.titulo).length;
      pintarTablaVideos(datasource,count);
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
function pintarTablaVideos(datasource, count)
{
  let thead = $('#theadVideos');
  thead.empty();
  thead.append(crearHeaders(['Titulo', 'Etiquetas', 'Size', 'Fecha de subida', 'Reproduccion', 'Eliminar']));

  let tbody = $('#tbodyVideos');
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
      let sizeTd = document.createElement('td');
      let fechaSubidaTd = document.createElement('td');
      let descargar = document.createElement('a');
      let verOnline = document.createElement('a');
      let enlaceTd = document.createElement('td');
      let botonBorrar = document.createElement('button');
      let borrarTd = document.createElement('td');

      tituloTd.innerText = datasource.titulo[i];
      etiquetasTd.innerText = datasource.etiquetas[i];
      sizeTd.innerText = (parseFloat(datasource.size[i] / 1000000).toFixed(2)) + " MB";
      fechaSubidaTd.innerText = datasource.fecha[i];

      descargar.href = datasource.enlace[i];
      descargar.innerHTML = "Descargar" + "<br>";
      enlaceTd.appendChild(descargar);

      verOnline.href = "../templates/video.html#" + user + "/" + datasource.id[i];
      verOnline.innerHTML = "Ver online";
      enlaceTd.appendChild(verOnline);

      botonBorrar.setAttribute('class', 'btn btn-danger');
      botonBorrar.setAttribute('id', 'botonBorrar');
      botonBorrar.innerText = 'Borrar';
      botonBorrar.id = datasource.id[i];

      $(botonBorrar).click(function (e) {
        var delete_user = "";
        var delete_archivo = "";

        var answer=$.get(
            "https://ii052jxr1k.execute-api.us-east-1.amazonaws.com/Borrar_video",
            {id: e.target.id},
            function(data) {
              acceso = data.borrado;

              if (acceso == "True")
              {
                alert("Video eliminado con exito");
              }
              else
              {
                alert("Error a eliminar el video");
              }

              datasource = []
              window.location.reload();
            }
        )
      });

      borrarTd.appendChild(botonBorrar);

      insertarCeldas(row, [tituloTd, etiquetasTd, sizeTd, fechaSubidaTd, enlaceTd, borrarTd]);
    }
  }
  // si no, muestra una alerta
  else
  {
    $('#tablaVideos').hide();
    alert("Actualmente no hay videos disponibles");
  }
}

// Funcion para buscar etiquetas en nuestra tabla
function buscarEtiquetas()
{
  // Declaramos variables
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("busqueda");
  filter = input.value.toUpperCase();
  table = document.getElementById("tablaVideos");
  tr = table.getElementsByTagName("tr");

  // Recorremos todas las filas de la tabla y ocultamos las que no coinciden con la busqueda
  for (i = 0;i < tr.length;i++)
  {
    td = tr[i].getElementsByTagName("td")[1];
    if (td)
    {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1)
      {
        tr[i].style.display = "";
      }
      else
      {
        tr[i].style.display = "none"
      }
    }
  }
}
