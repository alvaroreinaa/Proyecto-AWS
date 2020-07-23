// Cuando hagamos click en el boton, enviamos los datos a la BBDD para comprobar el acceso
$(document).ready(function(){
  $("button").click(function(){
	var vnombre=document.getElementById("nombre_usuario").value;
	var vpassword=document.getElementById("password").value;

    if (vnombre == '' || vpassword == '')
    {
      alert("Por favor, rellene ambos campos.");
    }
    else
    {
      var acceso = false
      vpassword = vpassword.split("").reverse().join("");  // Nuestra "encriptación"

      var answer=$.get(
          "https://h9grwxbwak.execute-api.us-east-1.amazonaws.com/Login",
          {nombre_usuario: vnombre, password: vpassword},
          function(data) {
             acceso = data.accesoConcedido;

             if (acceso == 'True') {
               window.location.href = "../templates/perfil.html#" + vnombre;
             }
             else if (acceso == 'Usuario no encontrado'){
               alert("Nombre de usuario incorrecto");
             }
             else if (acceso == 'Password incorrecta'){
               alert("Password incorrecta");
             }
             else if (acceso == 'Numero de intentos superados. Cuenta deshabilitada'){
               alert("Numero de intentos superados. Cuenta deshabilitada");
               window.location.reload();
             }
             else {
               alert(acceso)
             }
          }
      )
    }
  });
});
