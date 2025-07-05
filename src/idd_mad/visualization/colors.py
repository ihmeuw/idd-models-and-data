"""Color schemes and palettes for visualizations."""

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from typing import Dict

# ColorBrewer Set1 palette
SET1_COLORS = [
    '#e41a1c',  # Red
    '#377eb8',  # Blue  
    '#4daf4a',  # Green
    '#984ea3',  # Purple
    '#ff7f00',  # Orange
    '#ffff33',  # Yellow
    '#a65628',  # Brown
    '#f781bf',  # Pink
    '#999999'   # Gray
]


def get_epidemiology_colors() -> Dict[str, str]:
    """Return standard colors for epidemiological models."""
    return {
        'S': SET1_COLORS[1],   # Blue for Susceptible
        'E': SET1_COLORS[4],   # Orange for Exposed
        'I': SET1_COLORS[0],   # Red for Infected
        'R': SET1_COLORS[2],   # Green for Recovered
        'newI': SET1_COLORS[4], # Orange for new infections
        'newE': SET1_COLORS[3], # Purple for new exposures
        'newR': SET1_COLORS[2]  # Green for new recoveries
    }


def get_color_palette() -> list:
    """Return the Set1 color palette."""
    return SET1_COLORS.copy()


def configure_matplotlib_defaults():
    """Configure matplotlib to use Set1 colors by default."""
    plt.rcParams['axes.prop_cycle'] = plt.cycler(color=SET1_COLORS)
