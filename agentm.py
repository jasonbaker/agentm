__version__ = '0.1.0'

class ValidationFailedError(Exception):
    pass

def WritableValue(name, validator=None):
    """ A value in the dictionary that has been exposed as both readable and
    writable.

    :param name: The key of the dictionary to be exposed.  

    :param validator: If given, a function that will return True if the value is valid.  If this
        function returns false, a :class:`~ValidationFailedError` will be raised.
    """

    def _get_prop(self):
        return self[name]
    
    if validator:
        def _set_prop(self, value):
            if not validator(value):
                raise ValidationFailedError
            self[name] = value
    else:
        def _set_prop(self, value):
            self[name] = value

    return property(fget=_get_prop, fset=_set_prop)

def ReadonlyValue(name):
    """
    A value that is exposed as read only.

    :param name:  The key of the dictionary to be exposed.
    """
    def _get_prop(self):
        return self[name]

    return property(fget=_get_prop)

def Reference(name, cls):
    def _get_prop(self):
        if not isinstance(self[name], cls):
            self[name] = cls(self[name])
        return self[name]

    def _set_prop(self, value):
        if not isinstance(value, cls):
            value = cls(value)
        self[name] = value

    return property(fget=_get_prop, fset=_set_prop)

def ReferenceList(name, cls):
    """
    A list of references.  This will convert each element of the list to cls if
    it is not already.
    """
    def _get_prop(self):
        # Could be a performance issue since we're regenerating the list every
        # time the property is accessed.
        self[name] = [cls(val) for val in self[name]]
        return self[name]

    def _set_prop(self, values):
        self[name] = [cls(val) for val in values]

    return property(fget=_get_prop, fset=_set_prop)
        

class Document(dict):
    id = ReadonlyValue('_id')
    def __new__(cls, *args, **kwargs):
        instance = dict.__new__(cls, *args, **kwargs)
        collection = getattr(cls, 'collection', None)
        if collection and not instance.get('_ns', None):
            instance['_ns'] = collection
        elif instance.get('_ns', None):
            instance.collection = instance['_ns']
        return instance


