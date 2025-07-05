"""Visualization module for epidemiological models."""

from .colors import get_epidemiology_colors, get_color_palette, configure_matplotlib_defaults
from .plotting import plot_sir_model, plot_seir_model, create_epidemiology_figure

__all__ = [
    'get_epidemiology_colors', 
    'get_color_palette', 
    'configure_matplotlib_defaults',
    'plot_sir_model',
    'plot_seir_model', 
    'create_epidemiology_figure'
]
