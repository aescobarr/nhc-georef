from georef.models import Toponim, Tipustoponim, Pais, Qualificadorversio, Recursgeoref, Toponimversio
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models import Q
import operator, functools

class NumberOfColumnsException(Exception):
    pass


class EmptyFileException(Exception):
    pass


def check_file_structure(file_array):
    if len(file_array) < 2:
        raise EmptyFileException()
    numlinia = 1
    for rows in file_array:
        if len(rows) != 17:
            raise NumberOfColumnsException({"numrow": str(numlinia), "numcols": str(len(rows))})
        numlinia = numlinia + 1


def toponim_exists(line):
    try:
        return Toponim.objects.get(linia_fitxer_importacio=line)
    except Toponim.DoesNotExist:
        return None


def get_georeferencer_by_name(name):
    name_parts = name.split(' ')
    filter_clause = []
    if len(name_parts) > 0:
        first_name = name_parts[0]
        filter_clause.append( Q(**{ 'first_name__iexact': first_name }) )
        if len(name_parts) > 1:
            last_name = name_parts[1]
            filter_clause.append( Q(**{'last_name__iexact': last_name }) )
            try:
                return User.objects.get(functools.reduce(operator.and_, filter_clause))
            except User.DoesNotExist:
                pass
    return None


def get_model_by_attribute(attribute_name, attribute_value, model_name):
    try:
        filter_clause = Q(**{ attribute_name + '__iexact' : attribute_value } )
        return model_name.objects.get(filter_clause)
    except model_name.DoesNotExist:
        return None


def get_toponim_nom_estructurat(nom_toponim):
    if nom_toponim != '':
        if '-' in nom_toponim:
            filter_clause = []
            nom_info_addicional = nom_toponim.split('-')
            nom = nom_info_addicional[0].strip()
            info_addicional = nom_info_addicional[1].strip().split('(')
            pais = info_addicional[0].strip().lower()
            tipusToponim = info_addicional[1].replace(")", "").strip().lower()
            aquatic = info_addicional[2].replace(")", "").strip().lower() != 'terrestre'
            aquatic_string = ''
            if aquatic == True:
                aquatic_string = 'S'
            else:
                aquatic_string = 'N'
            p = get_model_by_attribute('nom', pais, Pais)
            tt = get_model_by_attribute('nom', tipusToponim, Tipustoponim)
            if p is not None:
                filter_clause.append( Q(**{ 'idpais' : p } ) )
            if tt is not None:
                filter_clause.append(Q(**{ 'idtipustoponim' : tt } ) )
            filter_clause.append(Q(**{ 'aquatic' : aquatic_string } ) )
            filter_clause.append(Q(**{'nom': nom}))
            return Toponim.objects.filter(functools.reduce(operator.and_, filter_clause))
        else:
            return Toponim.objects.filter(nom__icontains=nom_toponim)
    return None


def register_error(num_line, message, problems):
    lineNums = []
    try:
        lineNums = problems[message]
        lineNums.append(num_line)
        problems[message] = lineNums
    except KeyError:
        lineNums.append(num_line)
        problems[message] = lineNums


def process_line(line, line_string, errors, toponims_exist, toponims_to_create, line_counter, problemes, nomFitxer):
    t = toponim_exists(line_string)
    if t is None:
        # [0] - Nom toponim --> Cap comprovacio(comprovar blancs)
        nom = ''
        # [1] - Tipus toponim --> Buscar toponim per nom TipusToponim
        tt = None
        # [2] - Pais --> Buscar pais per nom Pais
        p = None
        # [3] - Aquatic --> Cap comprovacio
        aquatic = 'N'
        # [4] - Node superior --> Buscar toponim per nom(multiples resultats?)
        pare = None
        # [5] - Numero de versio
        numeroVersio = -1
        # [6] - Qualificador de la versió
        qv = None
        # [7] - Versio capturada del recurs RecursGeoreferenciacio
        rg = None
        # [8] - Nom del toponim al recurs
        nomToponimRecurs = None
        # [9] - Data
        data = None
        # [10] - Coord x original
        coordX_original = None
        # [11] - Coord y original
        coordY_original = None
        # [12] - Coord z
        coordZ_original = None
        # [13] - Incertesa de coordenada
        precisioH = None
        # [14] - Incertesa h
        precisioZ = None
        # [15] - Georeferenciador
        georeferenciador = None
        # [16] - Observacions
        observacions = None

        errorsALinia = False
        errorsLinia = []
        errorsLiniaActual = []

        if line[0] == '' or line[0].strip() == '':
            errorsALinia = True
            errorsLiniaActual.append("Nom de toponim en blanc a la columna 1")
            register_error(line_counter, "Nom de toponim en blanc a la columna 1", problemes)
        else:
            nom = line[0].strip()

        if line[1] == '' or line[1].strip() == '':
            errorsALinia = True
            errorsLiniaActual.append("Tipus de toponim en blanc a la columna 2")
            register_error(line_counter, "Tipus de toponim en blanc a la columna 2", problemes)
        else:
            tt = get_model_by_attribute('nom', line[1].strip(), Tipustoponim)
            if tt is None:
                errorsALinia = True
                errorsLiniaActual.append("No s'ha trobat el tipus de toponim '" + line[1] + "' a la columna 2")
                register_error(line_counter, "No s'ha trobat el tipus de toponim '" + line[1] + "' a la columna 2", problemes)

        if line[2] == '' or line[2].strip() == '':
            errorsALinia = True
            errorsLiniaActual.append("País en blanc a la columna 3")
            register_error(line_counter, "País en blanc a la columna 3", problemes)
        else:
            p = get_model_by_attribute('nom', line[2].strip(), Pais)
            if p is None:
                errorsALinia = True
                errorsLiniaActual.append("No s'ha trobat el país '" + line[2] + "' a la columna 3")
                register_error(line_counter, "No s'ha trobat el país '" + line[2] + "' a la columna 3", problemes)

        if line[3] == '' or line[3].strip() == '':
            errorsALinia = True
            errorsLiniaActual.append("Aquatic en blanc a la columna 4")
            register_error(line_counter, "Aquatic en blanc a la columna 4", problemes)
        else:
            if line[3].strip().lower() in ['true', 'cert', 'sí', 'si', '1', 'cierto', 'verdadero']:
                aquatic = 'S'

        if line[4] == '' or line[4].strip() == "":
            pare = None
        else:
            ts = get_toponim_nom_estructurat(line[4])
            if len(ts) == 0:
                errorsALinia = True
                errorsLiniaActual.append("No trobo cap topònim node superior amb nom '" + line[4] + "' a la columna 5")
                register_error(line_counter, "No trobo cap topònim node superior amb nom '" + line[4] + "' a la columna 5", problemes)
            elif len(ts) == 1:
                pare = ts[0]
            else:
                errorsALinia = True
                errorsLiniaActual.append("Hi ha múltiples topònims  node superior amb nom '" + line[4] + "' a la columna 5")
                register_error(line_counter, "Hi ha múltiples topònims  node superior amb nom '" + line[4] + "' a la columna 5", problemes)

        if line[5] == '' or line[5].strip().lower() == '':
            errorsALinia = True
            errorsLiniaActual.append("Número de versió en blanc a la columna 6")
            register_error(line_counter, "Número de versió en blanc a la columna 6", problemes)
        else:
            try:
                numeroVersio = int(line[5])
            except ValueError:
                errorsALinia = True
                errorsLiniaActual.append("No sé convertir en nombre '" + line[5] + "' a la columna 6")
                register_error(line_counter, "No sé convertir en nombre '" + line[5] + "' a la columna 6", problemes)

        if line[6] is None or line[6].strip().lower() == '':
            qv = None # No és obligatori
        else:
            qv = get_model_by_attribute('qualificador', line[6].strip(), Qualificadorversio)
            if qv is None:
                errorsALinia = True
                errorsLiniaActual.append("No trobo el qualificador de versió '" + line[6] + "' a la columna 7")
                register_error(line_counter, "No trobo el qualificador de versió '" + line[6] + "' a la columna 7", problemes)

        if line[7] is None or line[7].strip().lower() == '':
            errorsALinia = True
            errorsLiniaActual.append("El recurs de georeferenciacio en que es basa el recurs està en blanc a la columna 8")
            register_error(line_counter, "El recurs de georeferenciacio en que es basa el recurs està en blanc a la columna 8", problemes)
        else:
            rg = get_model_by_attribute('nom', line[7].strip(), Recursgeoref)
            if rg is None:
                errorsALinia = True
                errorsLiniaActual.append("No trobo el recurs de georeferenciació '" + line[7] + "' a la columna 8")
                register_error(line_counter, "No trobo el recurs de georeferenciació '" + line[7] + "' a la columna 8", problemes)

        if line[8] is None or line[8].strip().lower() == '':
            errorsALinia = True
            errorsLiniaActual.append("El nom del topònim al recurs de georeferenciacio està en blanc a la columna 9")
            register_error(line_counter, "El nom del topònim al recurs de georeferenciacio està en blanc a la columna 9", problemes)
        else:
            nomToponimRecurs = line[8]

        if line[9] is None or line[9].strip().lower() == '':
            data = None
        else:
            try:
                data = datetime.strptime(line[9].strip(), '%d/%m/%Y')
            except ValueError:
                errorsALinia = True
                errorsLiniaActual.append("Error convertint " + line[9] + " a format data a  la columna 10")
                register_error(line_counter, "Error convertint " + line[9] + " a format data a  la columna 10", problemes)

        #x coord
        if line[10] is None or line[10].strip().lower() == '':
            errorsALinia = True
            errorsLiniaActual.append("La coordenada x original està en blanc a la columna 11")
            register_error(line_counter, "La coordenada x original està en blanc a la columna 11", problemes)
        else:
            coordX_original = None
            try:
                float(line[10].strip().replace(",", "."))
                coordX_original = line[10].strip().replace(",", ".")
            except ValueError:
                errorsALinia = True
                errorsLiniaActual.append("Error de conversió a la coordenada x original " + line[10] +  ", columna 11")
                register_error(line_counter, "Error de conversió a la coordenada x original " + line[10] +  ", columna 11", problemes)

        # coord y
        if line[11] is None or line[11].strip().lower() == '':
            errorsALinia = True
            errorsLiniaActual.append("La coordenada y original està en blanc a la columna 12")
            register_error(line_counter, "La coordenada y original està en blanc a la columna 12", problemes)
        else:
            try:
                float(line[11].strip().replace(",", "."))
                coordY_original = line[11].replace(",", ".")
            except ValueError:
                errorsALinia = True
                errorsLiniaActual.append("Error de conversió a la coordenada y original " + line[11] +  ", columna 11")
                register_error(line_counter, "Error de conversió a la coordenada y original " + line[11] +  ", columna 11", problemes)

        # coord z
        if line[12] is None or line[12].strip().lower() == '':
            errorsALinia = True
            errorsLiniaActual.append("La coordenada z original està en blanc a la columna 13")
            register_error(line_counter, "La coordenada z original està en blanc a la columna 13", problemes)
        else:
            try:
                float(line[12].replace(",", "."))
                coordZ_original = line[12].replace(",", ".")
            except ValueError:
                errorsALinia = True
                errorsLiniaActual.append("Error de conversió a la coordenada z original " + line[12] +  ", columna 13")
                register_error(line_counter, "Error de conversió a la coordenada z original " + line[12] +  ", columna 13", problemes)


        # incertesa coordenades h
        if line[13] is not None and not line[13].strip().lower() == '':
            try:
                precisioH = float(line[13].strip().replace(",", "."))
            except ValueError:
                errorsALinia = True
                errorsLiniaActual.append("Error de conversió a incertesa de coordenades " + line[13] +  ", columna 14")
                register_error(line_counter, "Error de conversió a incertesa de coordenades " + line[13] +  ", columna 14", problemes)

        # incertesa coordenades z
        if line[14] is None or line[14].strip().lower() == '':
            precisioZ = None
        else:
            try:
                float(line[14].strip().replace(",", "."))
                precisioZ = line[14]
            except ValueError:
                errorsALinia = True
                errorsLiniaActual.append("Error de conversió a incertesa d'altitud " + line[14] +  ", columna 15")
                register_error(line_counter, "Error de conversió a incertesa d'altitud " + line[14] +  ", columna 15", problemes)

        # georeferenciador versio
        if line[15] is None or line[15].strip().lower() == '':
            errorsALinia = True
            errorsLiniaActual.append("Georeferenciador en blanc a la columna 16")
            register_error(line_counter, "Georeferenciador en blanc a la columna 16", problemes)            
        else:
            georeferenciador = get_georeferencer_by_name(line[15].strip())
            if georeferenciador is None:
                errorsALinia = True
                errorsLiniaActual.append("No trobo el georeferenciador " + line[15] +  ", columna 16")
                register_error(line_counter, "No trobo el georeferenciador " + line[15] +  ", columna 16", problemes)

        if len(line) > 16:
            observacions = line[16]
        else:
            observacions = ''

        if errorsALinia:
            errorsLinia.insert(0, line_counter)
            errorsLinia.append(errorsLiniaActual)
            errors.append(errorsLinia)
        else:
            t = Toponim()
            t.nom = nom
            t.aquatic = aquatic
            t.idtipustoponim = tt
            t.idpais = p
            t.idpare = pare
            t.nom_fitxer_importacio = nomFitxer
            t.linia_fitxer_importacio = line_string

            tv = Toponimversio()
            tv.coordenada_x = coordX_original
            tv.coordenada_y = coordY_original
            tv.coordenada_z = coordZ_original
            tv.datacaptura = data

            tv.nom = nomToponimRecurs;
            tv.numero_versio = numeroVersio
            tv.observacions = observacions
            tv.precisio_z = precisioZ
            tv.iduser = georeferenciador
            if precisioH is not None:
                tv.precisio_h = precisioH
            tv.idqualificador = qv
            tv.idrecursgeoref = rg
            tv.idtoponim = t

            #t.versions.add(tv)

            toponims_to_create.append({ 'toponim': t, 'versio': tv })
    else:
        toponims_exist.append(t)