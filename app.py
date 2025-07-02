"""
Main application entry point for Proportion MCP Server.
Handles both local development and cloud deployment.
"""

import logging
import os
import signal
import sys

from proportion_server import create_gradio_app
from config import get_settings, setup_logging, is_huggingface_space

# Initialize logging and settings
setup_logging()
logger = logging.getLogger(__name__)
settings = get_settings()


def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    logger.info(f"📡 Received signal {signum}, shutting down gracefully...")
    sys.exit(0)


def main() -> None:
    """Main application entry point."""
    
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    logger.info("🚀 Starting Proportion MCP Server")
    logger.info(f"Settings: {settings.model_dump_json(indent=2)}")
    
    # Create Gradio app
    demo = create_gradio_app()
    assert demo is not None, "Failed to create Gradio application"
    logger.info("✅ Gradio application created successfully")
    
    # Launch configuration
    launch_kwargs = {
        "server_name": settings.server_name,
        "server_port": settings.server_port,
        "mcp_server": True,  # Enable MCP server functionality
        "show_error": settings.debug,
        "quiet": not settings.debug,
        "prevent_thread_lock": False,  # Keep main thread alive
    }
    
    # Development-specific settings
    if not settings.is_production():
        launch_kwargs.update({
            "debug": settings.debug,
        })
    
    # Hugging Face Spaces specific settings
    if is_huggingface_space():
        launch_kwargs.update({
            "server_name": "0.0.0.0",  # Required for HF Spaces
            "share": False,  # Don't create gradio.live links on HF
            "quiet": True,  # Reduce logging noise
        })
        logger.info("🤗 Configured for Hugging Face Spaces deployment")
    
    # Log the MCP endpoint information
    if is_huggingface_space():
        space_url = os.environ.get("SPACE_URL", "https://your-space.hf.space")
        logger.info(f"🔗 MCP Server will be available at: {space_url}")
    else:
        logger.info(f"🔗 MCP Server will be available at: http://{settings.server_name}:{settings.server_port}")
    
    logger.info("🔧 MCP Tools exposed: percent_of, solve_proportion, scale_by_ratio, direct_k, resize_dimensions")
    logger.info("📖 Functions with proper type hints and docstrings are automatically exposed as MCP tools")
    
    # Launch the server
    logger.info("🌐 Starting server...")
    demo.launch(**launch_kwargs)
    
    # Keep the main thread alive
    logger.info("✅ Server is running, press Ctrl+C to stop")
    if hasattr(signal, 'pause'):
        # Unix systems
        signal.pause()
    else:
        # Windows systems
        import time
        while True:
            time.sleep(1)


if __name__ == "__main__":
    main()