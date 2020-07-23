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

// Cuando hagamos click, enviamos los datos para recuperar la contraseña
$(document).ready(function(){
  $("button").click(function(){
	var vnombre=document.getElementById("nombre_usuario").value;
	var vfrase=document.getElementById("frase_recuperacion").value;
  var vopcion = "password";

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

             if (acceso == 'Usuario o frase incorrecta') {
               alert("Nombre de usuario o frase de recuperacion incorrecta");
             }
             else {
               acceso = acceso.split("").reverse().join("");
               alert("Su contrase\361a es " + acceso);
               window.location.href = "../templates/login.html"
             }
          }
      )
    }
  });
});
