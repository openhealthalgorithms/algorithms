from OHA.Defaults import Defaults
from OHA.helpers.converters.HeightConverter import LengthConverter


class WaistConverter(LengthConverter):
    def _default_from_unit(self):
        return Defaults.waist_unit

    def _default_to_unit(self):
        return Defaults.waist_unit
