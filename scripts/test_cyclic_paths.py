import os, sys

proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoref.settings")
sys.path.append(proj_path)

os.chdir(proj_path)

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

from georef.models import Toponim


id_illes_balears = 'furibe1596469293583000154'
id_palma = '544552524553545245303730343050616C6D61206465204D616C6C6F72636131302F31312F32303036'
id_espanya = 'furibe159512327682189780'
#"furibe1596469293583000154";"Illes Balears"
#"544552524553545245303730343050616C6D61206465204D616C6C6F72636131302F31312F32303036";"Palma"
#"furibe159512327682189780";"Espanya"


def check_if_cyclic(theoretical_idpare, found=None):
    current_toponim_id = theoretical_idpare
    if theoretical_idpare in found:
        raise Exception
    else:
        found.add(current_toponim_id)
        current_pare = Toponim.objects.get(pk=current_toponim_id)
        if current_pare is not None and current_pare.idpare is not None:
            current_pare_id = current_pare.idpare.id
            check_if_cyclic(current_pare_id, current_toponim_id, found)


def test():
    illes_balears = Toponim.objects.get(pk=id_illes_balears)
    found = set()
    found.add(illes_balears.id)
    check_if_cyclic(id_palma, found)
    #check_if_cyclic(id_espanya, id_illes_balears, found)

test()