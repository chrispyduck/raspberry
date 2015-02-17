import imp

def getClassInstanceFromName(dotted_name):
    typ = import_from_dotted_path(dotted_name)
    return typ()

def import_from_dotted_path(dotted_names, path=None):
    """ import_from_dotted_path('foo.bar') -> from foo import bar; return bar """
    next_module, remaining_names = dotted_names.split('.', 1)
    fp, pathname, description = imp.find_module(next_module, path)
    module = imp.load_module(next_module, fp, pathname, description)
    if hasattr(module, remaining_names):
        return getattr(module, remaining_names)
    if '.' not in remaining_names:
        return module
    return import_from_dotted_path(remaining_names, path=module.__path__)

def todict(obj, classkey=None):
    if isinstance(obj, dict):
        data = {}
        for (k, v) in obj.items():
            data[k] = todict(v, classkey)
        return data
    elif isinstance(obj, str):
        return obj
    elif hasattr(obj, "_ast"):
        return todict(obj._ast())
    elif hasattr(obj, "__iter__"):
        return [todict(v, classkey) for v in obj]
    elif hasattr(obj, "__dict__"):
        data = {}
        for (k, v) in obj.__dict__.items():
            if not callable(obj.__dict__[k]) and not k.startswith('_'):
                data[k] = todict(v, classkey)
        if classkey is not None and hasattr(obj, "__class__"):
            data[classkey] = obj.__class__.__name__
        return data
    else:
        return obj