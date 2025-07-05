"""Multi-Tab Dashboard Shiny Application - recreates the original app functionality."""

import signal
import sys
from shiny import App
from .ui import create_app_ui
from .server import create_server


def create_multi_tab_dashboard_app() -> App:
    """Create and return the multi-tab dashboard Shiny app."""
    return App(create_app_ui(), create_server)


# For direct execution
app = create_multi_tab_dashboard_app()

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    print("\nShutting down gracefully...")
    sys.exit(0)

if __name__ == "__main__":
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        app.run(host="127.0.0.1", port=8000)
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
    finally:
        sys.exit(0)
