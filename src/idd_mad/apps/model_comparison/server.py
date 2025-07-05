"""Server logic for model comparison application."""

from shiny import reactive, render, ui
from ...utils.calculations import ModelCalculator
from ...utils.sync import create_parameter_sync_functions
from ...visualization.plotting import create_epidemiology_figure
from ...ui.components import model_parameter_set


def create_server(input, output, session):
    """Create server function for model comparison app."""
    
    # Create reactive values to store parameter values
    param_values = reactive.Value({
        'i_0': 1,
        'beta': 1, 
        'gamma': 1,
        'sigma': 1,
        'aa': 70
    })
    
    # Dynamic UI for model-specific parameters
    @output
    @render.ui
    def dynamic_sliders_comp():
        try:
            model_type = input.comp_model_select()
            if model_type is None:
                model_type = "SIR"
            current_values = param_values.get()
            return model_parameter_set(model_type, current_values, "comp")
        except (AttributeError, TypeError):
            # Return default SIR parameters if there's an error
            return model_parameter_set("SIR", param_values.get(), "comp")
    
    # Create sync functions for all possible parameters
    all_params = ['i_0', 'beta', 'gamma', 'sigma', 'aa']
    create_parameter_sync_functions(input, all_params, "comp")
    
    # Plot rendering
    @output
    @render.plot
    @reactive.event(input.update_comparison_plot)
    def comparison_plot():
        # Get model type
        model_type = input.comp_model_select() if input.comp_model_select() is not None else "SIR"
        
        # Get parameter values
        i_0 = input.comp_i_0() if input.comp_i_0() is not None else 1
        beta = input.comp_beta() if input.comp_beta() is not None else 1
        gamma = input.comp_gamma() if input.comp_gamma() is not None else 1
        sigma = input.comp_sigma() if input.comp_sigma() is not None else 1
        aa = input.comp_aa() if input.comp_aa() is not None else 70
        
        # Calculate model data
        data = ModelCalculator.calculate_model_data(
            model_type=model_type,
            i_0_percent=i_0,
            beta=beta,
            gamma=gamma,
            sigma=sigma,
            average_age=aa
        )
        
        # Create and return the figure
        return create_epidemiology_figure(
            df=data['model_df'],
            model_type=data['model_type'],
            title=data['title1']
        )
