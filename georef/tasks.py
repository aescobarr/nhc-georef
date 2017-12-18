from georef.models import Toponim


def append_string_to_toponim(toponim, current_elements):
    if toponim.idpare:
        current_elements.append(toponim.idpare.id + '$' + toponim.idpare.nom)
        append_string_to_toponim(toponim.idpare, current_elements)
    else:
        pass


def update_denormalized_toponim_tree():
    for toponim in Toponim.objects.all():
        stack = []
        append_string_to_toponim(toponim,stack)
        denormalized_val = '#'.join(list(reversed(stack)))
        if denormalized_val != toponim.denormalized_toponimtree:
            toponim.denormalized_toponimtree = denormalized_val
            toponim.save()