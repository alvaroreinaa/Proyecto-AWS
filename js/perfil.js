  var user = window.location.hash.substring(1);

function getName() {
  document.getElementById("saludo").innerHTML = "Bienvenido " + user;
}

function redirectToUpload()
{
  window.location.href = "../templates/upload.html#" + user;
}

function redirectToMyVideos()
{
  window.location.href = "../templates/misvideos.html#" + user;
}

function redirectToCommunity()
{
  window.location.href = "../templates/comunidad.html#" + user;
}
