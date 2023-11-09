from .e_docip import E_Docip


_ALL_CLASSES = [
    cla
    for name, cla in globals().items()
    if name.startswith('E_')
]
