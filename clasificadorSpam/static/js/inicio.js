$( document ).ready(()=> {
   
   $btn_entrenar = $("#btn-entrenar")

   $btn_entrenar.on("click", ()=>{
      $btn_entrenar.find("i").toggleClass('fa-brain fa-spinner fa-pulse');
   })

});