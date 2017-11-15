$(document).ready(function() {

    var indexTaula = 0;

    var valorsOperadors = new Array();
    valorsOperadors[0] = {id : "and", value : "AND"};
    valorsOperadors[1] = {id : "or", value : "OR" };

    function createSelect(valors,idselected,idselect,onchange){
        var htmlSelect = '<select class="input-field"';
        if(idselect!=null && idselect!=undefined)
            htmlSelect += " id='"+idselect+"'";
        if(idselect!=null && idselect!=undefined)
            htmlSelect += " onchange='"+onchange+"'";
        htmlSelect += ">";
        for(var i=0;i<valors.length;i++){
            if(idselected==valors[i].id)
                htmlSelect += "<option id='"+valors[i].id+"' selected='selected'>"+valors[i].value+"</option>";
            else
                htmlSelect += "<option id='"+valors[i].id+"'>"+valors[i].value+"</option>";
        }
        htmlSelect += "</select>";
        return htmlSelect;
    }

    function insertCondicioFiltre(operador,condicio,valor,not,indexTaulaNovaFila){
        var taula = $("#taulafiltre")[0];
        var selectOperador = createSelect(valorsOperadors,operador,'select_operador_'+indexTaulaNovaFila);
        /*if(taula.children.length==1){
            //només hi ha els titols de les columnes
            selectOperador = "";
        }
        var selectCondicio = createSelect(valorsCondicions,condicio,'select_condicio_'+indexTaulaNovaFila,'javascript:canviCondicio('+indexTaulaNovaFila+');');
        var valorCondicio = createValor(condicio,valor);
        var checkNot = createCheckNot(not);
        var botoEsborrar = "<input type='button' onclick='javascript:esborrarFilaFiltre("+indexTaulaNovaFila+");return false;' value='Esborrar'/>" +
                "<a href=\"#\" class=\"botoinfo\" title=\""+txtBotoEsborrarCondicioFiltre+"\">&nbsp;</a>";*/
        var fila = "<td>"+selectOperador+"</td>";
        /*fila += "<td>"+checkNot+"</td>";
        fila += "<td>"+selectCondicio+"</td>";
        fila += "<td id='value_"+indexTaulaNovaFila+"'>"+valorCondicio+"</td>";
        fila += "<td>"+botoEsborrar+"</td>";*/
        var newtr = document.createElement('tr');
        newtr.setAttribute('id','fila_'+indexTaulaNovaFila);
        newtr.setAttribute('name','trfiltre');
        newtr.innerHTML = fila;
        taula.appendChild(newtr);
    }

    function afegirCondicioFiltre(){
        insertCondicioFiltre("and", "", "", "N", indexTaula);
        indexTaula++;
    }

    $( "#addCondicio" ).click(function() {
         afegirCondicioFiltre();
    });

});