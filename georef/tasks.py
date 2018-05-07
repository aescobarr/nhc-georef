import uuid

def append_string_to_toponim(toponim, current_elements):
    if toponim.idpare:
        current_elements.append(toponim.idpare.id + '$' + toponim.idpare.nom)
        append_string_to_toponim(toponim.idpare, current_elements)
    else:
        pass


def compute_denormalized_toponim_tree_val(toponim):
    stack = []
    append_string_to_toponim(toponim, stack)
    denormalized_val = '#'.join(list(reversed(stack)))
    return denormalized_val


def format_denormalized_toponimtree(denormalized_toponimtree_str):
    stack = []
    stack = denormalized_toponimtree_str.split('#')
    return stack



def compute_denormalized_toponim_tree_val_to_root(toponim, stack):
    stack.append(toponim.id + '$' + toponim.nom)
    if(toponim.idpare):
        compute_denormalized_toponim_tree_val_to_root(toponim.idpare,stack)
    else:
        stack.append('1$Mon')
    denormalized_val = '#'.join(list(reversed(stack)))
    return denormalized_val

def pkgen():
    return str(uuid.uuid4())