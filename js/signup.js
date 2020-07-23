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

// Cuando hagamos click, enviamos los datos para registrar al usuario
$(document).ready(function(){
  $("button").click(function(){
  	var vnombre = document.getElementById("nombre_completo").value;
    var vuser = document.getElementById("nombre_usuario").value;
    var vemail = document.getElementById("correo_electronico").value;
  	var vpassword = document.getElementById("password").value;
    var vfrase = document.getElementById("frase_recuperacion").value;


    if (vnombre == '' || vuser == '' || vemail == '' || vpassword == '' || vfrase == '')
    {
      alert("Por favor, rellene todos los campos.")
    }
    else if (vemail.includes("@") == Boolean(false))
    {
      alert("Email invalido");
    }
    else
    {
      vpassword = vpassword.split("").reverse().join("");  // Nuestra "encriptación"

      var answer=$.get(
          "https://v2wk64r6t1.execute-api.us-east-1.amazonaws.com/signup",
          {nombre_completo: vnombre, nombre_usuario: vuser, correo_electronico: vemail, password: vpassword, frase_recuperacion: vfrase},
          function(data) {
             acceso = data.usuarioCreado;

             if (acceso == 'Usuario creado con exito') {
               alert(acceso);
               window.location.href = "../templates/login.html"
             }
             else {
               alert(acceso);
             }
          }
      )
    }
  });
});
