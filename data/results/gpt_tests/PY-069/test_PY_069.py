import pytest
from unittest.mock import MagicMock

def test_apply_axis_properties_rotation():
    axis = MagicMock()
    axis.get_majorticklabels.return_value = [MagicMock(), MagicMock()]
    axis.get_minorticklabels.return_value = [MagicMock()]

    apply_axis_properties(axis, rot=45)

    for label in axis.get_majorticklabels() + axis.get_minorticklabels():
        label.set_rotation.assert_called_with(45)

def test_apply_axis_properties_fontsize():
    axis = MagicMock()
    axis.get_majorticklabels.return_value = [MagicMock(), MagicMock()]
    axis.get_minorticklabels.return_value = [MagicMock()]

    apply_axis_properties(axis, fontsize=12)

    for label in axis.get_majorticklabels() + axis.get_minorticklabels():
        label.set_fontsize.assert_called_with(12)

def test_apply_axis_properties_rotation_and_fontsize():
    axis = MagicMock()
    axis.get_majorticklabels.return_value = [MagicMock(), MagicMock()]
    axis.get_minorticklabels.return_value = [MagicMock()]

    apply_axis_properties(axis, rot=90, fontsize=10)

    for label in axis.get_majorticklabels() + axis.get_minorticklabels():
        label.set_rotation.assert_called_with(90)
        label.set_fontsize.assert_called_with(10)

def test_apply_axis_properties_no_changes():
    axis = MagicMock()
    axis.get_majorticklabels.return_value = [MagicMock(), MagicMock()]
    axis.get_minorticklabels.return_value = [MagicMock()]

    apply_axis_properties(axis)

    for label in axis.get_majorticklabels() + axis.get_minorticklabels():
        label.set_rotation.assert_not_called()
        label.set_fontsize.assert_not_called()

def test_apply_axis_properties_zero_rotation():
    axis = MagicMock()
    axis.get_majorticklabels.return_value = [MagicMock(), MagicMock()]
    axis.get_minorticklabels.return_value = [MagicMock()]

    apply_axis_properties(axis, rot=0)

    for label in axis.get_majorticklabels() + axis.get_minorticklabels():
        label.set_rotation.assert_called_with(0)

def test_apply_axis_properties_large_fontsize():
    axis = MagicMock()
    axis.get_majorticklabels.return_value = [MagicMock(), MagicMock()]
    axis.get_minorticklabels.return_value = [MagicMock()]

    apply_axis_properties(axis, fontsize=100)

    for label in axis.get_majorticklabels() + axis.get_minorticklabels():
        label.set_fontsize.assert_called_with(100)

def test_apply_axis_properties_negative_rotation():
    axis = MagicMock()
    axis.get_majorticklabels.return_value = [MagicMock(), MagicMock()]
    axis.get_minorticklabels.return_value = [MagicMock()]

    apply_axis_properties(axis, rot=-45)

    for label in axis.get_majorticklabels() + axis.get_minorticklabels():
        label.set_rotation.assert_called_with(-45)