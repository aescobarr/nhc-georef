from georef.models import Toponim


###
# It works like this: for a given toponim, extract its id and put it in a set called "found"
# let theoretical_idpare be the id of another toponim
# The function checks if making theoretical_idpare the parent of the toponim creates a cyclic path like:
# toponim_ini parent -> theoretical_idpare parent -> toponim_n parent .... -> toponim_ini
###
def check_if_cyclic(theoretical_idpare, found=None):
    current_toponim_id = theoretical_idpare
    if theoretical_idpare in found:
        raise Exception
    else:
        found.add(current_toponim_id)
        current_pare = Toponim.objects.get(pk=current_toponim_id)
        if current_pare is not None and current_pare.idpare is not None:
            current_pare_id = current_pare.idpare.id
            check_if_cyclic(current_pare_id, found)