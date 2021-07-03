Property = 0


class NumericProperty(Property):
    """
    NumericProperty(defaultvalue=0, **kw)
    Property that represents a numeric value.

        :Parameters:
            `defaultvalue`: int or float, defaults to 0
                Specifies the default value of the property.

        >>> wid = Widget()
        >>> wid.x = 42
        >>> print(wid.x)
        42
        >>> wid.x = "plop"
         Traceback (most recent call last):
           File "<stdin>", line 1, in <module>
           File "properties.pyx", line 93, in kivy.properties.Property.__set__
           File "properties.pyx", line 111, in kivy.properties.Property.set
           File "properties.pyx", line 159, in kivy.properties.NumericProperty.check
         ValueError: NumericProperty accept only int/float

        .. versionchanged:: 1.4.1
            NumericProperty can now accept custom text and tuple value to indicate a
            type, like "in", "pt", "px", "cm", "mm", in the format: '10pt' or (10,
            'pt').
    """

    def get_format(self, EventDispatcher_obj):  # real signature unknown; restored from __doc__
        """
        NumericProperty.get_format(self, EventDispatcher obj)

                Return the format used for Numeric calculation. Default is px (mean
                the value have not been changed at all). Otherwise, it can be one of
                'in', 'pt', 'cm', 'mm'.
        """
        pass

    def __init__(self, defaultvalue=0, **kw):  # real signature unknown; restored from __doc__
        pass

    @staticmethod  # known case of __new__
    def __new__(*args, **kwargs):  # real signature unknown
        """ Create and return a new object.  See help(type) for accurate signature. """
        pass

    def __reduce__(self, *args, **kwargs):  # real signature unknown
        """ NumericProperty.__reduce_cython__(self) """
        pass

    def __setstate__(self, *args, **kwargs):  # real signature unknown
        """ NumericProperty.__setstate_cython__(self, __pyx_state) """
        pass

    __pyx_vtable__ = None  # (!) real value is '<capsule object NULL at 0x0000016B0938EB10>'
