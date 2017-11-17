$(document).ready(function() {
     var valorFiltre = getCookie("filtre_t");
     if(valorFiltre){
        crearTaulaFiltre(valorFiltre);
        //table.ajax.reload();
     }
});