$(document).ready(function(){
  $("button").click(function(){
	var vnombre=document.getElementById("nombre_usuario").value;
	var vfrase=document.getElementById("frase_recuperacion").value;

    if (vnombre == '' || vfrase == '')
    {
      alert("Por favor, rellene ambos campos.");
    }
    else
    {
      var answer=$.get(
          "https://0vykchj5q7.execute-api.us-east-1.amazonaws.com/Recuperacion_password",
          {nombre_usuario: vnombre, frase_recuperacion: vfrase},
          function(data) {
             acceso = data.passwordRecuperada;

             if (acceso == 'Usuario o frase incorrecta') {
               alert("Nombre de usuario o frase de recuperacion incorrecta");
             }
             else {
               alert("Su password es " + acceso);
               window.location.href = "../templates/login.html"
             }
          }
      )
    }
  });
});
