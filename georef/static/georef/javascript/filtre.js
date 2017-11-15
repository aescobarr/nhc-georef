//$(document).ready(function() {

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

    function createValor(condicio,valor){
        if('nom'==condicio){
            return "<input type='text' value='"+valor+"' />";
        }else if('tipus'==condicio){
            return createSelect(valorsTipus,valor);
        }else if('pais'==condicio){
            return createSelect(valorsPaisos,valor);
        }else if('aquatic'==condicio){
            return createSelect(valorsAquatic,valor);
        }else if('geografic'==condicio){
            return createImportCartoButton(valor);
        }else{
            return "<input type='text' value='"+valor+"' />";
        }
        return "";
    }

    function createCheckNot(valueNot){
        var htmlChck = "<input type='checkbox' name='chcknot' />";
        if("S"==valueNot)
            htmlChck = "<input type='checkbox' name='chcknot' checked='checked' />";
        return htmlChck;
    }

    function esborrarFilaFiltre(indexTaulaAEsborrar){
        var fila = document.getElementById("fila_"+indexTaulaAEsborrar);
        if($('#select_condicio_'+indexTaulaAEsborrar).val()=='Geogràfic'){
            clearFeaturesMapa();
        }
        fila.parentNode.removeChild(fila);
    }

    function insertCondicioFiltre(operador,condicio,valor,not,indexTaulaNovaFila){
        var taula = $("#taulafiltre")[0];
        var selectOperador = createSelect(valorsOperadors,operador,'select_operador_'+indexTaulaNovaFila);
        if(taula.children.length==0){
            //només hi ha els titols de les columnes
            selectOperador = "&nbsp;";
        }
        var selectCondicio = createSelect(valorsCondicions,condicio,'select_condicio_'+indexTaulaNovaFila,'javascript:canviCondicio('+indexTaulaNovaFila+');');
        var valorCondicio = createValor(condicio,valor);
        var checkNot = createCheckNot(not);
        /*var botoEsborrar = "<input class='btn btn-danger' type='button' onclick='javascript:esborrarFilaFiltre("+indexTaulaNovaFila+");return false;' value='Esborrar'/>" +
                "<a href=\"#\" class=\"botoinfo\" title=\""+txtBotoEsborrarCondicioFiltre+"\">&nbsp;</a>";*/
        var botoEsborrar = '<button id="addCondicio" onclick="javascript:esborrarFilaFiltre('+indexTaulaNovaFila+');return false;" type="button" class="btn btn-danger">Esborrar <i class="fa fa-times" aria-hidden="true"></i></button>';
        var fila = "<td>"+selectOperador+"</td>";
        fila += "<td>"+checkNot+"</td>";
        fila += "<td>"+selectCondicio+"</td>";
        fila += "<td id='value_"+indexTaulaNovaFila+"'>"+valorCondicio+"</td>";
        fila += "<td>"+botoEsborrar+"</td>";
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

    function canviCondicio(indexTaulaFila){
        var select = document.getElementById('select_condicio_'+indexTaulaFila);
        var indexSelect = select.selectedIndex;
        var valueCondicio = select.options[indexSelect].id;
        var tdValue = document.getElementById('value_'+indexTaulaFila);
        var valorCondicio = createValor(valueCondicio,"");
        tdValue.innerHTML = valorCondicio;
    }

    function createImportCartoButton(valor){
        var boto = txtFuncionamentFiltreCarto;
        if(valor!=null && ''!=valor){
            //mostrarWTK(valor);
            //centrarMapaADigitalitzacio();
            //filtarCQLMapa(valor);
        }
        return boto;
    }

    $( "#addCondicio" ).click(function() {
         afegirCondicioFiltre();
    });



//});