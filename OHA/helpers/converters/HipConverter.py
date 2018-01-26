from OHA.Defaults import Defaults
from OHA.helpers.converters.HeightConverter import LengthConverter


class HipConverter(LengthConverter):
    def _default_from_unit(self):
        return Defaults.hip_unit

    def _default_to_unit(self):
        return Defaults.hip_unit
