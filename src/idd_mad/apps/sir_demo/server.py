"""Server logic for SIR demo application."""

from shiny import reactive, render
from ...utils.calculations import ModelCalculator
from ...utils.sync import create_model_parameter_sync
from ...visualization.plotting import create_epidemiology_figure


def create_server(input, output, session):
    """Create server function for SIR demo app."""
    
    # Create reactive values to store parameter values
    param_values = reactive.Value({
        'i_0': 1,
        'beta': 1, 
        'gamma': 1
    })
    
    # Create sync functions for parameters
    create_model_parameter_sync(input, "SIR", "sir")
    
    # Plot rendering
    @output
    @render.plot
    @reactive.event(input.update_sir_plot)
    def sir_plot():
        # Get parameter values
        i_0 = input.sir_i_0() if input.sir_i_0() is not None else 1
        beta = input.sir_beta() if input.sir_beta() is not None else 1
        gamma = input.sir_gamma() if input.sir_gamma() is not None else 1
        dt = input.sir_dt() if input.sir_dt() is not None else 0.01
        
        # Calculate model data
        data = ModelCalculator.calculate_sir_data(
            i_0_percent=i_0,
            beta=beta,
            gamma=gamma,
            dt=dt
        )
        
        # Create and return the figure
        return create_epidemiology_figure(
            df=data['model_df'],
            model_type=data['model_type'],
            title=data['title1']
        )
