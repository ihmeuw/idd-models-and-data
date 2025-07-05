"""Plotting functions for epidemiological models."""

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
from typing import Dict, Tuple, Optional, List
from .colors import get_epidemiology_colors


def plot_sir_model(
    df: pd.DataFrame, 
    title: str = "SIR Model Simulation",
    figsize: Tuple[int, int] = (10, 4),
    show_new_infections: bool = True
) -> plt.Figure:
    """
    Create a plot for SIR model results.
    
    Args:
        df: DataFrame with columns: time, S, I, R, newI
        title: Title for the main plot
        figsize: Figure size tuple
        show_new_infections: Whether to show new infections subplot
        
    Returns:
        Matplotlib figure
    """
    colors = get_epidemiology_colors()
    
    if show_new_infections:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    else:
        fig, ax1 = plt.subplots(1, 1, figsize=(figsize[0]/2, figsize[1]))
    
    # Plot S, I, R compartments
    ax1.plot(df['time'], df['S'], color=colors['S'], linewidth=2, label='Susceptible')
    ax1.plot(df['time'], df['I'], color=colors['I'], linewidth=2, label='Infected')
    ax1.plot(df['time'], df['R'], color=colors['R'], linewidth=2, label='Recovered')
    
    ax1.set_title(title)
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Population Proportion")
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(df['time'].min(), df['time'].max())
    
    # Dynamic y-limits
    lower_limit = min(0, df[['S', 'I', 'R']].min().min())
    upper_limit = max(1, df[['S', 'I', 'R']].max().max())
    ax1.set_ylim(lower_limit, upper_limit)
    ax1.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))
    ax1.legend(loc='best')
    
    if show_new_infections and 'newI' in df.columns:
        # Plot new infections
        ax2.plot(df['time'], df['newI'], color=colors['newI'], linewidth=2, label='New Infections')
        ax2.set_title("New Infections")
        ax2.set_xlabel("Time")
        ax2.set_ylabel("Population Proportion")
        ax2.grid(True, alpha=0.3)
        ax2.set_xlim(df['time'].min(), df['time'].max())
        ax2.set_ylim(0, max(df['newI'].max() * 1.1, 0.05))
        ax2.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))
        ax2.legend(loc='best')
    
    plt.tight_layout()
    return fig


def plot_seir_model(
    df: pd.DataFrame, 
    title: str = "SEIR Model Simulation",
    figsize: Tuple[int, int] = (10, 4),
    show_new_infections: bool = True
) -> plt.Figure:
    """
    Create a plot for SEIR model results.
    
    Args:
        df: DataFrame with columns: time, S, E, I, R, newI
        title: Title for the main plot
        figsize: Figure size tuple
        show_new_infections: Whether to show new infections subplot
        
    Returns:
        Matplotlib figure
    """
    colors = get_epidemiology_colors()
    
    if show_new_infections:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    else:
        fig, ax1 = plt.subplots(1, 1, figsize=(figsize[0]/2, figsize[1]))
    
    # Plot S, E, I, R compartments
    ax1.plot(df['time'], df['S'], color=colors['S'], linewidth=2, label='Susceptible')
    if 'E' in df.columns:
        ax1.plot(df['time'], df['E'], color=colors['E'], linewidth=2, label='Exposed')
    ax1.plot(df['time'], df['I'], color=colors['I'], linewidth=2, label='Infected')
    ax1.plot(df['time'], df['R'], color=colors['R'], linewidth=2, label='Recovered')
    
    ax1.set_title(title)
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Population Proportion")
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(df['time'].min(), df['time'].max())
    
    # Dynamic y-limits
    columns_to_check = ['S', 'I', 'R']
    if 'E' in df.columns:
        columns_to_check.append('E')
    
    lower_limit = min(0, df[columns_to_check].min().min())
    upper_limit = max(1, df[columns_to_check].max().max())
    ax1.set_ylim(lower_limit, upper_limit)
    ax1.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))
    ax1.legend(loc='best')
    
    if show_new_infections and 'newI' in df.columns:
        # Plot new infections
        ax2.plot(df['time'], df['newI'], color=colors['newI'], linewidth=2, label='New Infections')
        ax2.set_title("New Infections")
        ax2.set_xlabel("Time")
        ax2.set_ylabel("Population Proportion")
        ax2.grid(True, alpha=0.3)
        ax2.set_xlim(df['time'].min(), df['time'].max())
        ax2.set_ylim(0, max(df['newI'].max() * 1.1, 0.05))
        ax2.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))
        ax2.legend(loc='best')
    
    plt.tight_layout()
    return fig


def create_epidemiology_figure(
    df: pd.DataFrame,
    model_type: str,
    title: Optional[str] = None,
    figsize: Tuple[int, int] = (10, 4),
    show_new_infections: bool = True
) -> plt.Figure:
    """
    Create a figure for epidemiological model results.
    
    Args:
        df: DataFrame with simulation results
        model_type: Type of model ('SIR', 'SEIR', 'SEIRS')
        title: Custom title (auto-generated if None)
        figsize: Figure size tuple
        show_new_infections: Whether to show new infections subplot
        
    Returns:
        Matplotlib figure
    """
    if title is None:
        title = f"{model_type} Model Simulation"
    
    if model_type.upper() == 'SIR':
        return plot_sir_model(df, title, figsize, show_new_infections)
    elif model_type.upper() in ['SEIR', 'SEIRS']:
        return plot_seir_model(df, title, figsize, show_new_infections)
    else:
        raise ValueError(f"Unknown model type: {model_type}")


def create_multi_panel_figure(
    data_dict: Dict[str, Dict],
    figsize: Tuple[int, int] = (12, 8)
) -> plt.Figure:
    """
    Create a multi-panel figure for complex visualizations.
    
    Args:
        data_dict: Dictionary with panel data
        figsize: Figure size tuple
        
    Returns:
        Matplotlib figure
    """
    fig = plt.figure(figsize=figsize)
    
    # Create subplot layout based on number of panels
    n_panels = len(data_dict)
    if n_panels <= 2:
        rows, cols = 1, n_panels
    elif n_panels <= 4:
        rows, cols = 2, 2
    else:
        rows = int(np.ceil(n_panels / 3))
        cols = 3
    
    for i, (panel_name, panel_data) in enumerate(data_dict.items()):
        ax = plt.subplot(rows, cols, i + 1)
        
        # Extract data
        x = panel_data.get('x', [])
        y = panel_data.get('y', [])
        title = panel_data.get('title', f'Panel {i+1}')
        color = panel_data.get('color', 'blue')
        plot_type = panel_data.get('type', 'line')
        
        # Create plot based on type
        if plot_type == 'line':
            ax.plot(x, y, color=color, linewidth=2)
        elif plot_type == 'fill':
            ax.plot(x, y, color=color, linewidth=2)
            ax.fill_between(x, 0, y, alpha=0.3, color=color)
        elif plot_type == 'scatter':
            ax.scatter(x, y, color=color)
        
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
        
        # Set limits if provided
        if 'xlim' in panel_data:
            ax.set_xlim(panel_data['xlim'])
        if 'ylim' in panel_data:
            ax.set_ylim(panel_data['ylim'])
        
        ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))
    
    plt.tight_layout()
    return fig
