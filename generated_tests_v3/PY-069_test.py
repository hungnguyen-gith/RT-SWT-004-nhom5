from functions.PY_069 import apply_axis_properties
import pytest

class StubAxis:
    def __init__(self):
        self.major_ticks = []
        self.minor_ticks = []

    def get_majorticklabels(self):
        return self.major_ticks

    def get_minorticklabels(self):
        return self.minor_ticks

class StubLabel:
    def __init__(self):
        self.rotation = None
        self.fontsize = None

    def set_rotation(self, rot):
        self.rotation = rot

    def set_fontsize(self, fontsize):
        self.fontsize = fontsize

def test_apply_axis_properties_rotation_and_fontsize():
    axis = StubAxis()
    label1 = StubLabel()
    label2 = StubLabel()
    axis.major_ticks = [label1]
    axis.minor_ticks = [label2]

    apply_axis_properties(None, axis, rot=45, fontsize=12)

    assert label1.rotation == 45
    assert label1.fontsize == 12
    assert label2.rotation == 45
    assert label2.fontsize == 12

def test_apply_axis_properties_only_rotation():
    axis = StubAxis()
    label1 = StubLabel()
    label2 = StubLabel()
    axis.major_ticks = [label1]
    axis.minor_ticks = [label2]

    apply_axis_properties(None, axis, rot=90)

    assert label1.rotation == 90
    assert label1.fontsize is None
    assert label2.rotation == 90
    assert label2.fontsize is None

def test_apply_axis_properties_only_fontsize():
    axis = StubAxis()
    label1 = StubLabel()
    label2 = StubLabel()
    axis.major_ticks = [label1]
    axis.minor_ticks = [label2]

    apply_axis_properties(None, axis, fontsize=14)

    assert label1.rotation is None
    assert label1.fontsize == 14
    assert label2.rotation is None
    assert label2.fontsize == 14

def test_apply_axis_properties_no_changes():
    axis = StubAxis()
    label1 = StubLabel()
    label2 = StubLabel()
    axis.major_ticks = [label1]
    axis.minor_ticks = [label2]

    apply_axis_properties(None, axis)

    assert label1.rotation is None
    assert label1.fontsize is None
    assert label2.rotation is None
    assert label2.fontsize is None

def test_apply_axis_properties_empty_labels():
    axis = StubAxis()
    axis.major_ticks = []
    axis.minor_ticks = []

    apply_axis_properties(None, axis, rot=30, fontsize=10)

    # No labels to change, so nothing should be set
    assert True  # Just to ensure the test runs without errors

def test_apply_axis_properties_zero_rotation():
    axis = StubAxis()
    label1 = StubLabel()
    label2 = StubLabel()
    axis.major_ticks = [label1]
    axis.minor_ticks = [label2]

    apply_axis_properties(None, axis, rot=0)

    assert label1.rotation == 0
    assert label2.rotation == 0

def test_apply_axis_properties_negative_rotation():
    axis = StubAxis()
    label1 = StubLabel()
    label2 = StubLabel()
    axis.major_ticks = [label1]
    axis.minor_ticks = [label2]

    apply_axis_properties(None, axis, rot=-45)

    assert label1.rotation == -45
    assert label2.rotation == -45

def test_apply_axis_properties_large_fontsize():
    axis = StubAxis()
    label1 = StubLabel()
    label2 = StubLabel()
    axis.major_ticks = [label1]
    axis.minor_ticks = [label2]

    apply_axis_properties(None, axis, fontsize=100)

    assert label1.fontsize == 100
    assert label2.fontsize == 100

def test_apply_axis_properties_small_fontsize():
    axis = StubAxis()
    label1 = StubLabel()
    label2 = StubLabel()
    axis.major_ticks = [label1]
    axis.minor_ticks = [label2]

    apply_axis_properties(None, axis, fontsize=0)

    assert label1.fontsize == 0
    assert label2.fontsize == 0