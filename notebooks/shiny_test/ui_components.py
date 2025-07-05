from shiny import ui

def create_parameter_input(param_id, label, min_val, max_val, default_val, step=0.1, add_percent=False):
    """Create a parameter input with slider and numeric input"""
    post_text = "%" if add_percent else None
    numeric_class = "numeric-percent-container" if add_percent else None
    
    return ui.div(
        ui.p(label, style="margin-bottom: 5px; font-weight: bold;"),
        ui.div(
            ui.input_slider(f"{param_id}", None, min=min_val, max=max_val, value=default_val, step=step, post=post_text),
            ui.div(
                ui.input_numeric(f"{param_id}_num", None, value=default_val, min=min_val, max=max_val, step=step, width="100px"),
                class_=numeric_class
            ),
            style="display: flex; align-items: end; gap: 10px;"
        )
    )

def get_css_styles():
    """Return the CSS styles for the app"""
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
    """

def create_page1_ui():
    """Create the UI for Page 1"""
    return ui.nav_panel(
        "Page 1",
        ui.layout_sidebar(
            ui.sidebar(
                ui.h3("Controls"),
                create_parameter_input("p1_i_0", "Percent infectious at t=0", 0, 10, 1, add_percent=True),
                create_parameter_input("p1_beta", "beta", 0.1, 10, 1),
                create_parameter_input("p1_gamma", "gamma", 0, 10, 1),
                ui.input_slider("p1_dt", "Time step", min=0.01, max=0.25, value=0.01),
                ui.br(),
                ui.input_action_button("update_plot1", "Run SIR model", class_="btn-primary"),
                width=300
            ),
            ui.output_plot("plot1", width="100%", height="400px")
        )
    )

def create_page2_ui():
    """Create the UI for Page 2"""
    return ui.nav_panel(
        "Page 2", 
        ui.layout_sidebar(
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
            ui.output_plot("plot2", width="100%", height="400px")
        )
    )

def create_page3_ui():
    """Create the UI for Page 3"""
    return ui.nav_panel(
        "Page 3",
        ui.layout_sidebar(
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
            ui.output_plot("plot3", width="100%", height="600px")
        )
    )