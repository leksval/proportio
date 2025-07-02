"""
Pydantic models for proportion calculation inputs and outputs.
Provides robust validation and clear error messages.
"""

from typing import Optional
from pydantic import BaseModel, Field, model_validator


class PercentOfInput(BaseModel):
    """Input for calculating what percentage part is of whole."""
    
    part: float = Field(description="The part value")
    whole: float = Field(description="The whole value (must not be zero)")
    


class PercentOfOutput(BaseModel):
    """Output for percentage calculation."""
    
    percentage: float = Field(description="The calculated percentage")


class ProportionInput(BaseModel):
    """Input for solving proportion a/b = c/d with exactly one missing value."""
    
    a: Optional[float] = Field(None, description="First numerator")
    b: Optional[float] = Field(None, description="First denominator")  
    c: Optional[float] = Field(None, description="Second numerator")
    d: Optional[float] = Field(None, description="Second denominator")
    
    @model_validator(mode='after')
    def validate_exactly_one_none(self) -> 'ProportionInput':
        """Ensure exactly one value is None (missing)."""
        values = [self.a, self.b, self.c, self.d]
        none_count = sum(1 for v in values if v is None)
        
        assert none_count == 1, "Exactly one value must be None (missing) to solve proportion"
        
        return self


class ProportionOutput(BaseModel):
    """Output for proportion calculation."""
    
    missing: float = Field(description="The calculated missing value")


class ScaleByRatioInput(BaseModel):
    """Input for scaling a value by a ratio."""
    
    value: float = Field(description="The value to scale")
    ratio: float = Field(description="The scaling ratio")


class ScaleByRatioOutput(BaseModel):
    """Output for ratio scaling."""
    
    result: float = Field(description="The scaled result")


class DirectKInput(BaseModel):
    """Input for finding constant of proportionality k in y = kx."""
    
    x: float = Field(description="The x value (cannot be zero)")
    y: float = Field(description="The y value")
    


class DirectKOutput(BaseModel):
    """Output for proportionality constant calculation."""
    
    k: float = Field(description="The proportionality constant")


class ResizeDimensionsInput(BaseModel):
    """Input for resizing dimensions with uniform scale factor."""
    
    width: float = Field(description="Original width (must be non-negative)")
    height: float = Field(description="Original height (must be non-negative)")
    scale: float = Field(description="Scale factor (must be positive)")


class ResizeDimensionsOutput(BaseModel):
    """Output for dimension resizing."""
    
    new_width: float = Field(description="The new width after scaling")
    new_height: float = Field(description="The new height after scaling")


# Error response model for consistent error handling
class ErrorResponse(BaseModel):
    """Standard error response format."""
    
    error: str = Field(description="Error message")
    detail: Optional[str] = Field(None, description="Additional error details")