$(document).ready(function() {
    var valorFiltre = getCookie('filtre_r');

    if(valorFiltre){
        crearTaulaFiltre(valorFiltre);
    }
    var layer_recursos = djangoRef.Map.getOverlayByHandle('recursos');
    filterCQL(valorFiltre,layer_recursos);
});