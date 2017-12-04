$(document).ready(function() {
     var valorFiltre = getCookie("filtre_t");

     if(valorFiltre){
        crearTaulaFiltre(valorFiltre);
     }
     var layer_toponims = djangoRef.Map.getOverlayByHandle('toponims');
     filterCQL(valorFiltre,layer_toponims);

});