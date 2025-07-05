"""UI for multi-tab dashboard application."""

from shiny import ui
from ...ui.components import get_component_css, parameter_input_with_sync


def create_page1_ui():
    """Create Page 1 - Basic SIR Model."""
    return ui.layout_sidebar(
        ui.sidebar(
            ui.h3("Controls"),
            parameter_input_with_sync("p1_i_0", "Percent infectious at t=0", 0, 10, 1, add_percent=True),
            parameter_input_with_sync("p1_beta", "Transmission Rate (β)", 0.1, 10, 1),
            parameter_input_with_sync("p1_gamma", "Recovery Rate (γ)", 0, 10, 1),
            ui.input_slider("p1_dt", "Time step", min=0.01, max=0.25, value=0.01),
            ui.br(),
            ui.input_action_button("update_plot1", "Run SIR model", class_="btn-primary"),
            width=300
        ),
        ui.div(
            ui.output_plot("plot1", width="100%", height="400px"),
            class_="plot-container"
        )
    )


def create_page2_ui():
    """Create Page 2 - Model Comparison."""
    return ui.layout_sidebar(
        ui.sidebar(
            ui.h3("Controls"),
            ui.input_selectize(
                "dropdown2_1", 
                "Select Model Structure",
                choices=["SIR", "SEIR", "SEIRS"],
                selected="SIR"
            ),
            ui.br(),
            ui.output_ui("dynamic_sliders2"),
            ui.br(),
            ui.input_action_button("update_plot2", "Run model", class_="btn-primary"),
            width=300
        ),
        ui.div(
            ui.output_plot("plot2", width="100%", height="400px"),
            class_="plot-container"
        )
    )


def create_page3_ui():
    """Create Page 3 - Multi-panel Analysis."""
    return ui.layout_sidebar(
        ui.sidebar(
            ui.h3("Controls"),
            ui.input_selectize(
                "dropdown3_1", 
                "Dropdown 1",
                choices=["Choice 1", "Choice 2", "Choice 3", "Choice 4"],
                selected="Choice 1"
            ),
            ui.input_selectize(
                "dropdown3_2", 
                "Dropdown 2", 
                choices=["Type X", "Type Y", "Type Z"],
                selected="Type X"
            ),
            ui.br(),
            ui.input_slider("slider3_1", "Slider 1", min=0, max=100, value=10),
            ui.input_slider("slider3_2", "Slider 2", min=0, max=100, value=90),
            ui.input_slider("slider3_3", "Slider 3", min=0, max=100, value=45),
            ui.input_slider("slider3_4", "Slider 4", min=0, max=100, value=75),
            ui.input_slider("slider3_5", "Slider 5", min=0, max=100, value=35),
            ui.br(),
            ui.input_action_button("update_plot3", "Update Plot 3", class_="btn-primary"),
            width=300
        ),
        ui.div(
            ui.output_plot("plot3", width="100%", height="600px"),
            class_="plot-container"
        )
    )


def create_app_ui():
    """Create the UI for the multi-tab dashboard app."""
    
    return ui.page_navbar(
        ui.nav_panel("Page 1", create_page1_ui()),
        ui.nav_panel("Page 2", create_page2_ui()),
        ui.nav_panel("Page 3", create_page3_ui()),
        title="Multi-Tab Dashboard",
        id="navbar",
        header=ui.tags.head(ui.tags.style(get_component_css()))
    )
