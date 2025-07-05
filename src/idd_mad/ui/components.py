"""Reusable UI components for Shiny applications."""

from shiny import ui
from typing import Optional, List, Dict, Any


def parameter_input_with_sync(
    param_id: str,
    label: str,
    min_val: float,
    max_val: float,
    default_val: float,
    step: float = 0.1,
    add_percent: bool = False,
    width: str = "100px"
) -> ui.Tag:
    """
    Create a synchronized parameter input with slider and numeric input.
    
    Args:
        param_id: Unique identifier for the parameter
        label: Display label
        min_val: Minimum value
        max_val: Maximum value  
        default_val: Default value
        step: Step size
        add_percent: Whether to add % symbol
        width: Width of numeric input
    """
    post_text = "%" if add_percent else None
    numeric_class = "numeric-percent-container" if add_percent else None
    
    return ui.div(
        ui.p(label, style="margin-bottom: 5px; font-weight: bold;"),
        ui.div(
            ui.input_slider(
                param_id, 
                None, 
                min=min_val, 
                max=max_val, 
                value=default_val, 
                step=step, 
                post=post_text
            ),
            ui.div(
                ui.input_numeric(
                    f"{param_id}_num", 
                    None, 
                    value=default_val, 
                    min=min_val, 
                    max=max_val, 
                    step=step, 
                    width=width
                ),
                class_=numeric_class
            ),
            style="display: flex; align-items: end; gap: 10px;"
        )
    )


def model_parameter_set(model_type: str, param_values: Dict[str, float], prefix: str = "p") -> ui.Tag:
    """
    Create parameter inputs for different epidemiological models.
    
    Args:
        model_type: One of 'SIR', 'SEIR', 'SEIRS'
        param_values: Dictionary of current parameter values
        prefix: Prefix for parameter IDs
    """
    base_params = [
        parameter_input_with_sync(
            f"{prefix}_i_0", "Initial % Infected", 0, 10, 
            param_values.get('i_0', 1), add_percent=True
        ),
        parameter_input_with_sync(
            f"{prefix}_beta", "Transmission Rate (β)", 0.1, 10, 
            param_values.get('beta', 1)
        )
    ]
    
    if model_type.upper() in ['SEIR', 'SEIRS']:
        base_params.append(
            parameter_input_with_sync(
                f"{prefix}_sigma", "Incubation Rate (σ)", 0.1, 10, 
                param_values.get('sigma', 1)
            )
        )
    
    base_params.append(
        parameter_input_with_sync(
            f"{prefix}_gamma", "Recovery Rate (γ)", 0.1, 10, 
            param_values.get('gamma', 1)
        )
    )
    
    if model_type.upper() == 'SEIRS':
        base_params.append(
            parameter_input_with_sync(
                f"{prefix}_aa", "Average Age (1/μ)", 0, 100, 
                param_values.get('aa', 70)
            )
        )
    
    return ui.div(*base_params, class_="model-controls")


def create_model_controls_sidebar(
    model_type: str,
    param_values: Dict[str, float],
    prefix: str = "p",
    include_dt: bool = False,
    button_label: str = "Run Model",
    button_id: str = "update_plot"
) -> ui.Tag:
    """
    Create a complete sidebar with model controls.
    
    Args:
        model_type: Type of epidemiological model
        param_values: Current parameter values
        prefix: Prefix for parameter IDs
        include_dt: Whether to include time step control
        button_label: Text for the action button
        button_id: ID for the action button
    """
    controls = [
        ui.h3("Controls"),
        model_parameter_set(model_type, param_values, prefix)
    ]
    
    if include_dt:
        controls.append(
            ui.input_slider(
                f"{prefix}_dt", "Time step", 
                min=0.01, max=0.25, value=0.01
            )
        )
    
    controls.extend([
        ui.br(),
        ui.input_action_button(button_id, button_label, class_="btn-primary")
    ])
    
    return ui.sidebar(*controls, width=300)


def create_model_selector_sidebar(
    model_options: List[str],
    selected_model: str,
    param_values: Dict[str, float],
    prefix: str = "p",
    button_label: str = "Run Model",
    button_id: str = "update_plot"
) -> ui.Tag:
    """
    Create a sidebar with model selection dropdown and dynamic controls.
    
    Args:
        model_options: List of available model types
        selected_model: Currently selected model
        param_values: Current parameter values
        prefix: Prefix for parameter IDs
        button_label: Text for the action button
        button_id: ID for the action button
    """
    return ui.sidebar(
        ui.h3("Controls"),
        ui.input_selectize(
            f"{prefix}_model_select", 
            "Select Model Structure",
            choices=model_options,
            selected=selected_model
        ),
        ui.br(),
        ui.output_ui(f"dynamic_sliders_{prefix}"),
        ui.br(),
        ui.input_action_button(button_id, button_label, class_="btn-primary"),
        width=300
    )


def get_component_css() -> str:
    """Return CSS styles for UI components."""
    return """
        .numeric-percent-container {
            position: relative;
            display: inline-block;
        }
        .numeric-percent-container input {
            padding-right: 25px !important;
            text-align: left !important;
        }
        .numeric-percent-container::after {
            content: '%';
            position: absolute;
            right: 25px;
            top: 50%;
            transform: translateY(-50%);
            color: #333;
            font-size: 14px;
            font-weight: normal;
            pointer-events: none;
            z-index: 1;
        }
        .numeric-percent-container .form-control {
            padding-right: 25px !important;
        }
        
        .model-controls {
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 5px;
            margin-bottom: 15px;
        }
        
        .plot-container {
            border: 1px solid #dee2e6;
            border-radius: 5px;
            padding: 10px;
            background-color: white;
        }
        
        .nav-panel {
            padding: 20px;
        }
        
        .sidebar-content {
            padding: 15px;
        }
    """
