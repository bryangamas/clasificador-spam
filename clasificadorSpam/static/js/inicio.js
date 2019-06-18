$( document ).ready(()=> {
   var getUrl = window.location;
   var baseUrl = getUrl .protocol + "//" + getUrl.host + "/" + getUrl.pathname.split('/')[1];
   
   $btn_entrenar = $("#btn-entrenar")
   $btn_mensaje_aleatorio = $("#btn-msj-aleatorio")
   $area_mensaje = $("#text-area-msj")

   $btn_entrenar.on("click", ()=>{
      $btn_entrenar.find("i").toggleClass('fa-brain fa-spinner fa-pulse');
      //$btn_entrenar.attr('disabled', true);
   })

   $btn_mensaje_aleatorio.on("click", ()=>{
      $.ajax({
         url: baseUrl + "/aleatorio", 
         success: function(result){
            $area_mensaje.html(result.mensaje);
         }
      });
   })

});