"""Shiny applications for epidemiological modeling."""

from typing import Dict, Callable, List
from shiny import App


def get_available_apps() -> Dict[str, Callable[[], App]]:
    """Return dictionary of available apps and their factory functions."""
    apps = {}
    
    try:
        from .sir_demo.app import create_sir_demo_app
        apps['sir_demo'] = create_sir_demo_app
    except ImportError:
        pass
    
    try:
        from .model_comparison.app import create_model_comparison_app
        apps['model_comparison'] = create_model_comparison_app
    except ImportError:
        pass
    
    try:
        from .multi_tab_dashboard.app import create_multi_tab_dashboard_app
        apps['multi_tab_dashboard'] = create_multi_tab_dashboard_app
    except ImportError:
        pass
    
    # Add more apps as they're developed
    return apps


def run_app(app_name: str, **kwargs):
    """
    Run a specific app by name.
    
    Args:
        app_name: Name of the app to run
        **kwargs: Additional arguments to pass to app.run()
    """
    import signal
    import sys
    
    def signal_handler(signum, frame):
        """Handle shutdown signals gracefully."""
        print("\nShutting down gracefully...")
        sys.exit(0)
    
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    apps = get_available_apps()
    if app_name not in apps:
        available = ', '.join(apps.keys())
        raise ValueError(f"App '{app_name}' not found. Available apps: {available}")
    
    app = apps[app_name]()
    
    try:
        # Set default parameters for better behavior
        default_kwargs = {"host": "127.0.0.1", "port": 8000}
        default_kwargs.update(kwargs)
        app.run(**default_kwargs)
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
    finally:
        sys.exit(0)


def list_apps() -> List[str]:
    """Return list of available app names."""
    return list(get_available_apps().keys())
