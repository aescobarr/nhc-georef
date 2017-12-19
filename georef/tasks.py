from georef.models import Toponim
from georef.models import compute_denormalized_toponim_tree_val


def update_all_denormalized_toponim_tree():
    for toponim in Toponim.objects.all():
        denormalized_val = compute_denormalized_toponim_tree_val(toponim)
        if denormalized_val != toponim.denormalized_toponimtree:
            toponim.denormalized_toponimtree = denormalized_val
            toponim.save()