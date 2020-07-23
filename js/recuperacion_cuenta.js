// Para ver la frase de recuperacion que esta oculta por defecto
function verFrase()
{
  var x = document.getElementById("frase_recuperacion");
  if (x.type === "password")
  {
    x.type = "text";
  }
  else
  {
    x.type = "password";
  }
}

// Cuando hagamos click, enviamos los datos para recuperar la cuenta
$(document).ready(function(){
  $("button").click(function(){
	var vnombre=document.getElementById("nombre_usuario").value;
	var vfrase=document.getElementById("frase_recuperacion").value;
  var vopcion = "cuenta";

    if (vnombre == '' || vfrase == '')
    {
      alert("Por favor, rellene ambos campos.");
    }
    else
    {
      var answer=$.get(
          "https://0vykchj5q7.execute-api.us-east-1.amazonaws.com/Recuperacion_password",
          {nombre_usuario: vnombre, frase_recuperacion: vfrase, opcion: vopcion},
          function(data) {
             acceso = data.exito;

             if (acceso == 'Usuario no encontrado') {
               alert(acceso);
             }
             else if (acceso == 'Su cuenta no esta desactivada')
             {
               alert(acceso)
             }
             else if (acceso == 'Frase incorrecta')
             {
               alert(acceso)
             }
             else {
               alert(acceso);
               window.location.href = "../templates/login.html"
             }

          }
      )
    }
  });
});
