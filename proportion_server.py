"""
Core proportion calculation tools with Gradio MCP server capabilities.
Provides reliable mathematical operations for LLM agents.
"""

import logging
from typing import Optional, Tuple
import gradio as gr

from config import get_settings, setup_logging, get_deployment_info

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)
settings = get_settings()


def percent_of(part: float, whole: float) -> float:
    """
    Calculate what percentage 'part' is of 'whole'.
    
    Args:
        part: The part value
        whole: The whole value (must not be zero)
        
    Returns:
        The percentage value
    
    Mathematical preconditions:
        - whole != 0 (to avoid division by zero)
    """
    # Mathematical preconditions
    assert whole != 0, "Division by zero: whole cannot be zero"
    
    # Calculate percentage
    percentage = (part / whole) * 100
    
    logger.debug(f"Calculated {part} is {percentage:.2f}% of {whole}")
    
    return percentage


def solve_proportion(
    a: Optional[float] = None,
    b: Optional[float] = None,
    c: Optional[float] = None,
    d: Optional[float] = None
) -> float:
    """
    Solve missing term in proportion a/b = c/d.
    Exactly one parameter must be None (missing).
    
    Args:
        a: First numerator (optional)
        b: First denominator (optional, cannot be zero)
        c: Second numerator (optional)
        d: Second denominator (optional, cannot be zero)
        
    Returns:
        The missing value
    
    Mathematical preconditions:
        - Exactly one value must be None (missing)
        - Division denominators != 0 (varies by missing value)
    """
    # Mathematical preconditions - exactly one value must be None
    values = [a, b, c, d]
    none_count = sum(1 for v in values if v is None)
    assert none_count == 1, "Exactly one value must be None"
    
    # Solve for missing value using cross multiplication: a*d = b*c
    if a is None:
        assert d != 0, "Division by zero: denominator"
        missing = (b * c) / d
    elif b is None:
        assert c != 0, "Division by zero: denominator"
        missing = (a * d) / c
    elif c is None:
        assert b != 0, "Division by zero: denominator"
        missing = (a * d) / b
    else:  # d is None
        assert a != 0, "Division by zero: denominator"
        missing = (b * c) / a
    
    logger.debug(f"Solved proportion: missing value = {missing}")
    
    return missing


def scale_by_ratio(value: float, ratio: float) -> float:
    """
    Scale a value by a given ratio.
    
    Args:
        value: The value to scale
        ratio: The scaling ratio
        
    Returns:
        The scaled value
    """
    # Calculate scaled result
    scaled_result = value * ratio
    
    logger.debug(f"Scaled {value} by ratio {ratio} = {scaled_result}")
    
    return scaled_result


def direct_k(x: float, y: float) -> float:
    """
    Find constant of proportionality k in direct variation y = kx.
    
    Args:
        x: The x value (cannot be zero)
        y: The y value
        
    Returns:
        The proportionality constant k
    
    Mathematical preconditions:
        - x != 0 (to avoid division by zero)
    """
    # Mathematical preconditions
    assert x != 0, "Division by zero: x cannot be zero"
    
    # Calculate proportionality constant
    k = y / x
    
    logger.debug(f"Found proportionality constant k = {k} for y = {y}, x = {x}")
    
    return k


def resize_dimensions(width: float, height: float, scale: float) -> Tuple[float, float]:
    """
    Resize dimensions with uniform scale factor.

    Args:
        width: Original width (must be non-negative)
        height: Original height (must be non-negative)
        scale: Scale factor (must be positive)

    Returns:
        Tuple of (new_width, new_height)

    Mathematical preconditions:
        - width >= 0 (dimensions must be non-negative)
        - height >= 0 (dimensions must be non-negative)
        - scale > 0 (scale factor must be positive)
    """
    # Mathematical preconditions
    assert width >= 0, "Width must be non-negative"
    assert height >= 0, "Height must be non-negative"
    assert scale > 0, "Scale factor must be positive"
    
    # Calculate new dimensions
    new_width = width * scale
    new_height = height * scale
    
    logger.debug(f"Resized {width}x{height} by {scale} = {new_width}x{new_height}")
    
    return (new_width, new_height)


# Demo functions for Gradio interface
def demo_percent_of(part: float, whole: float) -> str:
    """Demo function for percent_of calculation."""
    result = percent_of(part, whole)
    return f"{part} is {result:.2f}% of {whole}"


def demo_solve_proportion(a: Optional[str], b: Optional[str], c: Optional[str], d: Optional[str]) -> str:
    """Demo function for proportion solving."""
    # Convert string inputs to float or None
    a_val = None if a == "" or a is None else float(a)
    b_val = None if b == "" or b is None else float(b)
    c_val = None if c == "" or c is None else float(c)
    d_val = None if d == "" or d is None else float(d)
    
    result = solve_proportion(a_val, b_val, c_val, d_val)
    return f"Missing value: {result:.4f}"


def demo_scale_by_ratio(value: float, ratio: float) -> str:
    """Demo function for scaling by ratio."""
    result = scale_by_ratio(value, ratio)
    return f"{value} × {ratio} = {result:.4f}"


def demo_direct_k(x: float, y: float) -> str:
    """Demo function for finding proportionality constant."""
    result = direct_k(x, y)
    return f"k = {result:.4f} (where y = kx)"


def demo_resize_dimensions(width: float, height: float, scale: float) -> str:
    """Demo function for resizing dimensions."""
    new_width, new_height = resize_dimensions(width, height, scale)
    return f"New dimensions: {new_width:.2f} × {new_height:.2f}"


def create_gradio_app():
    """Create and return the Gradio interface."""
    with gr.Blocks(
        title="PROPORTIO",
        css_paths=["styles.css"],
        theme=gr.themes.Base(),
        head='<link rel="icon" type="image/png" href="/file=logo.png"><link rel="shortcut icon" type="image/png" href="/file=logo.png">'
    ) as demo:
        with gr.Row():
            with gr.Column(scale=1, min_width=72):
                gr.Image("logo.png", height=72, width=72, show_label=False, show_download_button=False, show_fullscreen_button=False, container=False, interactive=False)
            with gr.Column(scale=10):
                gr.HTML("""
                <div class="p-brand">
                    <h1 class="p-title">PROPORTIO</h1>
                    <div class="p-tagline">Mathematical Precision & Proportion Calculator</div>
                </div>
                """)
        
        with gr.Tabs():
            with gr.TabItem("📊 Percentage Calculator"):
                gr.HTML('<div class="tab-title">Calculate Percentage</div>')
                gr.HTML('<div class="tab-desc">Find what percentage the part is of the whole</div>')
                
                with gr.Row():
                    with gr.Column(scale=1):
                        part_input = gr.Number(label="Part", value=25, info="The part value")
                        whole_input = gr.Number(label="Whole", value=100, info="The whole value (cannot be zero)")
                        percent_btn = gr.Button("Calculate Percentage", variant="secondary", size="lg")
                    
                    with gr.Column(scale=1):
                        percent_output = gr.Textbox(label="Result", interactive=False, show_label=True)
                        gr.HTML('<div class="formula-box"><strong>Formula:</strong> (Part ÷ Whole) × 100</div>')
            
            with gr.TabItem("⚖️ Proportion Solver"):
                gr.HTML('<div class="tab-title">Solve Proportion (a/b = c/d)</div>')
                gr.HTML('<div class="tab-desc">Leave exactly one field empty to solve for the missing value</div>')
                
                with gr.Row():
                    with gr.Column(scale=1):
                        with gr.Row():
                            a_input = gr.Textbox(label="a", value="3", info="First numerator")
                            b_input = gr.Textbox(label="b", value="4", info="First denominator")
                        with gr.Row():
                            c_input = gr.Textbox(label="c", value="6", info="Second numerator")
                            d_input = gr.Textbox(label="d", value="", info="Second denominator")
                        proportion_btn = gr.Button("Solve Proportion", variant="secondary", size="lg")
                    
                    with gr.Column(scale=1):
                        proportion_output = gr.Textbox(label="Result", interactive=False, show_label=True)
                        gr.HTML('<div class="formula-box"><strong>Formula:</strong> a × d = b × c</div>')
            
            with gr.TabItem("📏 Scale by Ratio"):
                gr.HTML('<div class="tab-title">Scale Value by Ratio</div>')
                gr.HTML('<div class="tab-desc">Multiply a value by a scaling ratio</div>')
                
                with gr.Row():
                    with gr.Column(scale=1):
                        value_input = gr.Number(label="Value", value=10, info="The value to scale")
                        ratio_input = gr.Number(label="Ratio", value=1.5, info="The scaling factor")
                        scale_btn = gr.Button("Scale Value", variant="secondary", size="lg")
                    
                    with gr.Column(scale=1):
                        scale_output = gr.Textbox(label="Result", interactive=False, show_label=True)
                        gr.HTML('<div class="formula-box"><strong>Formula:</strong> Value × Ratio</div>')
            
            with gr.TabItem("🔢 Find Constant k"):
                gr.HTML('<div class="tab-title">Find Proportionality Constant (y = kx)</div>')
                gr.HTML('<div class="tab-desc">Calculate the constant k in direct variation</div>')
                
                with gr.Row():
                    with gr.Column(scale=1):
                        x_input = gr.Number(label="x", value=5, info="The x value (cannot be zero)")
                        y_input = gr.Number(label="y", value=15, info="The y value")
                        direct_btn = gr.Button("Find k", variant="secondary", size="lg")
                    
                    with gr.Column(scale=1):
                        direct_output = gr.Textbox(label="Result", interactive=False, show_label=True)
                        gr.HTML('<div class="formula-box"><strong>Formula:</strong> k = y ÷ x</div>')
            
            with gr.TabItem("📐 Resize Dimensions"):
                gr.HTML('<div class="tab-title">Resize Dimensions</div>')
                gr.HTML('<div class="tab-desc">Scale width and height by a uniform factor</div>')
                
                with gr.Row():
                    with gr.Column(scale=1):
                        width_input = gr.Number(label="Width", value=100, info="Original width (≥ 0)")
                        height_input = gr.Number(label="Height", value=50, info="Original height (≥ 0)")
                        scale_dim_input = gr.Number(label="Scale Factor", value=2.0, info="Scaling factor (> 0)")
                        resize_btn = gr.Button("Resize", variant="secondary", size="lg")
                    
                    with gr.Column(scale=1):
                        resize_output = gr.Textbox(label="Result", interactive=False, show_label=True)
                        gr.HTML('<div class="formula-box"><strong>Formula:</strong> New = Original × Scale</div>')
        
        # Event handlers
        percent_btn.click(
            demo_percent_of,
            inputs=[part_input, whole_input],
            outputs=[percent_output]
        )
        
        proportion_btn.click(
            demo_solve_proportion,
            inputs=[a_input, b_input, c_input, d_input],
            outputs=[proportion_output]
        )
        
        scale_btn.click(
            demo_scale_by_ratio,
            inputs=[value_input, ratio_input],
            outputs=[scale_output]
        )
        
        direct_btn.click(
            demo_direct_k,
            inputs=[x_input, y_input],
            outputs=[direct_output]
        )
        
        resize_btn.click(
            demo_resize_dimensions,
            inputs=[width_input, height_input, scale_dim_input],
            outputs=[resize_output]
        )
        
        gr.HTML("""
        <div class="footer">
            <div class="footer-content">
                <div class="footer-section">
                    <div class="footer-title">About</div>
                    <div class="footer-text">Professional mathematical calculations for proportions, percentages, and scaling operations.</div>
                </div>
                <div class="footer-section">
                    <div class="footer-title">Features</div>
                    <div class="footer-text">• Assertion-based validation<br>• Precise error handling<br>• MCP server integration</div>
                </div>
            </div>
        </div>
        """)
    
    return demo


if __name__ == "__main__":
    # Get deployment info
    deployment_info = get_deployment_info()
    logger.info(f"Starting Proportio Calculator - {deployment_info}")
    
    # Create and launch the interface
    demo = create_gradio_app()
    
    # Launch with MCP server capabilities
    demo.launch(
        server_name="0.0.0.0",
        server_port=settings.PORT,
        share=settings.SHARE,
        mcp_server=True,  # Enable MCP server functionality
        show_error=True
    )