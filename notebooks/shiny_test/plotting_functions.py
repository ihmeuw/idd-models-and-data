import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from constants import get_sir_colors, get_plot2_colors, get_plot3_colors, set_matplotlib_colormap

def plot_SIR(data):
    """Create the SIR model plot"""
    SIR_df = data['model_df']
    title1 = data['title1']
    title1 = data['title2']
    colors = get_sir_colors()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
   
    # Plot S, I, R with specific colors and labels
    ax1.plot(SIR_df['time'], SIR_df['S'], color=colors['S'], linewidth=2, label='Susceptible')
    ax1.plot(SIR_df['time'], SIR_df['I'], color=colors['I'], linewidth=2, label='Infected')
    ax1.plot(SIR_df['time'], SIR_df['R'], color=colors['R'], linewidth=2, label='Recovered')
    ax1.set_title(data['title1'])
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Population Proportion")
    ax1.grid(True, alpha=0.3)
    # Dynamic limits based on data
    ax1.set_xlim(SIR_df['time'].min(), SIR_df['time'].max())
    lower_limit = min(0, SIR_df['S'].min(), SIR_df['I'].min(), SIR_df['R'].min())
    upper_limit = max(1, SIR_df['S'].max(), SIR_df['I'].max(), SIR_df['R'].max())
    ax1.set_ylim(lower_limit, upper_limit)
    ax1.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))

    # Add legend that automatically finds the best location
    ax1.legend(loc='best')
    
    ax2.plot(SIR_df['time'], SIR_df['newI'], color=colors['newI'], linewidth=2, label='New Infections')
    ax2.set_title(data['title2'])
    ax2.set_xlabel("Time")
    ax2.set_ylabel("Population Proportion")
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(SIR_df['time'].min(), SIR_df['time'].max())
    ax2.set_ylim(0, max(SIR_df['newI'].max() * 1.1, 0.05))
    ax2.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))

    # Add legend that automatically finds the best location
    ax2.legend(loc='best')
    
    plt.tight_layout()
    return fig

def plot_SEIR(data):
    """Create the SEIR model plot"""
    SEIR_df = data['model_df']
    title1 = data['title1']
    title1 = data['title2']
    colors = get_sir_colors()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

    # Plot S, I, R with specific colors and labels
    ax1.plot(SEIR_df['time'], SEIR_df['S'], color=colors['S'], linewidth=2, label='Susceptible')
    ax1.plot(SEIR_df['time'], SEIR_df['S'], color=colors['S'], linewidth=2, label='Susceptible')
    ax1.plot(SEIR_df['time'], SEIR_df['I'], color=colors['I'], linewidth=2, label='Infected')
    ax1.plot(SEIR_df['time'], SEIR_df['R'], color=colors['R'], linewidth=2, label='Recovered')
    ax1.set_title(data['title1'])
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Population Proportion")
    ax1.grid(True, alpha=0.3)
    # Dynamic limits based on data
    ax1.set_xlim(SEIR_df['time'].min(), SEIR_df['time'].max())
    lower_limit = min(0, SEIR_df['S'].min(), SEIR_df['I'].min(), SEIR_df['R'].min())
    upper_limit = max(1, SEIR_df['S'].max(), SEIR_df['I'].max(), SEIR_df['R'].max())
    ax1.set_ylim(lower_limit, upper_limit)
    ax1.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))

    # Add legend that automatically finds the best location
    ax1.legend(loc='best')
    
    ax2.plot(SEIR_df['time'], SEIR_df['newI'], color=colors['newI'], linewidth=2, label='New Infections')
    ax2.set_title(data['title2'])
    ax2.set_xlabel("Time")
    ax2.set_ylabel("Population Proportion")
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(SEIR_df['time'].min(), SEIR_df['time'].max())
    ax2.set_ylim(0, max(SEIR_df['newI'].max() * 1.1, 0.05))
    ax2.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))

    # Add legend that automatically finds the best location
    ax2.legend(loc='best')
    
    plt.tight_layout()
    return fig

def create_plot1(data):
    fig = plot_SIR(data)
    return fig

def create_plot2(data):
    model = data['model']
    if model == "SIR":
        fig = plot_SIR(data)
    elif model == "SEIR":
        fig = plot_SEIR(data)
    elif model == "SEIRS":
        fig = plot_SEIR(data)
    return fig

def create_plot3(data):
    """Create the multi-panel plot"""
    fig = plt.figure(figsize=(12, 8))
    
    ax1 = plt.subplot2grid((2, 2), (0, 0), fig=fig)
    ax2 = plt.subplot2grid((2, 2), (0, 1), fig=fig)
    ax3 = plt.subplot2grid((2, 2), (1, 0), colspan=2, fig=fig)
    
    # Plot 1 (top left)
    ax1.plot(data['x'], data['y1'], 'b-', linewidth=2)
    ax1.set_title(data['title1'])
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, 10)
    ax1.set_ylim(-2.5, 2.5)
    ax1.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))
    
    # Plot 2 (top right)
    ax2.plot(data['x'], data['y2'], 'r-', linewidth=2)
    ax2.set_title(data['title2'])
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, 10)
    ax2.set_ylim(-2.5, 2.5)
    ax2.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))
    
    # Plot 3 (bottom spanning)
    ax3.plot(data['x'], data['y3'], 'g-', linewidth=3)
    ax3.fill_between(data['x'], 0, data['y3'], alpha=0.3, color='green')
    ax3.set_title(data['title3'])
    ax3.set_xlabel("X Axis")
    ax3.set_ylabel("Y Axis")
    ax3.grid(True, alpha=0.3)
    ax3.set_xlim(0, 10)
    ax3.set_ylim(-8, 8)
    ax3.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))
    
    plt.tight_layout()
    return fig