import dataclasses

import pytest

from pathfinder2e_modeling.stats_model import StatsConversion


def test_stats_conversion_instance():
    """Test the StatsConversion class constructor"""

    converter = StatsConversion(source_system="2e", target_system="5e", stat_name_in="Str", stat_name_out="Str")

    assert converter.__class__ == StatsConversion, "Expect instance to be of type StatsConversion"


def _passthrough_parameterization(inputs, expected):
    """Return test parameterization for passthrough operations (input = level, output = level)"""
    return (
        lambda value: value, lambda value: value, lambda value: value,
        inputs, expected
    )


def _doubling_parameterization(inputs, expected):
    """Return test parameterization for doubling operations (input = level, output = level * 2"""
    return (
        lambda value: value, lambda value: value, lambda value: value * 2,
        inputs, expected
    )


@pytest.mark.parametrize(
    "variance_scaling_func, nominal_source_func, nominal_target_func, inputs, expected",
    (
            _passthrough_parameterization((1, 1), 1),
            _passthrough_parameterization((4, 6), 6),
            _doubling_parameterization((1, 1), 2),
            _doubling_parameterization((4, 6), 12),
    )
)
def test_stats_conversion_execute(variance_scaling_func, nominal_source_func, nominal_target_func, inputs, expected):
    """Run some conversions"""

    @dataclasses.dataclass
    class XConverter(StatsConversion):
        """A class declared to convert a test stat"""

        source_system: str = "a"
        target_system: str = "b"
        stat_name_in: str = "stat"
        stat_name_out: str = "stat"

        @staticmethod
        def variance_scaling(variance):
            """Variance Scaling"""
            return variance_scaling_func(variance)

        @staticmethod
        def nominal_source_value(level):
            """Source value estimation"""
            return nominal_source_func(level)

        @staticmethod
        def nominal_target_value(level):
            """Target value estimation"""
            return nominal_target_func(level)

    converter = XConverter()

    assert converter.stat_name_in == "stat", "Expect default value for stat_name_in"
    assert converter.stat_name_out == "stat", "Expect default value for stat_name_out"
    assert converter.source_system == "a", "Expect default value for source_system"
    assert converter.target_system == "b", "Expect default value for target_system"

    value = converter.convert_stat(*inputs)

    assert value == expected, f"Expect conversion from {inputs!r} to give {expected}"
