var vuser = window.location.hash.substring(1);

function redirectToProfile()
{
  window.location.href = "../templates/perfil.html#" + vuser;
}

// Para obtener las keys del aws
function getAWSKeys() {
	var asd=$.get(
 			"https://ldsh1uob46.execute-api.us-east-1.amazonaws.com/AWS4S3Credentials",
		    {nombre_usuario: vuser},
		    function(data) {
		       document.getElementById("Policy").value = data.stringToSign;
		       document.getElementById("X-Amz-Credential").value = data.xAmzCredential;
		       document.getElementById("X-Amz-Date").value = data.amzDate;
		       document.getElementById("X-Amz-Signature").value = data.stringSigned;
		       document.getElementById("X-Amz-Security-Token").value = data.securityToken;
					 document.getElementById("successField").value = "http://webdistribuidos.s3.us-east-1.amazonaws.com/templates/perfil.html#" + vuser;
				}
		)
}

//Para crear el video en la BBDD
function createVideoDB(url,file) {
	var vsize = document.getElementById('file').files[0].size;
	var vnombre_video = document.getElementById("nombre_video").value;
	var vetiquetas = document.getElementById("etiquetas").value;

	var asd=$.get(
			"https://usccdojg21.execute-api.us-east-1.amazonaws.com/Upload",
			{nombre_usuario: vuser, size: vsize, nombre_video: vnombre_video, etiquetas: vetiquetas, url: url, nombre_fichero: file},
			function(data) {
				acceso = data.subidaCorrecta;
				if (acceso == "True"){
					alert("Su video se ha subido correctamente");
				}
				else {
					alert("Fallo al procesar su subida");
				}
			}
	)
}

// Para establecer las keys
function setKeyFilename(form) {
	var url = "http://webdistribuidos.s3.us-east-1.amazonaws.com/";
	form.action = url;
	document.getElementById("key").value = "usuarios/" + vuser + "/" + document.getElementById("file").value.substring(document.getElementById("file").value.lastIndexOf('\\')+1);
	// Almacenamos donde la url donde se va a guardar nuestro archivo y el nombre del fichero con su extension
	url = url + document.getElementById("key").value;
	file = document.getElementById("file").value.substring(document.getElementById("file").value.lastIndexOf('\\')+1);
  createVideoDB(url,file);
}

// Para comprobar si la extension es la correcta y el fichero no existe ya para el usuario
function checkFile()
{
	// Obtenemos el nombre del archivo que quiere subir el usuario y su extensión para realizar las comprobaciones necesarias
	var filename_extension = document.getElementById("file").value.substring(document.getElementById("file").value.lastIndexOf('\\')+1);
	var temp = filename_extension.split(".");
	var extension = temp[1];

	if (extension != "avi" && extension != "mp3" && extension != "mp4")
	{
		alert("Extension no soportada. Extensiones validas: .avi, .mp3, .mp4");
	}
	else
	{
		var asd=$.get(
	 			"https://s61r9b78qe.execute-api.us-east-1.amazonaws.com/Comprobar_archivo",
		    {nombre_usuario: vuser, nombre_fichero: filename_extension},
		    function(data) {
		       if (data.error == "True")
					 {
						 alert("Nombre de archivo repetido. Por favor, cambielo para poder subirlo.");
					 }
					 else
					 {
						 alert("Nombre de archivo y extension validos.");
						 document.getElementById("submit").disabled = false;
					 }
				}
			)
	}
}

// Para informar al usuario
function checkInformation()
{
	alert("Comprueba si usted ha subido ya un fichero con el mismo nombre que el actual o si el formato del video es el adecuado (.mp4)");
}
