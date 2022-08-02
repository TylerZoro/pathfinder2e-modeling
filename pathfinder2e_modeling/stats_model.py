"""A modeler for a D&D-like roleplaying game system's statistics"""

import dataclasses
from typing import Tuple, OrderedDict, List


@dataclasses.dataclass
class StatsConversion:
    source_system: str
    target_system: str
    stat_name_in: str
    stat_name_out: str

    @staticmethod
    def variance_scaling(variance):
        """
        The difference in the variance between systems applied.

        For example, if the variance in the target system is 20% higher across the board,
        then this would simply return `variance * 1.2`.

        But that assumes a linear, continuous scaling, which might not always be the case.
        """

        raise RuntimeError("Classes must override StatsConversion.variance_scaling")

    @staticmethod
    def nominal_source_value(level):
        """Return the expected value for the stat in the source system at the given level"""

        raise RuntimeError("Classes must override StatsConversion.nominal_source_value")

    @staticmethod
    def nominal_target_value(level):
        """Return the expected value for the stat in the target system at the given level"""

        raise RuntimeError("Classes must override StatsConversion.nominal_target_value")

    def variance(self, level, source_value):
        """Compute the variance between the source value and the nominal value for the level"""

        nominal = self.nominal_source_value(level)

        return (source_value - nominal) / nominal

    def convert_stat(self, level, source_value):
        """Compute the converted value"""

        estimated_target = self.nominal_target_value(level)
        variance = self.variance(level, source_value)
        variance = self.variance_scaling(variance)
        return estimated_target * (1 + variance)


@dataclasses.dataclass
class StatsModel:
    level: int
    armor_class: int
    hit_points: int
    attack_bonus: int
    damage: str
    average_damage: int
    attributes: OrderedDict[str, Tuple[int, int]]
    saves: OrderedDict[str, int]
    other_details: List[str]
