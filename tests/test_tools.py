"""
Comprehensive test suite for proportion calculation tools.
Tests all functions with various inputs, edge cases, and error conditions.
"""

import pytest
from proportion_server import (
    percent_of, solve_proportion, scale_by_ratio, 
    direct_k, resize_dimensions
)


class TestPercentOf:
    """Test the percent_of function."""
    
    def test_basic_percentage(self):
        """Test basic percentage calculations."""
        assert percent_of(25, 100) == 25.0
        assert percent_of(1, 4) == 25.0
        assert percent_of(3, 4) == 75.0
        
    def test_zero_part(self):
        """Test with zero part."""
        assert percent_of(0, 100) == 0.0
        assert percent_of(0, 1) == 0.0
        
    def test_negative_values(self):
        """Test with negative values."""
        assert percent_of(-25, 100) == -25.0
        assert percent_of(25, -100) == -25.0
        assert percent_of(-25, -100) == 25.0
        
    def test_decimal_precision(self):
        """Test decimal precision in calculations."""
        result = percent_of(1, 3)
        assert abs(result - 33.333333333333336) < 1e-10
        
    def test_large_numbers(self):
        """Test with large numbers."""
        assert percent_of(1000000, 4000000) == 25.0
        
    def test_very_small_numbers(self):
        """Test with very small numbers."""
        result = percent_of(1e-10, 1e-8)
        assert abs(result - 1.0) < 1e-10
        
    def test_zero_whole_error(self):
        """Test assertion error when whole is zero."""
        with pytest.raises(AssertionError, match="Division by zero: whole cannot be zero"):
            percent_of(10, 0)
            
    def test_negative_whole_edge_cases(self):
        """Test edge cases with negative whole values."""
        assert percent_of(10, -5) == -200.0
        assert percent_of(-10, -5) == 200.0


class TestSolveProportion:
    """Test the solve_proportion function."""
    
    def test_solve_a(self):
        """Test solving for 'a' in proportion a/b = c/d."""
        result = solve_proportion(None, 4, 6, 8)
        assert result == 3.0
        
    def test_solve_b(self):
        """Test solving for 'b' in proportion a/b = c/d."""
        result = solve_proportion(3, None, 6, 8)
        assert result == 4.0
        
    def test_solve_c(self):
        """Test solving for 'c' in proportion a/b = c/d."""
        result = solve_proportion(3, 4, None, 8)
        assert result == 6.0
        
    def test_solve_d(self):
        """Test solving for 'd' in proportion a/b = c/d."""
        result = solve_proportion(3, 4, 6, None)
        assert result == 8.0
        
    def test_negative_values(self):
        """Test with negative values."""
        result = solve_proportion(-3, 4, 6, None)
        assert result == -8.0
        
    def test_decimal_results(self):
        """Test with decimal results."""
        result = solve_proportion(1, 3, 2, None)
        assert abs(result - 6.0) < 1e-10
        
    def test_multiple_none_error(self):
        """Test assertion error when multiple values are None."""
        with pytest.raises(AssertionError, match="Exactly one value must be None"):
            solve_proportion(None, None, 6, 8)
        
        with pytest.raises(AssertionError, match="Exactly one value must be None"):
            solve_proportion(None, 4, None, 8)
        
        with pytest.raises(AssertionError, match="Exactly one value must be None"):
            solve_proportion(None, None, None, None)
    
    def test_no_none_error(self):
        """Test assertion error when no values are None."""
        with pytest.raises(AssertionError, match="Exactly one value must be None"):
            solve_proportion(3, 4, 6, 8)
    
    def test_zero_denominator_error(self):
        """Test assertion error when denominators are zero."""
        with pytest.raises(AssertionError, match="Division by zero: denominator"):
            solve_proportion(None, 2, 3, 0)  # Solving for a, divides by d=0
        
        with pytest.raises(AssertionError, match="Division by zero: denominator"):
            solve_proportion(2, None, 0, 3)  # Solving for b, divides by c=0
    
    def test_division_by_zero_calculation(self):
        """Test assertion error for division by zero during calculation."""
        with pytest.raises(AssertionError, match="Division by zero: denominator"):
            # This would require dividing by zero in calculation
            solve_proportion(None, 4, 0, 0)
    
    def test_large_numbers(self):
        """Test with large numbers."""
        result = solve_proportion(1000000, 2000000, 500000, None)
        assert result == 1000000.0
        
    def test_very_small_numbers(self):
        """Test with very small numbers."""
        result = solve_proportion(1e-10, 2e-10, 5e-11, None)
        assert abs(result - 1e-10) < 1e-20


class TestScaleByRatio:
    """Test the scale_by_ratio function."""
    
    def test_positive_scaling(self):
        """Test scaling with positive ratios."""
        assert scale_by_ratio(10, 2.5) == 25.0
        assert scale_by_ratio(100, 0.5) == 50.0
        
    def test_negative_values(self):
        """Test scaling with negative values."""
        assert scale_by_ratio(-10, 2.0) == -20.0
        assert scale_by_ratio(10, -2.0) == -20.0
        assert scale_by_ratio(-10, -2.0) == 20.0
        
    def test_zero_scaling(self):
        """Test scaling with zero ratio."""
        assert scale_by_ratio(100, 0) == 0.0
        
    def test_zero_value(self):
        """Test scaling zero value."""
        assert scale_by_ratio(0, 5.0) == 0.0
        
    def test_identity_scaling(self):
        """Test scaling with ratio of 1."""
        assert scale_by_ratio(42, 1.0) == 42.0
        
    def test_fractional_scaling(self):
        """Test scaling with fractional ratios."""
        assert scale_by_ratio(9, 1/3) == 3.0
        
    def test_large_numbers(self):
        """Test scaling with large numbers."""
        result = scale_by_ratio(1e6, 1e-3)
        assert result == 1000.0
        
    def test_very_small_numbers(self):
        """Test scaling with very small numbers."""
        result = scale_by_ratio(1e-10, 1e10)
        assert result == 1.0
        
    def test_precision_edge_cases(self):
        """Test precision with edge cases."""
        result = scale_by_ratio(1/3, 3)
        assert abs(result - 1.0) < 1e-15


class TestDirectK:
    """Test the direct_k function."""
    
    def test_positive_values(self):
        """Test with positive values."""
        assert direct_k(5, 15) == 3.0
        assert direct_k(2, 10) == 5.0
        
    def test_negative_values(self):
        """Test with negative values."""
        assert direct_k(-4, 12) == -3.0
        assert direct_k(4, -12) == -3.0
        assert direct_k(-4, -12) == 3.0
        
    def test_zero_y(self):
        """Test with zero y value."""
        assert direct_k(5, 0) == 0.0
        
    def test_zero_x_error(self):
        """Test assertion error when x is zero."""
        with pytest.raises(AssertionError, match="Division by zero: x cannot be zero"):
            direct_k(0, 10)
            
    def test_decimal_precision(self):
        """Test decimal precision."""
        result = direct_k(3, 1)
        assert abs(result - 0.3333333333333333) < 1e-15
        
    def test_large_numbers(self):
        """Test with large numbers."""
        assert direct_k(1e6, 2e6) == 2.0
        
    def test_very_small_numbers(self):
        """Test with very small numbers."""
        result = direct_k(1e-10, 5e-10)
        assert abs(result - 5.0) < 1e-10
        
    def test_fractional_results(self):
        """Test fractional results."""
        result = direct_k(7, 2)
        assert abs(result - 2/7) < 1e-15


class TestResizeDimensions:
    """Test the resize_dimensions function."""
    
    def test_uniform_scaling(self):
        """Test uniform scaling of dimensions."""
        result = resize_dimensions(100, 50, 2.0)
        assert result == (200.0, 100.0)
        
    def test_zero_dimensions(self):
        """Test with zero dimensions."""
        result = resize_dimensions(0, 0, 3.0)
        assert result == (0.0, 0.0)
        
        result = resize_dimensions(100, 0, 2.0)
        assert result == (200.0, 0.0)
        
    def test_identity_scaling(self):
        """Test scaling with factor of 1."""
        result = resize_dimensions(100, 50, 1.0)
        assert result == (100.0, 50.0)
        
    def test_large_scaling(self):
        """Test with large scale factors."""
        result = resize_dimensions(10, 20, 100.0)
        assert result == (1000.0, 2000.0)
        
    def test_small_scaling(self):
        """Test with small scale factors."""
        result = resize_dimensions(100, 200, 0.1)
        assert result == (10.0, 20.0)
        
    def test_decimal_dimensions(self):
        """Test with decimal dimensions."""
        result = resize_dimensions(10.5, 20.7, 2.0)
        assert result == (21.0, 41.4)
    
    def test_negative_dimensions_error(self):
        """Test assertion error with negative dimensions."""
        with pytest.raises(AssertionError, match="Width must be non-negative"):
            resize_dimensions(-100, 50, 2.0)
        
        with pytest.raises(AssertionError, match="Height must be non-negative"):
            resize_dimensions(100, -50, 2.0)
        
        with pytest.raises(AssertionError, match="Width must be non-negative"):
            resize_dimensions(-100, -50, 2.0)
    
    def test_zero_scale_error(self):
        """Test assertion error with zero scale factor."""
        with pytest.raises(AssertionError, match="Scale factor must be positive"):
            resize_dimensions(100, 50, 0)
    
    def test_negative_scale_error(self):
        """Test assertion error with negative scale factor."""
        with pytest.raises(AssertionError, match="Scale factor must be positive"):
            resize_dimensions(100, 50, -1.5)
        
        with pytest.raises(AssertionError, match="Scale factor must be positive"):
            resize_dimensions(100, 50, -0.1)
    
    def test_very_large_dimensions(self):
        """Test with very large dimensions."""
        result = resize_dimensions(1e6, 1e7, 0.001)
        assert result == (1000.0, 10000.0)
        
    def test_precision_edge_cases(self):
        """Test precision edge cases."""
        result = resize_dimensions(1/3, 2/3, 3.0)
        expected_width = (1/3) * 3.0
        expected_height = (2/3) * 3.0
        assert abs(result[0] - expected_width) < 1e-15
        assert abs(result[1] - expected_height) < 1e-15


class TestIntegration:
    """Integration tests combining multiple functions."""
    
    def test_chained_calculations(self):
        """Test chaining multiple calculations."""
        # Start with a percentage
        percent = percent_of(25, 100)  # 25%
        
        # Use result in proportion
        result = solve_proportion(percent, 100, None, 200)  # 25/100 = x/200
        assert result == 50.0
        
    def test_proportion_verification(self):
        """Test proportion verification using cross multiplication."""
        a, b, c = 3, 4, 6
        d = solve_proportion(a, b, c, None)
        
        # Verify: a/b should equal c/d
        ratio1 = a / b
        ratio2 = c / d
        assert abs(ratio1 - ratio2) < 1e-15
        
    def test_resize_and_scale_workflow(self):
        """Test resizing and scaling workflow."""
        # Original dimensions
        width, height = 100, 50
        
        # Resize by factor of 2
        new_width, new_height = resize_dimensions(width, height, 2.0)
        assert new_width == 200.0
        assert new_height == 100.0
        
        # Scale the area by ratio
        original_area = width * height
        new_area = new_width * new_height
        area_ratio = new_area / original_area
        assert area_ratio == 4.0  # 2^2 = 4
        
    def test_percentage_and_proportion_workflow(self):
        """Test workflow combining percentages and proportions."""
        # What percentage is 15 of 60?
        percent = percent_of(15, 60)  # 25%
        
        # If 25% of some number is 30, what's the number?
        result = solve_proportion(percent, 100, 30, None)
        assert result == 120.0
        
    def test_scaling_chain(self):
        """Test chain of scaling operations."""
        value = 100
        
        # Scale by 1.5
        value = scale_by_ratio(value, 1.5)  # 150
        
        # Scale by 2/3
        value = scale_by_ratio(value, 2/3)  # 100
        
        # Should be back to original
        assert abs(value - 100.0) < 1e-15
        
    def test_real_world_recipe_scaling(self):
        """Test real-world recipe scaling scenario."""
        # Original recipe serves 4, we want to serve 6
        # Original calls for 2 cups flour
        original_servings = 4
        new_servings = 6
        original_flour = 2
        
        # Find scaling ratio
        ratio = new_servings / original_servings  # 1.5
        
        # Scale flour amount
        new_flour = scale_by_ratio(original_flour, ratio)
        assert new_flour == 3.0
        
        # Verify using proportion
        flour_check = solve_proportion(original_flour, original_servings, None, new_servings)
        assert flour_check == 3.0
        
    def test_financial_calculation_workflow(self):
        """Test financial calculation workflow."""
        # Investment grows from $1000 to $1250
        initial = 1000
        final = 1250
        
        # What's the growth percentage?
        growth_amount = final - initial  # 250
        growth_percent = percent_of(growth_amount, initial)  # 25%
        
        # Find the growth factor
        growth_factor = direct_k(initial, final)  # 1.25
        
        # Verify by scaling
        verification = scale_by_ratio(initial, growth_factor)
        assert verification == final


class TestErrorHandling:
    """Test error handling and edge cases."""
    
    def test_type_validation_errors(self):
        """Test that functions handle type validation properly."""
        # These should work with int inputs (converted to float)
        assert percent_of(1, 4) == 25.0
        assert solve_proportion(1, 2, 3, None) == 6.0
        assert scale_by_ratio(10, 2) == 20.0
        assert direct_k(2, 6) == 3.0
        assert resize_dimensions(10, 20, 2) == (20.0, 40.0)
    
    def test_boundary_conditions(self):
        """Test mathematical boundary conditions."""
        # Actual zero denominators should raise error
        with pytest.raises(AssertionError):
            percent_of(10, 0)
        
        # Very small but non-zero numbers should work
        result = percent_of(10, 1e-100)
        assert result == 1e103
        
        # Large numbers should work
        result = percent_of(1e50, 1e60)
        assert abs(result - 1e-8) < 1e-15
    
    def test_floating_point_precision_limits(self):
        """Test floating point precision limits."""
        # Very small numbers
        result = scale_by_ratio(1e-300, 1e-300)
        # Should not raise error, might be 0.0 due to underflow
        assert isinstance(result, float)
        
        # Very large numbers
        result = scale_by_ratio(1e100, 1e100)
        # Should not raise error, might be inf due to overflow
        assert isinstance(result, float)