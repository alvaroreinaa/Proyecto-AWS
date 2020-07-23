$(document).ready(function(){
  $("button").click(function(){
	var vmatrizX=document.getElementById("matrizX").value;
  var vmatrizY=document.getElementById("matrizY").value;

  var answer=$.get(
      "https://cjaqn5gc91.execute-api.us-east-1.amazonaws.com/Matrices",
      {matrizX: vmatrizX, matrizY: vmatrizY},
      function(data) {
         // Si devuelve el enlace, redirigimos para descargar
         if (data.resultado)
         {
           window.location.href = data.resultado;
         }
         // Si es un error se lo mostramos
         else if (data.error) {
           alert(data.error)
         }
      }
  )
  });
});
