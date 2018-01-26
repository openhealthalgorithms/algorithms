from OHA.Defaults import Defaults
from OHA.helpers.converters.LengthConverter import LengthConverter

__author__ = 'indrajit'
__email__ = 'eendroroy@gmail.com'


class HeightConverter(LengthConverter):
    def _default_from_unit(self):
        return Defaults.height_unit

    def _default_to_unit(self):
        return Defaults.height_unit
