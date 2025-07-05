"""Synchronization utilities for Shiny reactive inputs."""

from shiny import ui, reactive
from typing import List, Dict, Any, Callable


def create_parameter_sync_functions(
    input: Any, 
    parameters: List[str], 
    prefix: str = "p"
) -> None:
    """
    Create sync functions for parameter sliders and numeric inputs.
    
    Args:
        input: Shiny input object
        parameters: List of parameter names to sync
        prefix: Prefix used for parameter IDs
    """
    
    def create_sync_pair(param_name: str) -> None:
        """Create sync functions for a single parameter."""
        slider_id = f"{prefix}_{param_name}"
        numeric_id = f"{prefix}_{param_name}_num"
        
        @reactive.effect
        def sync_slider_to_numeric():
            try:
                value = input[slider_id]()
                if value is not None:
                    ui.update_numeric(numeric_id, value=value)
            except (KeyError, AttributeError, TypeError):
                pass
        
        @reactive.effect
        def sync_numeric_to_slider():
            try:
                value = input[numeric_id]()
                if value is not None:
                    ui.update_slider(slider_id, value=value)
            except (KeyError, AttributeError, TypeError):
                pass
    
    # Create sync functions for all parameters
    for param in parameters:
        create_sync_pair(param)


def create_model_parameter_sync(
    input: Any,
    model_type: str, 
    prefix: str = "p"
) -> None:
    """
    Create sync functions for epidemiological model parameters.
    
    Args:
        input: Shiny input object
        model_type: Type of model ('SIR', 'SEIR', 'SEIRS')
        prefix: Prefix used for parameter IDs
    """
    base_params = ['i_0', 'beta', 'gamma']
    
    if model_type.upper() in ['SEIR', 'SEIRS']:
        base_params.append('sigma')
    
    if model_type.upper() == 'SEIRS':
        base_params.append('aa')  # average age
    
    create_parameter_sync_functions(input, base_params, prefix)


def create_dynamic_parameter_updater(
    input: Any,
    output: Any,
    model_selector_id: str,
    dynamic_ui_id: str,
    param_values: reactive.Value,
    ui_generator: Callable[[str, Dict], Any],
    prefix: str = "p"
) -> None:
    """
    Create a dynamic UI updater that responds to model selection changes.
    
    Args:
        input: Shiny input object
        output: Shiny output object
        model_selector_id: ID of the model selection input
        dynamic_ui_id: ID of the dynamic UI output
        param_values: Reactive value containing current parameters
        ui_generator: Function that generates UI based on model type and values
        prefix: Prefix used for parameter IDs
    """
    
    @output
    @reactive.ui
    def dynamic_ui():
        try:
            model_type = input[model_selector_id]()
            current_values = param_values.get()
            return ui_generator(model_type, current_values)
        except (KeyError, AttributeError, TypeError):
            # Return empty div if there's an error
            return ui.div()
    
    # Assign the function to the correct output ID
    setattr(output, dynamic_ui_id, dynamic_ui)


def update_parameter_values(
    input: Any,
    param_values: reactive.Value,
    parameters: List[str],
    prefix: str = "p"
) -> None:
    """
    Update reactive parameter values from input controls.
    
    Args:
        input: Shiny input object
        param_values: Reactive value to update
        parameters: List of parameter names
        prefix: Prefix used for parameter IDs
    """
    current_values = param_values.get().copy()
    
    for param in parameters:
        try:
            value = input[f"{prefix}_{param}"]()
            if value is not None:
                current_values[param] = value
        except (KeyError, AttributeError, TypeError):
            pass
    
    param_values.set(current_values)
