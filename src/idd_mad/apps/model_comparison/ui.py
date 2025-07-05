"""UI for model comparison application."""

from shiny import ui
from ...ui.components import get_component_css
from ...ui.layouts import create_model_comparison_layout


def create_app_ui():
    """Create the UI for the model comparison app."""
    
    # Default parameter values
    default_params = {
        'i_0': 1,
        'beta': 1,
        'gamma': 1,
        'sigma': 1,
        'aa': 70
    }
    
    model_options = ["SIR", "SEIR", "SEIRS"]
    
    return ui.page_fixed(
        ui.tags.head(ui.tags.style(get_component_css())),
        ui.div(
            ui.h1("Epidemiological Model Comparison", class_="text-center mb-4"),
            create_model_comparison_layout(
                model_options=model_options,
                selected_model="SIR",
                param_values=default_params,
                plot_output_id="comparison_plot",
                prefix="comp",
                button_label="Run Model",
                button_id="update_comparison_plot"
            ),
            class_="container-fluid"
        )
    )
