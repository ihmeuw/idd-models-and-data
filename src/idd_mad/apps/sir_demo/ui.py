"""UI for SIR demo application."""

from shiny import ui
from ...ui.components import get_component_css
from ...ui.layouts import create_epidemiology_layout


def create_app_ui():
    """Create the UI for the SIR demo app."""
    
    # Default parameter values
    default_params = {
        'i_0': 1,
        'beta': 1,
        'gamma': 1
    }
    
    return ui.page_fixed(
        ui.tags.head(ui.tags.style(get_component_css())),
        ui.div(
            ui.h1("SIR Model Demo", class_="text-center mb-4"),
            create_epidemiology_layout(
                model_type="SIR",
                param_values=default_params,
                plot_output_id="sir_plot",
                prefix="sir",
                include_dt=True,
                button_label="Run SIR Model",
                button_id="update_sir_plot"
            ),
            class_="container-fluid"
        )
    )
