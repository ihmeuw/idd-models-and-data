import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np

# ColorBrewer Set1 palette (8 colors + gray)
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

def get_color_palette():
    """Return the Set1 color palette"""
    return SET1_COLORS

def get_sir_colors():
    """Return specific colors for SIR model plots"""
    return {
        'S': SET1_COLORS[1],  # Blue for Susceptible
        'I': SET1_COLORS[0],  # Red for Infected
        'R': SET1_COLORS[2],  # Green for Recovered
        'newI': SET1_COLORS[4]  # Orange for new infections
    }

def get_plot2_colors():
    """Return colors for plot 2"""
    return {
        'scatter': SET1_COLORS[3],  # Purple
        'bar': SET1_COLORS[5]       # Yellow
    }

def get_plot3_colors():
    """Return colors for plot 3"""
    return {
        'panel1': SET1_COLORS[1],   # Blue
        'panel2': SET1_COLORS[0],   # Red
        'panel3': SET1_COLORS[2],   # Green
        'panel3_fill': SET1_COLORS[2]  # Green with alpha
    }

def set_matplotlib_colormap():
    """Set the default matplotlib colormap to Set1"""
    plt.rcParams['axes.prop_cycle'] = plt.cycler(color=SET1_COLORS)