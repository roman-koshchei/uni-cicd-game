import pytest
import math
from movement.vector import Vector2

def test_vector_initialization():
    """Test Vector2 initialization with and without parameters"""
    # Test default initialization
    v1 = Vector2()
    assert v1.x == 0 and v1.y == 0
    
    # Test custom initialization
    v2 = Vector2(5, 10)
    assert v2.x == 5 and v2.y == 10

def test_vector_addition():
    """Test vector addition operation"""
    v1 = Vector2(5, 10)
    v2 = Vector2(2, 3)
    result = v1 + v2
    assert result.x == 7 and result.y == 13

def test_vector_subtraction():
    """Test vector subtraction operation"""
    v1 = Vector2(5, 10)
    v2 = Vector2(2, 3)
    result = v1 - v2
    assert result.x == 3 and result.y == 7

def test_vector_negation():
    """Test vector negation operation"""
    v = Vector2(5, 10)
    result = -v
    assert result.x == -5 and result.y == -10

def test_vector_scalar_multiplication():
    """Test vector multiplication by scalar"""
    v = Vector2(5, 10)
    result = v * 2
    assert result.x == 10 and result.y == 20

def test_vector_division():
    """Test vector division by scalar"""
    v = Vector2(10, 20)
    result = v / 2
    assert result.x == 5 and result.y == 10
    
    # Test division by zero
    result = v / 0
    assert result is None

def test_vector_equality():
    """Test vector equality comparison"""
    v1 = Vector2(5, 10)
    v2 = Vector2(5, 10)
    v3 = Vector2(5.0000001, 10)
    v4 = Vector2(6, 10)
    
    assert v1 == v2
    assert v1 == v3  # Should be equal within threshold
    assert v1 != v4

def test_vector_magnitude():
    """Test vector magnitude calculations"""
    v = Vector2(3, 4)
    assert v.magnitudeSquared() == 25
    assert v.magnitude() == 5.0
    
    # Test with different values
    v = Vector2(1, 1)
    assert v.magnitudeSquared() == 2
    assert math.isclose(v.magnitude(), math.sqrt(2))

def test_vector_copy():
    """Test vector copy method"""
    v1 = Vector2(5, 10)
    v2 = v1.copy()
    
    # Check equality but different objects
    assert v1 == v2
    assert v1 is not v2
    
    # Modify v2 and check v1 is unchanged
    v2.x = 7
    assert v1.x == 5
    assert v2.x == 7

def test_vector_as_tuple_and_int():
    """Test vector conversion methods"""
    v = Vector2(5.7, 10.2)
    assert v.asTuple() == (5.7, 10.2)
    assert v.asInt() == (5, 10)

def test_vector_string_representation():
    """Test string representation of vector"""
    v = Vector2(5, 10)
    assert str(v) == "<5, 10>" 