import pytest
from calculate_average import calculate_average

def test_calculate_average_normal_case():
    """Test with a normal list of numbers"""
    assert calculate_average([10, 20, 30]) == 20.0


def test_calculate_average_empty_list():
    """Test with an empty list"""
    assert calculate_average([]) == 0


def test_calculate_average_single_number():
    """Test with a single number"""
    assert calculate_average([5]) == 5.0


def test_calculate_average_negative_numbers():
    """Test with negative numbers"""
    assert calculate_average([-10, -20, -30]) == -20.0


def test_calculate_average_mixed_numbers():
    """Test with mixed positive and negative numbers"""
    assert calculate_average([10, -5, 15, -10]) == 2.5


def test_calculate_average_floats():
    """Test with floating point numbers"""
    assert calculate_average([1.5, 2.5, 3.5]) == pytest.approx(2.5)


def test_calculate_average_zeros():
    """Test with zeros"""
    assert calculate_average([0, 0, 0]) == 0.0


def test_calculate_average_large_numbers():
    """Test with large numbers"""
    assert calculate_average([1000000, 2000000, 3000000]) == pytest.approx(2000000.0)